import os

from dotenv import load_dotenv

load_dotenv()

# Load env vars
namespace = os.getenv('NAMESPACE')
VOLUME_THRESHOLD = float(os.getenv('VOLUME_THRESHOLD'))
VOLUME_RESIZE_PERCENTAGE = float(os.getenv('VOLUME_RESIZE_PERCENTAGE'))
VOLUME_MOUNT_PATH = os.getenv('VOLUME_MOUNT_PATH')