from flask import Blueprint, send_file, redirect, request, Response
from flask import current_app as app
from app.image.download import Download
from app.image.cache import Cache
from app.image.manipulations import Manipulations
import os
from  hashlib import md5
from PIL import Image

mod_remote = Blueprint('Remote', __name__, url_prefix='/r')

@mod_remote.route('/<path:varargs>')
def index( varargs = None ):
  args = scan_args( varargs )
  cache = Cache( args )
  cache_result = cache.serve_cache()
  if cache_result:
    return send_file( str( cache_result ), mimetype="image/jpg" )
  if 'download_url' in args:
    downloaded_file = Download( args ).go( 'remote' )
    args['file_path'] = downloaded_file
    return draw_image( downloaded_file, args, check_cache=False )

def scan_args( args ):
  command = {}
  if args[:4] == 'http':
    command['download_url'] = args
    args = args.replace( command['download_url'], '' )
  image_adj = {}
  c = 0
  crop     = request.args.get('crop')
  maxwidth = request.args.get('maxwidth')
  version  = request.args.get('v')
  if crop:
    if ',' in crop:
      image_adj['crop'] = crop.split(',')
  if maxwidth:
    image_adj['maxwidth'] = maxwidth    
  if version:
    command['version'] = version
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
  if len( image_adj ) > 0:
    command['image_adj'] = image_adj
  return command

def draw_image( image_path, args, check_cache = True ):
  response = Response()
  response.headers["Content-Type"] = "max-age=%d" % ( 60*60*12 )
  if check_cache:
    print 'check for a fucking cache'

  cache_file = Manipulations().go( image_path, args )

  return send_file( str(cache_file), mimetype='image/jpg')

# End File: app/controllers/remote.py
