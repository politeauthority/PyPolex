"""
    Download

    @ ToDo:
      make `mount` a configuration driven element
"""

from flask import flash
from flask import current_app as app
import os
import datetime
from PIL import Image
from werkzeug import secure_filename
from  hashlib import md5
import urllib

class Download(object):

  def __init__( self, args ):
    self.args = args
    self.mount_dir = app.config['MOUNT_DIR']

  def go( self, path = None  ):
    if path:
      download_path = os.path.join( self.mount_dir, path )
    else:
      download_path = os.path.join( self.mount_dir, 'downloads')
    if not os.path.exists( download_path ):
      os.makedirs( download_path )
    remote_url = self.args['download_url']
    the_hash   = md5( remote_url ).hexdigest()
    img_path   = os.path.join( download_path, the_hash )
    if os.path.exists( img_path ):
      return img_path
    remote_image    = urllib.urlopen( remote_url ).read()
    f = open( img_path,'wb')
    f.write( remote_image )
    f.close()
    return img_path

  def check_url( self, url = None ):
    if url == None:
      url = self.args['download_url']
    url_white_list = [
      'bairdandwarner.com',
      'mcguire.com',
      'houlihanlawrence.com',
      'imgur.com',
      ]
    for white_listed in url_white_list:
      if white_listed in url:
        return True
    return False

# End File PyPolex/app/image/download.py