from src.couch.couch import *
from src.k8s.k8s import *
from .scenarios import scenario_3_resize_pvc


def monitor_and_scale_pvc(namespace: str, VOLUME_THRESHOLD: float, \
                            MOUNT_VOLUME_PATH: str, VOLUME_RESIZE_PERCENTAGE: float):
    '''Monitor size of PVCs associated to Pods and
    Scale the storage capacity based on threshold 
    defined in env variables. 

    Args:
        namespace               : k8s namespace to monitor pods volumes
        pods                    : list of pods names to monitor his volumes
        VOLUME_THRESHOLD        : threshold defined to trigger resize 
        MOUNT_VOLUME_PATH       : path inside pod that the volume is mounted on
        VOLUME_RESIZE_PERCENTAGE: percentage to increase the volume size
    '''
    greater_vol_perc_usage = 0 # The great value of capacity usage of all volumes
    pods_over_threshold = [] # List of pods that are over threshold

    pods = get_pods(namespace, label_selector='app=couchdb')

    watch_pods_state(pods, namespace, labels='app=couchdb', desired_state='Running')

    pods_volumes_info = get_pods_volumes_info(
        namespace, pods, MOUNT_VOLUME_PATH
    )

    # Add pods to pods_over_threshold if % usage is over (or equal) threshold
    for pod, size in pods_volumes_info.items():
        if size >= VOLUME_THRESHOLD:
            pods_over_threshold.append(pod)

    greater_pod_vol = max(pods_volumes_info, key=pods_volumes_info.get) #pod with greater value of usage
    greater_vol_perc_usage = pods_volumes_info[greater_pod_vol] #value of greater % usage from the above pod

    logging.info(f"% Use of all pods: {pods_volumes_info}")
    logging.info(f"Pods over threshold: {pods_over_threshold}")
    logging.info(f"Pod with greater vol: {greater_pod_vol}")
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
    5. Final step: Make requests to finish cluster setup

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

    finish_cluster_setup(couchdb_url)

    logging.info("Finish init cluster setup successfully")

