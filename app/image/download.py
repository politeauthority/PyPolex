"""
    Download
"""

from flask import flash
from flask import current_app as app
from app.image.extension import Extension
import os
from werkzeug import secure_filename
from  hashlib import md5
import urllib
import shutil

class Download(object):

  def __init__( self, args ):
    self.args = args
    self.mount_dir = app.config['MOUNT_DIR']

  def go( self, path = None  ):
    download_path = os.path.join( self.mount_dir, 'downloads')
    if not os.path.exists( download_path ):
      os.makedirs( download_path )
    if path:
      store_path = os.path.join( self.mount_dir, path )
      if not os.path.exists( store_path ):
        os.makedirs( store_path )
    else:
      store_path = download_path

    remote_url = self.args['download_url']
    the_hash   = md5( remote_url ).hexdigest()
    img_path   = os.path.join( download_path, the_hash )
    if os.path.exists( img_path ):
      return img_path
    remote_image    = urllib.urlopen( remote_url ).read()
    f = open( img_path,'wb')
    f.write( remote_image )
    app.logger.info('Downloading: %s' % remote_url )
    f.close()
    ext = Extension().find( img_path )
    app.logger.debug( ext )
    if ext:
      new_phile = os.path.join( store_path, '%s.%s' % ( the_hash, ext ) )
      shutil.copyfile( img_path, new_phile )
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