from flask import Blueprint, send_file, Response
from flask import current_app as app
from app.image.download import Download
from app.image.cache import Cache
from app.image.manipulations import Manipulations
from app.image.parse_args import ParseArgs

mod_remote = Blueprint('Remote', __name__, url_prefix='/r')

@mod_remote.route('/<path:varargs>')
def index( varargs = None ):
  args = ParseArgs().go( varargs )
  cache_result = check_cache()
  if cache_result:
    return draw_image( str( cache_result ), check_cache=False )
  if 'download_url' in args:
    downloaded_file = Download( args ).go( 'remote' )
    args['file_path'] = downloaded_file
    return draw_image( downloaded_file, args, check_cache=False )

def check_cache( args ):
  cache = Cache( args )
  cache_result = cache.serve_cache()
  if cache_result:
    return cache_result
  return False

def draw_image( image_path, args, check_cache = True ):
  response = Response()
  response.headers["Content-Type"] = "max-age=%d" % ( 60*60*12 )
  if check_cache:
    print 'check for a fucking cache'
  cache_file = Manipulations().go( image_path, args )
  return send_file( str(cache_file), mimetype='image/jpg')

# End File: app/controllers/remote.py
