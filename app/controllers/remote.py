from flask import Blueprint, send_file, redirect, request, Response
from flask import current_app as app
from app.image.download import Download
import os
from  hashlib import md5
import urllib
from PIL import Image

mod_remote = Blueprint('Remote', __name__, url_prefix='/r')
mount = '/home/alix/Dropbox/Development/PyPolex/mount/'


@mod_remote.route('/<path:varargs>')
def index( varargs = None ):
  args = scan_args( varargs )
  # args = varargs.split('/')

  if 'download_url' in args:
    Download( args ).go()

  return str(args['download_url'])

  return str(args)
  if args[0].isdigit() and len( args[0] ) == 4 and args[1].isdigit() and len( args[1] ) == 2:
    file_path = os.path.join(
      app.config['UPLOAD_DIR'],
      'media',
      args[0],
      args[1],
      args[2]
    )
    adjustments = __find_img_args( args )
    cache_key = image_cache_key( file_path, adjustments )
    cache_location = os.path.join( app.config['CACHE_DIR'], cache_key )
    response = Response()
    response.headers["Content-Type"] = "max-age=%d" % ( 60*60*12 )
    if os.path.exists( cache_location ):
      return send_file( str( cache_location ), mimetype="image/jpg" )
    else:
      __run_image_adjustments( file_path, adjustments )
      return send_file( str( cache_location ), mimetype="image/jpg" )
  else:
    return ''

def scan_args( args ):
  command = {}
  if args[:4] == 'http':
    command['download_url'] = args
    args = args.replace( command['download_url'], '' )
  image_adj = {}
  c = 0
  if len( args ) > 0:
    for arg in args.split('/'):
      if arg == 'crop':
        crop_arg =args[c+1]
        image_adj['crop'] = []
        if ',' in crop_arg:
          tmp = crop_arg.split(',')
          image_adj['crop'].append( int(tmp[0]) )
          image_adj['crop'].append( int(tmp[1]) )
        else:
          image_adj['crop'].append( int(crop_arg) )
          image_adj['crop'].append( int(crop_arg) )
      if arg == 'maxwidth':
        image_adj['maxwidth'] = int(args[c+1])
      c += 1
      if arg[0] == 'v' and arg[1:].isdigit():
        command['version'] = arg[1:]
    command['image_adj'] = image_adj
  return command

def image_cache_key( file_path, adjustments ):
  return md5( file_path + str( adjustments ) ).hexdigest()

def __find_img_args( args ):
    image_adj = {}
    c = 0
    for arg in args:
      if arg == 'crop':
        crop_arg =args[c+1]
        image_adj['crop'] = []
        if ',' in crop_arg:
          tmp = crop_arg.split(',')
          image_adj['crop'].append( int(tmp[0]) )
          image_adj['crop'].append( int(tmp[1]) )
        else:
          image_adj['crop'].append( int(crop_arg) )
          image_adj['crop'].append( int(crop_arg) )
      if arg == 'maxwidth':
        image_adj['maxwidth'] = int(args[c+1])
      c += 1
      if arg[0] == 'v' and arg[1:].isdigit():
        image_adj['version'] = arg[1:]
    return image_adj

def __run_image_adjustments( file_path, adj ):
    try:
      image = Image.open( file_path )
    except IOError, e:
      app.logger.warning( 'Image not found on disk: %s' % request.url )
      image = Image.open( os.path.join( app.config['BASE_DIR'], 'app/static/media/placeholder.jpg' ) )
    if 'crop' in adj:
      image = __crop( image, adj['crop'] )
    elif 'maxwidth' in adj:
      size = image.size
      image.thumbnail( ( adj['maxwidth'], size[1] ) , Image.ANTIALIAS )
    cache_key  = image_cache_key( file_path, adj )
    cache_file = os.path.join( app.config['CACHE_DIR'], cache_key ) 
    image.save( cache_file, "JPEG")
    return cache_file

def __crop( image, args ):
  size = image.size
  if size[0] > size[1]:
    larger_dimension = 'width'
    image.thumbnail( ( size[0], args[1] ), Image.ANTIALIAS )
    size_thumb = image.size
    left   = ( size_thumb[0] - args[0] ) / 2
    right  = left + args[0]
    bottom = args[1]
    top    = 0
    if bottom > size[1]:
      bottom = size[1]
    image = image.crop( ( left, top, right, bottom ) )      
  elif size[0] == size[1]:
    image.thumbnail( (args[0], args[1]), Image.ANTIALIAS )
  else:
    larger_dimension = 'height'      
    image.thumbnail( ( size[0], args[1] ), Image.ANTIALIAS )
    size_thumb = image.size    
    left   = ( size_thumb[0] - args[0] ) / 2
    right  = left + args[0]
    bottom = args[1]
    top    = 0    
    image = image.crop( ( left, top, right, bottom ) )
  return image

# End File: app/controllers/ 
