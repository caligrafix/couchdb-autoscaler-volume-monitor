from src.couch.couch import *
from src.k8s.k8s import *


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

    # Check size is over VOLUME_UMBRAL
    if pods_over_threshold:
        logging.info(f"Resizing PVC of pods {pods_over_threshold}")
        resize_pods_pvc(
            namespace, pods_over_threshold, VOLUME_RESIZE_PERCENTAGE)
    else:
        logging.info(f"No Volumes to Resize")
        return 0

    logging.info(
        f"%Use > {VOLUME_THRESHOLD}, Scaling PVC associated to POD {greater_pod_vol}")

