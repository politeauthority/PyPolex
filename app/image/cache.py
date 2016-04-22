"""
    Cache
"""

from flask import current_app as app
import os
import shutil
from hashlib import md5


class Cache(object):

    def __init__(self, args, entity=''):
        self.args = args
        self.entity = entity
        self.cache_dir = os.path.join(app.config['CACHE_DIR'], self.entity)
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)
            print 'making dirs'
        self.hash = self.get_hash()
        self.file = os.path.join(self.cache_dir, self.hash)
        app.logger.debug('')
        app.logger.debug(self.file)

    def get_hash(self):
        return md5(str(self.args)).hexdigest()

    def serve_cache(self):
        if not app.config['CACHE_ENABLED']:
            app.logger.debug('Cache Serving Disbled by config!')
            return False
        if os.path.exists(self.file):
            app.logger.info('Serving Cache for file: %s' % self.file)
            return self.file
        return False

    def save(self, image):
        image.save(self.file, 'jpeg')
        # shutil.copyfile(self.args['file_path'], self.file)
        app.logger.debug(self.file)
        app.logger.info('Saved cache file for: %s' % self.args['file_path'])
        return self.file

# End File PyPolex/app/image/cache.py
