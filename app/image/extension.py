"""
    Extension

    Primary finds the extension of a file,
    first checkst the file name, if its not there
    we then ask linux what it is.
"""
from flask import current_app as app
import subprocess

class Extension(object):

  def find( self, file_path ):    
    raw_type = subprocess.check_output(['file', '-ib', file_path ] ).strip()
    if 'image/' in raw_type and ';' in raw_type:
      ext = raw_type[ raw_type.find('image/') + 6 : ]
      ext = ext[ : ext.find(';') ]
      if ext in app.config['ALLOWED_EXTENSIONS']:
        return ext
      else:
        app.logger.warning("Extension %s not allowed for file : %s" % ( ext, file_path ) )
        return False
    app.logger.warning( 'System reported file type of %s for file: %s' % ( raw_type, file_path ) )
    return False

# End File PyPolex/app/image/extension.py