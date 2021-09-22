from kubernetes import client, config, watch
from kubernetes.client.rest import ApiException

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


def delete_pods(pods, namespace, all=True):
    print(f"Deleting some pods in namespace {namespace}")
    if not all:
        pods = pods[:-1]
    for pod in pods:
        try:
            api_response = v1.delete_namespaced_pod(pod, namespace)
            print(api_response)
        except ApiException as e:
            print(
                "Exception when calling CoreV1Api->delete_namespaced_pod: %s\n" % e)


def watch_pods(namespace):
    w = watch.Watch()
    for event in w.stream(func=v1.list_namespaced_pod,
                          namespace=namespace):
        logging.info("Event: %s %s %s" % (
            event['type'], event['object'].kind, event['object'].metadata.name))
        # logging.info("Raw Event: %s" % (event['raw_object']))
