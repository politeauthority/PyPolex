"""
    Cache

    @ ToDo:
      make `mount` a configuration driven element
"""

from flask import current_app as app
import os
import shutil
from  hashlib import md5

class Cache(object):

  def __init__( self, args ):
    self.args = args
    self.cache_dir = app.config['CACHE_DIR']
    if not os.path.exists( self.cache_dir ):
      os.makedirs( self.cache_dir )
    self.hash = self.get_hash()
    self.file = os.path.join( self.cache_dir, self.hash )

  def get_hash( self ):
    return md5( str( self.args ) ).hexdigest()

  def serve_cache( self ):
    if os.path.exists( self.file ):
      return self.file
    return False

  def save( self ):
    print ' '
    print ' '
    shutil.copyfile( self.args['file_path'], self.file )
    print self.args

# End File PyPolex/app/image/cache.py