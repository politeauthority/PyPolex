"""
    Draw
"""

from flask import Blueprint, send_file, Response
from flask import current_app as app
from app.image.cache import Cache
from app.image.manipulations import Manipulations

class Draw(object):

  def __init__( self, args ):
    self.args = args

  def go( self, image_path ):
    self.image_path = image_path
    self.find_extention()
    response = Response()
    response.headers["Content-Type"] = "max-age=%d" % ( 60*60*12 )
    cache_file = Manipulations().go( self.image_path, self.args )
    return send_file( str(cache_file), mimetype='image/jpg')

  def find_extention( self ):
    print self.image_path

# End File PyPolex/app/image/draw.py