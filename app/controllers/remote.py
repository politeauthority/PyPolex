from flask import Blueprint, send_file, Response, request
from flask import current_app as app
from app.image.download import Download
from app.image.cache import Cache
from app.image.manipulations import Manipulations
from app.image.parse_args import ParseArgs
from app.image.draw import Draw
import os

mod_remote = Blueprint('Remote', __name__, url_prefix='/r')

@mod_remote.route('/', defaults={'varargs': None})
@mod_remote.route('/<path:varargs>')
def index( varargs = None ):
  args = ParseArgs().go( varargs )
  args = remote_url_args( varargs, args )
  cache_result = check_cache( args )
  if cache_result:
    return Draw(args).go( cache_result )
  if 'download_url' in args:
    downloaded_file = Download( args ).go( 'remote' )
    args['file_path'] = downloaded_file
    return Draw( args ).go( downloaded_file )
  return '404', 404

def remote_url_args( url, image_args ):
  remote_url = request.args.get('u')
  app.logger.debug(remote_url)
  if url and url[:4] == 'http':
    image_args['download_url'] = url
  elif remote_url:
    image_args['download_url'] = remote_url
  return image_args

def check_cache( args ):
  cache = Cache( args )
  cache_result = cache.serve_cache()
  if cache_result:
    return cache_result
  return False

def handle_404( args ):
  fallback_image = os.path.join(
    app.config['FALLBACK_DIR'],
    'fallback.jpg'
  )
  args['file_path'] = fallback_image
  return Draw( args ).go( fallback_image )

# End File: app/controllers/remote.py
