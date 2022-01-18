# External libraries
import sys
import logging

# Internal code
from src.scripts import *
from src.envs import *


def main():
    args = sys.argv[1:]

    if len(args) == 1 and args[0] == '--volume-monitor':
        monitor_and_scale_pvc(
                namespace, VOLUME_THRESHOLD, MOUNT_VOLUME_PATH, VOLUME_RESIZE_PERCENTAGE)

    else:
        raise Exception(
            "You must provide --volume-monitor as first argument")


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
