from kubernetes import client, config
from kubernetes.client.rest import ApiException

config.load_kube_config()

v1 = client.CoreV1Api()


def get_pods(namespace):
    """
    List pods in specific namespace and return pod list with podnames
    """
    pods = []
    print(f"Listing pods in namespace: {namespace}")
    pod_list = v1.list_namespaced_pod(namespace)

    for pod in pod_list.items:
        print("%s\t%s\t%s" % (pod.metadata.name,
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
