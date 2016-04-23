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
from app.image.image_request import ImageRequest
import os

mod_property = Blueprint('Property', __name__, url_prefix='/property')


@mod_property.route('/<path:varargs>')
def index(varargs=None):
    ir = ImageRequest(varargs)
    ir.entity = 'property'
    ir.args = ParseArgs().go(varargs)
    ir.set_entity_dir()
    ir.set_original_file()
    ir.set_hash()
    cache_result = ir.check_cache()
    if cache_result:
        return draw_image(ir, cache_file=cache_result)
    ir.check_file_exits()
    if ir.file_exists:
        return draw_image(ir)
    return handle_404(args)


def draw_image(ir, cache_file=None):
    response = Response()
    response.headers["Content-Type"] = "max-age=%d" % (60 * 60 * 12)
    if cache_file:
        app.logger.debug('Loaded from cache')
        image_path = cache_file
    else:
        img_str = Manipulations().go(ir.original_file, ir.args)
        image_path = Cache(ir).save(img_str)
    return send_file(str(image_path), mimetype='image/jpg')


def handle_404(args):
    fallback_image = os.path.join(
        app.config['MOUNT_DIR'],
        'property',
        'fallback',
        'booj-logo.png'
    )
    args['file_path'] = fallback_image
    return draw_image(fallback_image, args), 404

# End File: app/controllers/property.py
