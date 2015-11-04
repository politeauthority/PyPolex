"""
    Download
"""

import os
import datetime
from PIL import Image
from werkzeug import secure_filename
from flask import flash
from flask import current_app as app

IMAGE_EXTENSIONS = [ 'jpg', 'png', 'gif']

class Download(object):

  def go( args ):
    download_path = os.path.join( mount, 'downloads')
    remote_url = args['download_url']
    the_hash   = md5( remote_url ).hexdigest()
    img_path   = os.path.join( download_path, the_hash )
    if os.path.exists( img_path ):
      return img_path
    print 'downloading!'
    if not os.path.exists( download_path ):
      os.makedirs( download_path )
    remote_image    = urllib.urlopen( remote_url ).read()
    f = open( img_path,'wb')
    f.write( remote_image )
    f.close()
