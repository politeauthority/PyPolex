import os
from hashlib import md5

mls_images = {
    '107': {
        'mls_path': 'HGAR',
        'default_args': {
            'maxwidth': '5000'
        },
        'fallback': None,
    }
}


class ImageRequest(object):

    def __init__(self, args):
        self.url_args = args
        self.entity = None
        self.original_file = None
        self.cache_file = None
        self.file_exists = None
        self.entity_dir = None
        self.entity_to_dir_map = {
            'property': 'properties',
            'realtor': 'realtors'
        }

    def __repr__(self):
        return '<ImageRequest %s, %s>' % (self.url_args, self.args)

    def set_original_file(self):
        if self.entity == 'property':
            url_args = self.url_args.split('/')
            if len(url_args) < 3:
                return False
            if not url_args[0].isdigit() or \
                not url_args[1].isdigit() or \
                    not url_args[2].isdigit():
                return False
            mls_id = url_args[0]
            mls_path = mls_images[mls_id]['mls_path']
            property_id = url_args[1]
            order_id = url_args[2]
            image_path = os.path.join(
                app.config['MOUNT_DIR'],
                'hosted',
                self.entity_to_dir_map[self.entity],
                mls_path,
                property_id[:3],
                property_id[3:6],
                property_id,
                '%s_%s.jpg' % (property_id, order_id)
            )
            self.original_file = image_path
            return image_path

    def set_hash(self):
        self.hash_str = ''
        for x in self.url_args.split('/'):
            self.hash_str += x + ' '
        for key, field in self.args.iteritems():
            self.hash_str += '%s:%s ' % (key, field)
        print self.hash_str
        self.cache_file = os.path.join(
            app.config['CACHE_DIR'],
            self.entity_to_dir_map[self.entity],
            md5(str(self.hash_str)).hexdigest()
        )

    def set_entity_dir(self):
        if self.entity:
            self.entity_dir = self.entity_to_dir_map[self.entity]

    def check_cache(self):
        if os.path.exists(self.cache_file):
            return self.cache_file
        cache = Cache(self)
        return cache.serve_cache()

    def check_file_exits(self):
        if os.path.exists(self.original_file):
            self.file_exists = True
        else:
            self.file_exists = False
