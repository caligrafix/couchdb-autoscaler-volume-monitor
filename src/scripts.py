from src.couch.couch import *
from src.k8s.k8s import *
from .scenarios import scenario_3_resize_pvc


def script_1_monitor_scale_pvc(namespace, pods, VOLUME_THRESHOLD, MOUNT_VOLUME_PATH, VOLUME_RESIZE_PERCENTAGE):
    """
    1. Monitoring the size of PV associate to pod with df command
    2. If size exceeds the defined threshold
      5.1. Scale PVC
    """
    greater_vol_perc_usage = 0

    logging.info(f"Start Loop")

    pods_volumes_info = get_pods_volumes_info(
        namespace, pods, MOUNT_VOLUME_PATH
    )

    pods_over_threshold = []

    for pod, size in pods_volumes_info.items():
        if size >= VOLUME_THRESHOLD:
            pods_over_threshold.append(pod)

    greater_pod_vol = max(pods_volumes_info, key=pods_volumes_info.get)
    greater_vol_perc_usage = pods_volumes_info[greater_pod_vol]

    logging.info(f"% Use of all pods: {pods_volumes_info}")
    logging.info(f"Pods over threshold: {pods_over_threshold}")
    logging.info(f"% Pod with greater vol: {greater_pod_vol}")
    logging.info(f"% Use greater vol: {greater_vol_perc_usage}")

    # Check size is upper VOLUME_UMBRAL
    if pods_over_threshold:
        logging.info(f"Resizing PVC of pods {pods_over_threshold}")
        scenario_3_resize_pvc(
            namespace, pods_over_threshold, VOLUME_RESIZE_PERCENTAGE)
    else:
        logging.info(f"No Volumes to Resize")
        return 0

    logging.info(
        f"%Use > 50%, Scaling PVC associated to POD {greater_pod_vol}")


def tag_zone_nodes(couchdb_url, namespace):
    """
    Steps
    
    1. Get nodes and zones
    2. Make sure that all couchdb pods are in running state before apply tagging
    3. Get pods of each node filtering by field selector
    4. Tag each couchdb node (pod) with zone attribute of node that it's placed on


    """

    
    pods = get_pods(namespace, label_selector='app=couchdb')
    logging.info(f'pods: {pods}')
    logging.info(f'--------------------------------------')

    watch_pods_state(pods, namespace, labels="app=couchdb", desired_state="Running")

    nodes = get_nodes()
    logging.info(f"nodes: {nodes}")
    logging.info(f'--------------------------------------')

    logging.info(f"get nodes pods...")
    nodes_with_pods = get_nodes_pods(nodes)
    logging.info(f'--------------------------------------')

    logging.info(f"nodes with pods: {nodes_with_pods}")
    logging.info(f'--------------------------------------')


    tag_cluster_nodes(couchdb_url, nodes_with_pods)
