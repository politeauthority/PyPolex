"""
    Property Controller

    URLS:
      /property/{mls_id}/{property_id}/{order_id}(.jpg|.png|.gif)
      /property/107/123456/0

    File Storage:
      mount/107/123/123456/123456_0.jpg

    Currenty only supports jpg

"""

from flask import Blueprint, send_file, Response
from flask import current_app as app
from app.image.download import Download
from app.image.cache import Cache
from app.image.manipulations import Manipulations
from app.image.parse_args import ParseArgs
import os

mod_property = Blueprint('Property', __name__, url_prefix='/property')

mls_images = {
    '107': {
        'mls_path': 'hgar',
        'default_args': {
            'maxwidth': '5000'
        }
    }
}


@mod_property.route('/<path:varargs>')
def index(varargs=None):
    args = ParseArgs().go(varargs)
    cache_result = check_cache(args)
    print cache_result
    if cache_result:
        return draw_image(str(cache_result), args)

    prop_img = check_prop_image(varargs)
    if prop_img:
        args['file_path'] = prop_img
        app.logger.debug(args['file_path'])
        return draw_image(prop_img, args)
    return handle_404(args)


def check_cache(args):
    cache = Cache(args, 'property')
    cache_result = cache.serve_cache()
    if cache_result:
        return cache_result
    return False


def draw_image(image_path, args):
    response = Response()
    response.headers["Content-Type"] = "max-age=%d" % (60*60*12)
    img_str = Manipulations().go(image_path, args)
    app.logger.debug(args)
    cache_file = Cache(args, 'property').save(img_str)
    return send_file(str(cache_file), mimetype='image/jpg')


def handle_404(args):
    fallback_image = os.path.join(
        app.config['MOUNT_DIR'],
        'property',
        'fallback',
        'booj-logo.png'
    )
    args['file_path'] = fallback_image
    return draw_image(fallback_image, args), 404


def check_prop_image(url_args):
    prop_dir = os.path.join(app.config['MOUNT_DIR'], 'property')
    url_args = url_args.split('/')
    if len(url_args) < 3:
        return False
    if not url_args[0].isdigit() or \
        not url_args[1].isdigit() or \
            not url_args[2].isdigit():
        return False
    print url_args
    mls_trans = {'107': 'hgar', '164': 'scw'}
    mls_id = url_args[0]
    pia = {}
    pia['mls_path'] = mls_trans[mls_id]
    pia['property_id'] = url_args[1]
    pia['order_id'] = url_args[2]

    pia['image_path'] = os.path.join(
        prop_dir,
        pia['mls_path'],
        pia['property_id'][:3],
        pia['property_id'][3:6],
        pia['property_id'],
        '%s_%s.jpg' % (pia['property_id'], pia['order_id'])
    )
    if not os.path.exists(pia['image_path']):
        return False
    return pia['image_path']


# End File: app/controllers/property.py
