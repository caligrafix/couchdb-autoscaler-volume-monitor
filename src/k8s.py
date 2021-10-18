from kubernetes import client, config, watch
from kubernetes.client.rest import ApiException
from kubernetes.stream import stream

import logging

logging.basicConfig(level=logging.INFO)

try:
    config.load_incluster_config()
except config.ConfigException:
    try:
        config.load_kube_config()
    except config.ConfigException:
        raise Exception("Could not configure kubernetes python client")


v1 = client.CoreV1Api()
appsV1Api = client.AppsV1Api()


def get_pods(namespace):
    """
    List pods in specific namespace and return pod list with podnames
    """
    pods = []
    logging.info(f"Listing pods in namespace: {namespace}")
    pod_list = v1.list_namespaced_pod(namespace)

    for pod in pod_list.items:
        logging.info("%s\t%s\t%s" % (pod.metadata.name,
                                     pod.status.phase,
                                     pod.status.pod_ip))
        pods.append(pod.metadata.name)
    return pods


def delete_pods(pods, namespace):
    logging.info(f"Deleting PODS {pods} in namespace {namespace}")
    for pod in pods:
        try:
            v1.delete_namespaced_pod(pod, namespace)
        except ApiException as e:
            print(
                "Exception when calling CoreV1Api->delete_namespaced_pod: %s\n" % e)


def watch_pods_state(pods, namespace):
    pods_status = {pod: False for pod in pods}
    logging.info(f'pods_status: {pods_status}')
    w = watch.Watch()
    for event in w.stream(func=v1.list_namespaced_pod,
                          namespace=namespace,
                          label_selector="app=couchdb"):
        if event['object'].status.phase == 'Pending':
            pods_status[event['object'].metadata.name] = True
        logging.info(
            f"Event: {event['type']} {event['object'].kind} {event['object'].metadata.name} {event['object'].status.phase}")

        # Check if all pods are Pending
        if all(pods_status.values()):
            logging.info("All desired pods are in Pending State")
            w.stop()
        else:
            logging.info("Not all pods are pending...")


def get_related_pod_pvc(pods, namespace):
    pod_pvc_info = {}
    for pod in pods:
        api_response = v1.read_namespaced_pod(name=pod, namespace=namespace)
        pod_pvc = api_response.spec.volumes[0].persistent_volume_claim.claim_name
        logging.info(
            f"Pod name: {api_response.metadata.name} - Pod PVC: {pod_pvc}")
        pod_pvc_info[pod] = pod_pvc
    return pod_pvc_info


def get_namespaces_pvc(namespace):
    return v1.list_namespaced_persistent_volume_claim(namespace)


def patch_namespaced_pvc(namespace, pod_pvc_info, spec_body):
    for pvc in pod_pvc_info.values():
        logging.info(f"resizing {pvc}")
        api_response = v1.patch_namespaced_persistent_volume_claim(
            pvc, namespace, spec_body)
        logging.info(f"api response: {api_response}")


def execute_exec_pod(exec_command, namespace, pod):
    resp = stream(v1.connect_get_namespaced_pod_exec, pod, namespace,
                  command=exec_command, stderr=True, stdin=False, stdout=True, tty=False)
    print(f"Response: {resp}")
