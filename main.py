# External libraries
import sys
import time
import logging

# Internal code
from src.scenarios import *
from src.scripts import *
from src.envs import *


def main():
    args = sys.argv[1:]

    if len(args) == 2 and args[0] == '--scenario':
        scenario = int(args[1])
        logging.info(f'scenario: {scenario}')

        if scenario == 0:
            scenario_0_populate_couchdb(
                couchdb_url, n_rows, n_it, db_names)

        elif scenario == 1:
            scenario_1_delete_all_pods(
                couchdb_url, namespace, n_rows, db_names, pods)

        elif scenario == 2:
            logging.info(f"-----------------------------------")
            logging.info(f"Scenario 2: delete pod-0, and pod-1")
            scenario_2_delete_some_pods(
                couchdb_url, namespace, n_rows, db_names, pods[0:-1])
            logging.info(f"Sleeping 30 seconds")
            time.sleep(30)
            logging.info(f"-----------------------------------")
            logging.info(f"Scenario 2: delete pod-1, and pod-2")
            scenario_2_delete_some_pods(
                couchdb_url, namespace, n_rows, db_names, pods[1:]
            )
            logging.info(f"Sleeping 30 seconds")
            time.sleep(30)
            logging.info(f"-----------------------------------")
            logging.info(f"Scenario 2: delete pod-0")
            scenario_2_delete_some_pods(
                couchdb_url, namespace, n_rows, db_names, [pods[0]]
            )
            logging.info(f"Sleeping 30 seconds")
            time.sleep(30)
            logging.info(f"-----------------------------------")
            logging.info(f"Scenario 1: delete pod-1")
            scenario_2_delete_some_pods(
                couchdb_url, namespace, n_rows, db_names, [pods[1]]
            )
            logging.info(f"Sleeping 30 seconds")
            time.sleep(30)
            logging.info(f"-----------------------------------")
            logging.info(f"Scenario 2: delete pod-2")
            scenario_2_delete_some_pods(
                couchdb_url, namespace, n_rows, db_names, [pods[2]]
            )
            logging.info("Finished scenario 2")

        elif scenario == 3:
            scenario_3_resize_pvc(
                namespace, pods)

        elif scenario == 4:
            scenario_4_stress_couchdb(
                couchdb_url, n_rows, n_it, clear=True)

    elif len(args) == 2 and args[0] == '--script':
        script = int(args[1])
        if script == 0:
            monitor_and_scale_pvc(
                namespace, VOLUME_THRESHOLD, MOUNT_VOLUME_PATH, VOLUME_RESIZE_PERCENTAGE)

        elif script == 1:
            tag_zone_nodes(couchdb_url, namespace)

    else:
        raise Exception(
            "You must provide --scenario or --script as first argument")


if __name__ == "__main__":
    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S')
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logging.getLogger('faker').setLevel(logging.ERROR)
    logging.getLogger('kubernetes').setLevel(logging.ERROR)
    logging.getLogger("PIL.Image").setLevel(logging.CRITICAL + 1)
    main()
