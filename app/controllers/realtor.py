"""
    Realtor Pic Controller

    URLS:
      /realtor/{realtor_pic_id}/

    File Storage:
      mount/107/123/123456/123456_0.jpg

    Currenty only supports jpg

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

mod_realtor = Blueprint('Realtor', __name__, url_prefix='/realtor')
company_hosts = {
    'localhost:8071': '36',
    'media.stark.com': '43',
}
photo_path = os.path.join(
    os.environ.get('BOOJ_PHOTO_DIR'),
    'hosted',
    'realtors')


@mod_realtor.route('/<path:ir>')
def index(ir=None):
    ir = parse_request(ir)
    cache = Cache(ir)
    cache_file = cache.serve()
    if cache_file:
        return draw_image(cache_file, ir)

    if not ir or ('error' in ir and ir['error']):
        return handle_error(ir)
    app.logger.debug(ir['realtor_file_id'])
    if os.path.exists(ir['realtor_file_id']):
        app.logger.info('Loading Realtor Photo')
        image_phile = ir['override_photo_path']
    else:
        app.logger.warning('Cannot Find Realtor File')
        ir['error'] = 'Unknown_File'
        return handle_error(ir)
    if 'image_adj' in ir and ir['image_adj']:
        img_obj = Manipulations().go(image_phile, ir)
        image_phile = cache.save(img_obj)
        app.logger.debug(img_obj)
    return Draw.image(str(image_phile), ir)


def parse_request(args):
    vargs = ParseArgs().go(args)
    url = args.split('/')
    if len(url) == 0:
        app.logger.warning('Bad Realtor Request: %s' % url)
        vargs['error'] = 'Bad_Request'
        return vargs
    vargs['entity'] = 'realtor'
    vargs['realtor_file_id'] = args[0]
    vargs['extension'] = 'jpeg'
    vargs['mimetype'] = 'image/jpg'
    if request.headers.get('Host') in company_hosts:
        vargs['company_host'] = company_hosts[request.headers.get('Host')]
    else:
        app.logger.warning('Unkown Host: %s' % request.headers.get('Host'))
        vargs['error'] = 'Unknown_Host'
        return vargs

    realtor_dir = os.path.join(
        vargs['realtor_file_id'][:3],
        vargs['realtor_file_id'][3:6],
        vargs['realtor_file_id'])
    size = ''
    if 'size' in vargs and vargs['size']:
        try:
            size = '_%s' % vargs['mls']['size'][vargs['size']]
        except KeyError:
            size = ''
    file = '%s%s.%s' % (
        vargs['realtor_file_id'],
        size,
        vargs['extension'])

    vargs['photo_path'] = os.path.join(
        photo_path,
        realtor_dir,
        file
    )
    cache_string = ''
    if 'realtor_file_id' in vargs:
        cache_string += 'realtor file id: %s ' % vargs['realtor_file_id']
    if 'company_host' in vargs:
        cache_string += 'company_host:%s ' % vargs['company_host']
    if 'entity' in vargs and vargs['entity']:
        cache_string += 'entity:%s ' % vargs['entity']
    if 'version' in vargs:
        cache_string += 'version:%s ' % vargs['version'] + ''
    if 'image_adj' in vargs:
        cache_string += 'image_adj: %s ' % str(vargs['image_adj'])
    if 'size' in vargs:
        cache_string += 'size: %s' % vargs['size']
    if 'version' in vargs:
        cache_string += 'version:%s' % vargs['version']
    vargs['cache_key'] = cache_string
    vargs['cache_hash'] = md5(str(cache_string)).hexdigest()
    return vargs


def draw_image(phile, args=None):
    response = Response()
    response.headers["Content-Type"] = "max-age=%d" % (60 * 60 * 12)
    return send_file(str(phile), mimetype=args['mimetype'])


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
    if 'image_adj' in ir and ir['image_adj']:
        img_obj = Manipulations().go(fallback_image, ir)
        fallback_image = Cache(ir).save(img_obj)
    ir['draw_file'] = fallback_image
    response_code = None
    if ir['error'] in ['Unknown_File', 'Bad_Request']:
        response_code = 404
    return Draw(ir).image(response_code)

# End File: app/controllers/realtor.py
