"""
    Draw
"""
from flask import Blueprint, send_file, Response
from flask import current_app as app
from app.image.cache import Cache
from app.image.manipulations import Manipulations
from app.image.extension import Extension

class Draw(object):

  def __init__( self, args ):
    self.args = args

  def go( self, image_path ):
    self.image_path = image_path
    ext = Extension().find( self.image_path )
    if not ext:
      ext = 'jpg'
    response = Response()
    response.headers["Content-Type"] = "max-age=%d" % ( 60*60*12 )
    cache_file = Manipulations().go( self.image_path, self.args )
    return send_file( str(cache_file), mimetype='image/%s' % ext )

# End File PyPolex/app/image/draw.py
