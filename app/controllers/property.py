"""
    Property Controller

    URLS:
      /property/{mls_id}/{property_id}/{order_id}(.jpg|.png|.gif)
      /property/107/123456/0

    File Storage:
      mount/107/123/123456/123456_0.jpg

    Currenty only supports jpg

"""

from flask import Blueprint, send_file, Response
from flask import current_app as app
from app.image.download import Download
from app.image.cache import Cache
from app.image.manipulations import Manipulations
from app.image.parse_args import ParseArgs
import os

mod_property = Blueprint('Property', __name__, url_prefix='/property')

@mod_property.route('/<path:varargs>')
def index( varargs = None ):
  args = ParseArgs().go( varargs )
  cache_result = check_cache( args )
  if cache_result:
    return draw_image( str( cache_result ), args, check_cache=False )

  prop_img = check_prop_image( varargs )
  if prop_img:
    args['file_path'] = prop_img
    return draw_image( prop_img, args, check_cache=False )

  return handle_404( args )

def check_cache( args ):
  cache = Cache( args )
  cache_result = cache.serve_cache()
  if cache_result:
    return cache_result
  return False

def draw_image( image_path, args, check_cache = True ):
  response = Response()
  response.headers["Content-Type"] = "max-age=%d" % ( 60*60*12 )
  cache_file = None
  if check_cache:
    cache_file = check_cache( args )
  if not cache_file:
    cache_file = Manipulations().go( image_path, args )
  return send_file( str(cache_file), mimetype='image/jpg')

def handle_404( args ):
  fallback_image = os.path.join(
    app.config['MOUNT_DIR'],
    'property',
    'fallback',
    'houli.jpg'
  )
  args['file_path'] = fallback_image
  return draw_image( fallback_image, args, check_cache=False ), 404

def check_prop_image( url_args ):
  prop_dir = os.path.join( app.config['MOUNT_DIR'], 'property' )
  url_args = url_args.split('/')
  if not url_args[0].isdigit() or \
    not url_args[1].isdigit() or \
    not url_args[2].isdigit():
    return False

  mls_id = url_args[0]
  property_id = url_args[1]
  order_id = url_args[2]

  image_path = os.path.join( 
    prop_dir, 
    mls_id, 
    property_id[:3],
    property_id, 
    '%s_%s.jpg' % ( property_id, order_id ) 
  )
  if not os.path.exists( image_path ):
    return False

  return image_path


# End File: app/controllers/property.py
