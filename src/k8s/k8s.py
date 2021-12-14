from kubernetes import client, config, watch
from kubernetes.client.rest import ApiException
from kubernetes.stream import stream

import logging
import math

try:
    config.load_incluster_config()
except config.ConfigException:
    try:
        config.load_kube_config()
    except config.ConfigException:
        raise Exception("Could not configure kubernetes python client")


v1 = client.CoreV1Api()
appsV1Api = client.AppsV1Api()


def get_pods(namespace, label_selector=None, field_selector=None):
    """
    List pods in specific namespace and return pod list with podnames
    """
    pods = []
    logging.info(f"Listing pods in namespace: {namespace}")

    pod_list = v1.list_namespaced_pod(namespace, label_selector=label_selector, field_selector=field_selector)

    for pod in pod_list.items:
        logging.info("%s\t%s\t%s" % (pod.metadata.name,
                                     pod.status.phase,
                                     pod.status.pod_ip))
        pods.append(pod.metadata.name)
    return pods


def get_node_pods(namespace, label_selector, node_name):
    '''
    Return a list of pods for specific node 

    :namespace (str)        : K8s namespace, default couchdb
    :label_selector (str)   : Selector to filter pods in k8s, default app=couchdb
    :node_name (str)        : Name of K8s node

    '''
    field_selector = 'spec.nodeName='+node_name
    logging.info(f"get pods of node: {node_name}")
    pods = get_pods(namespace, label_selector=label_selector, field_selector=field_selector)
    
    return pods


def get_nodes_pods(nodes: list):
    ''' 
    Add list of pods for nodes dictionary

    :nodes (dict): List of Dictionaries with nodes information

    Return nodes with list of pods
    '''
    for node in nodes:
        node_pods = get_node_pods(namespace='couchdb', label_selector='app=couchdb', node_name=node['node'])
        node['pods'] = node_pods
    
    return nodes
    

def delete_pods(pods, namespace):
    logging.info(f"Deleting PODS {pods} in namespace {namespace}")
    for pod in pods:
        try:
            v1.delete_namespaced_pod(pod, namespace)
        except ApiException as e:
            logging.info(
                "Exception when calling CoreV1Api->delete_namespaced_pod: %s\n" % e)


def watch_pods_state(pods, namespace, desired_state='Pending'):
    terminating = False
    pods_status = {pod: False for pod in pods}
    w = watch.Watch()
    for event in w.stream(func=v1.list_namespaced_pod,
                          namespace=namespace,
                          label_selector=f"app=couchdb, statefulset.kubernetes.io/pod-name={pods[0]}"):
        status_pod = event['object'].status.phase

        logging.info(
            f"Event: {event['type']} {event['object'].kind} {event['object'].metadata.name} {event['object'].status.phase}")

        if status_pod == 'Pending':
            terminating = True

        if status_pod == desired_state and terminating:
            pods_status[event['object'].metadata.name] = True

        # Check if all pods are in desired_state
        if all(pods_status.values()):
            logging.info(f"All desired pods are in {desired_state} State")
            w.stop()
        else:
            logging.info(f"Not all pods are {desired_state}...")


def get_related_pod_pvc(pods, namespace):
    pod_pvc_info = {}
    for pod in pods:
        pvc_info = []
        api_response = v1.read_namespaced_pod(name=pod, namespace=namespace)

        # Get name of PVC
        pvc_name = api_response.spec.volumes[0].persistent_volume_claim.claim_name
        pvc_info.append(pvc_name)

        # Get value of size PVC
        pvc_metadata = v1.read_namespaced_persistent_volume_claim(
            namespace=namespace, name=pvc_name)

        # logging.info(f'pvc_info: {pvc_metadata}')

        # pvc_size = pvc_info.spec.resources.requests['storage']
        pvc_size = pvc_metadata.status.capacity['storage']

        pvc_info.append(pvc_size)

        pod_pvc_info[pod] = pvc_info
    return pod_pvc_info


def get_namespaces_pvc(namespace):
    return v1.list_namespaced_persistent_volume_claim(namespace)


def patch_namespaced_pvc(namespace, pod_pvc_info, resize_percentage):
    for pod, pvc in pod_pvc_info.items():
        pvc_size = int(pvc[1].strip('Gi'))  # Must be in Gi unit
        pvc_resize_number = int(
            math.ceil(pvc_size*(1+resize_percentage)))  # Upper function
        pvc_resize_value = str(pvc_resize_number)+'Gi'

        spec_body = {'spec': {'resources': {
            'requests': {'storage': pvc_resize_value}}}}

        logging.info(f"resizing {pvc[0]}-{pvc[1]} to {pvc_resize_value}")
        resize_response = v1.patch_namespaced_persistent_volume_claim(
            pvc[0], namespace, spec_body)

        # Delete POD associated to PVC
        delete_pods([pod], namespace)

        # Wait until pod to Running State
        watch_pods_state([pod], namespace, 'Running')


def execute_exec_pods(exec_command, namespace, pod):
    resp = stream(v1.connect_get_namespaced_pod_exec, pod, namespace,
                  command=exec_command, stderr=True, stdin=False, stdout=True, tty=False)
    return resp


def get_pods_volumes_info(namespace, pods, mount_volume_path):
    exec_command = ['df', '-Ph', mount_volume_path]
    pods_volumes_info = {}

    for pod in pods:
        # Execute command df inside each POD to obtain %Use of volume associated
        resp = execute_exec_pods(exec_command, namespace, pod)
        df_output_lines = [s.split() for s in resp.splitlines()]
        perc_usage = float(df_output_lines[1][4].strip('%'))/100
        pods_volumes_info[pod] = perc_usage

    return pods_volumes_info


def get_nodes():
    logging.info("Getting k8s nodes...")
    nodes = []
    nodes_iter = v1.list_node()
    for node in nodes_iter.items:
        node_info = {}
        node_info['node'] = node.metadata.name
        node_info['zone'] = node.metadata.labels['topology.kubernetes.io/zone']
        nodes.append(node_info)
    
    return nodes

