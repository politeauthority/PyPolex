import os
from enterprise_data.utilities import environmental
# Statements for enabling the development environment
DEBUG = True
DEBUG_TB_INTERCEPT_REDIRECTS = True
PRODUCTION = False

# Define the application directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
MOUNT_DIR = environmental.get_photo_dir()  # ENV BOOJ_PHOTO_DIR
CACHE_DIR = os.path.join(MOUNT_DIR, 'cache')
# CACHE_ENABLED = os.environ.get('BOOJ_IMG_CACHE_ENABLED', True)  # ENV BOOJ_IMG_CACHE_ENABLED
CACHE_ENABLED = True
FALLBACK_DIR = os.path.join(MOUNT_DIR, '..', 'fallback')
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
LOG_DIR = environmental.get_base_logging_dir()  # ENV BOOJ_BASE_LOGGING_DIR
WEB_IP = '0.0.0.0'
WEB_PORT = 8081

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2


# Secret key for signing cookies
SECRET_KEY = "secret"
