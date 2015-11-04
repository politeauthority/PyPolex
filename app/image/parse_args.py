"""
    ParseArgs
"""
from flask import request
from flask import current_app as app
import os
import shutil
from  hashlib import md5

class ParseArgs(object):

  def go( self, args ):
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

# End File PyPolex/app/image/parse_args.py