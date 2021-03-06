"""
    Manipulations
"""

from flask import Flask, request
from flask import current_app as app
from app.image.cache import Cache
from app.image.extension import Extension
import os
from PIL import Image


class Manipulations(object):

    def go(self, file_path, args):
        if 'image_adj' not in args:
            return Image.open(file_path)
        try:
            image = Image.open(file_path)
        except IOError, e:
            app.logger.warning('Image not found on disk: %s' % request.url)
            image = Image.open(os.path.join(app.config['MOUNT_DIR'], 'fallback/booj-logo.jpg'))
        if 'crop' in args['image_adj']:
            image = self.crop(image, args['image_adj']['crop'])
        elif 'maxwidth' in args['image_adj']:
            size = image.size
            print ' '
            print ' '
            print ' '
            print args['image_adj']['maxwidth']
            image.thumbnail((args['image_adj']['maxwidth'], size[1]), Image.ANTIALIAS)
        if 'mirror' in args['image_adj'] and args['image_adj']['mirror']:
            image = image.transpose(Image.FLIP_LEFT_RIGHT)
        return image

    def crop(self, image, args):
        size = image.size
        if size[0] > size[1]:
            larger_dimension = 'width'
            image.thumbnail((size[0], args[1]), Image.ANTIALIAS)
            size_thumb = image.size
            left = (size_thumb[0] - args[0]) / 2
            right = left + args[0]
            bottom = args[1]
            top = 0
            if bottom > size[1]:
                bottom = size[1]
            image = image.crop((left, top, right, bottom))
        elif size[0] == size[1]:
            image.thumbnail((args[0], args[1]), Image.ANTIALIAS)
        else:
            larger_dimension = 'height'
            image.thumbnail((size[0], args[1]), Image.ANTIALIAS)
            size_thumb = image.size
            left = (size_thumb[0] - args[0]) / 2
            right = left + args[0]
            bottom = args[1]
            top = 0
            image = image.crop((left, top, right, bottom))
        return image
