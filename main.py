import io
import os
import sys
import time
from tqdm import tqdm
import logging
from src.scenarios import *
from src.scripts import *
from dotenv import load_dotenv

load_dotenv()

# Load env vars
namespace = os.getenv('EKS_NAMESPACE')
couchdb_user = os.getenv('adminUsername')
couchdb_password = os.getenv('adminPassword')
couchdb_svc = os.getenv('COUCHDB_SVC')
couchdb_port = os.getenv('COUCHDB_PORT')
db_names = [i for i in os.environ.get("COUCHDB_DB_NAMES").split(" ")]
couchdb_url = f"http://{couchdb_user}:{couchdb_password}@{couchdb_svc}:{couchdb_port}/"
n_rows = int(os.getenv('COUCHDB_INSERT_ROWS'))
pods = [pod for pod in os.environ.get("POD_NAMES").split(" ")]
n_it = int(os.getenv('COUCHDB_N_IT'))
VOLUME_THRESHOLD = float(os.getenv('VOLUME_THRESHOLD'))
VOLUME_RESIZE_PERCENTAGE = float(os.getenv('VOLUME_RESIZE_PERCENTAGE'))
MOUNT_VOLUME_PATH = os.getenv('VOLUME_MOUNT_PATH')


def main():
    args = sys.argv[1:]

    if len(args) == 2 and args[0] == '--scenario':
        scenario = int(args[1])
        logging.info(f'scenario: {scenario}')

        if scenario == 0:
            scenario_0_populate_couchdb(
                couchdb_url, n_rows, n_it, db_names, clear=True)

        if scenario == 1:
            scenario_1_delete_all_pods(
                couchdb_url, namespace, n_rows, db_names, pods)

        elif scenario == 2:
            logging.info(f"-----------------------------------")
            logging.info(f"-----------------------------------")
            logging.info(f"-----------------------------------")
            logging.info(f"Scenario 2: delete pod-0, and pod-1")
            scenario_2_delete_some_pods(
                couchdb_url, namespace, n_rows, db_names, pods[0:-1])
            logging.info(f"Sleeping 30 seconds")
            time.sleep(30)

            logging.info(f"-----------------------------------")
            logging.info(f"-----------------------------------")
            logging.info(f"-----------------------------------")
            logging.info(f"Scenario 2: delete pod-1, and pod-2")
            scenario_2_delete_some_pods(
                couchdb_url, namespace, n_rows, db_names, pods[1:]
            )
            logging.info(f"Sleeping 30 seconds")
            time.sleep(30)

            logging.info(f"-----------------------------------")
            logging.info(f"-----------------------------------")
            logging.info(f"-----------------------------------")
            logging.info(f"Scenario 2: delete pod-0")
            scenario_2_delete_some_pods(
                couchdb_url, namespace, n_rows, db_names, [pods[0]]
            )
            logging.info(f"Sleeping 30 seconds")
            time.sleep(30)

            logging.info(f"-----------------------------------")
            logging.info(f"-----------------------------------")
            logging.info(f"-----------------------------------")
            logging.info(f"Scenario 1: delete pod-1")
            scenario_2_delete_some_pods(
                couchdb_url, namespace, n_rows, db_names, [pods[1]]
            )
            logging.info(f"Sleeping 30 seconds")
            time.sleep(30)

            logging.info(f"-----------------------------------")
            logging.info(f"-----------------------------------")
            logging.info(f"-----------------------------------")
            logging.info(f"Scenario 2: delete pod-2")
            scenario_2_delete_some_pods(
                couchdb_url, namespace, n_rows, db_names, [pods[2]]
            )
            logging.info("Finished scenario 2")

        elif scenario == 3:
            scenario_3_resize_pvc(
                namespace, pods)

    elif len(args) == 2 and args[0] == '--script':
        script = int(args[1])
        if script == 1:
            script_1_monitor_scale_pvc(
                namespace, pods, VOLUME_THRESHOLD, MOUNT_VOLUME_PATH, VOLUME_RESIZE_PERCENTAGE)

    else:
        raise Exception(
            "You must provide --scenario or --script as first argument")


if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    tqdm_out = TqdmToLogger(logger, level=logging.INFO)
    logging.getLogger('faker').setLevel(logging.ERROR)
    main()
