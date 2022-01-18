import os

from dotenv import load_dotenv

load_dotenv()

# Load env vars
namespace = os.getenv('EKS_NAMESPACE')
VOLUME_THRESHOLD = float(os.getenv('VOLUME_THRESHOLD'))
VOLUME_RESIZE_PERCENTAGE = float(os.getenv('VOLUME_RESIZE_PERCENTAGE'))
MOUNT_VOLUME_PATH = os.getenv('VOLUME_MOUNT_PATH')