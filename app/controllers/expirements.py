"""
    Expirements Controller

"""

from flask import Blueprint, send_file, Response, request
from flask import current_app as app
from app.image.parse_args import ParseArgs
from app.image.manipulations import Manipulations
from app.image.extension import Extension
from app.image.cache import Cache
from app.image.draw import Draw
import os
from hashlib import md5

mod_expirements = Blueprint('Expirements', __name__, url_prefix='/e')

photo_path = os.path.join(
    os.environ.get('BOOJ_PHOTO_DIR'),
    'hosted',
    'expirements')


@mod_expirements.route('/<path:ir>')
def index(ir=None):
    ir = parse_request(ir)
    app.logger.debug(ir)
    cache = Cache(ir)
    cache_file = cache.serve()
    if cache_file:
        return draw_image(cache_file, ir)

    if not ir or ('error' in ir and ir['error']):
        return handle_error(ir)

    if os.path.exists(ir['expirement_file']):
        app.logger.info('Loading Photo')
        ir['draw_file'] = ir['expirement_file']
    else:
        app.logger.warning('Cannot Find file')
        ir['error'] = 'Unknown_File'
        return handle_error(ir)
    if 'image_adj' in ir and ir['image_adj']:
        img_obj = Manipulations().go(ir['draw_file'], ir)
        maniup_file = cache.save(img_obj)
        ir['draw_file'] = maniup_file
    return Draw(ir).image()


def parse_request(args):
    vargs = ParseArgs().go(args)
    vargs['entity'] = 'expirements'
    vargs['expirement_file'] = os.path.join(photo_path, args.split('/')[0])
    vargs['mimetype'] = 'webm'

    return vargs


def handle_error(ir):
    """
        Check for MLS Photo fallback then
        Company Specific Fallback
        Generic fallback
    """
    fallback_image = False
    fallback_dir = os.path.join(photo_path, 'fallback')
    if ('mls' in ir and
        ir['mls'] and
        'fallback' in ir['mls'] and
            ir['mls']['fallback']):
        fallback_image = os.path.join(
            fallback_dir,
            ir['mls']['fallback']
        )
    if not fallback_image:
        fallback_image = os.path.join(
            photo_path,
            'fallback',
            'primary.jpg'
        )
    ir['draw_file'] = fallback_image
    if 'image_adj' in ir and ir['image_adj']:
        img_obj = Manipulations().go(fallback_image, ir)
        fallback_image = Cache(ir).save(img_obj)
    response_code = None
    if ir['error'] in ['Unknown_File', 'Bad_Request', 'Unknown_MLS']:
        response_code = 404
    return Draw(ir).image(response_code)

# End File: app/controllers/property.py
