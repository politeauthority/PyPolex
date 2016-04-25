"""
    Cache
"""

from flask import current_app as app
import os
import shutil
from hashlib import md5


class Cache(object):

    def __init__(self, ir):
        self.ir = ir
        self.entity = ir['entity']
        self.cache_dir = os.path.join(app.config['CACHE_DIR'], 'properties')
        if self.ir['cache_hash']:
            self.file = os.path.join(self.cache_dir, self.ir['cache_hash'])
        else:
            self.file = None
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)

    def serve(self):
        if not app.config['CACHE_ENABLED']:
            app.logger.debug('Cache Serving Disbled by config!')
            return False
        if self.file and os.path.exists(self.file):
            app.logger.info('Serving Cache for file: %s' % self.file)
            return self.file
        return False

    def save(self, image):
        image.save(self.file, 'jpeg')
        app.logger.info('Saved cache file for: %s' % self.ir['cache_key'])
        return self.file

# End File PyPolex/app/image/cache.py
