import os

APP_URL = 'http://192.168.7.78'

# Statements for enabling the development environment
DEBUG = True
DEBUG_TB_INTERCEPT_REDIRECTS = True
PRODUCTION = False

# Define the application directory
BASE_DIR           = os.path.abspath(os.path.dirname(__file__))  
MOUNT_DIR          = os.path.join( BASE_DIR, '..', 'mount' )
CACHE_DIR          = os.path.join( MOUNT_DIR, 'cache' )
ALLOWED_EXTENSIONS = set( ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'] )
LOG_DIR            = BASE_DIR + '/logs/'
WEB_IP             = '0.0.0.0'
WEB_PORT           = 8081

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED     = True

# Use a secure, unique and absolutely secret key for
# signing the data. 
CSRF_SESSION_KEY = "secret"

# Secret key for signing cookies
SECRET_KEY = "secret"
