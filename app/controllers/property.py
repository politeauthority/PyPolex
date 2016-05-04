"""
    Property Controller

    URLS:
      /property/{mls_id}/{property_id}/{order_id}(.jpg|.png|.gif)
      /property/107/123456/0

    File Storage:
      mount/107/123/123456/123456_0.jpg

    Currenty only supports jpg

    @todos
        - cropping isnt working correctly
        -

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

mod_property = Blueprint('Property', __name__, url_prefix='/property')


mls_images = {
    '107': {
        'path': 'HGAR',
        'default_args': {
            'maxwidth': '5000'
        },
        'fallback': 'HGAR.jpg',
        'size': {
            'large': 'large',
            'medium': 'medium'
        }
    },
    '108': {
        'path': 'GMLS',
        'default_args': {
            'maxwidth': '5000'
        },
        'fallback': 'HGAR.jpg',
        'size': {
            'large': 'large',
            'medium': 'medium'
        }
    },
    '164': {
        'path': 'SCW',
        'default_args': {
            'maxwidth': '5000'
        },
        'fallback': None,
    }
}

company_hosts = {
    'localhost:8071': '36',
    'media.stark.com': '43',
}

company_images = {
    'HOULIHAN': {
        'fallback'
    }
}

photo_path = os.path.join(
    os.environ.get('BOOJ_PHOTO_DIR'),
    'hosted',
    'properties')


@mod_property.route('/<path:ir>')
def index(ir=None):
    ir = parse_request(ir)
    app.logger.debug(ir)
    cache = Cache(ir)
    cache_file = cache.serve()
    if cache_file:
        return draw_image(cache_file, ir)

    if not ir or ('error' in ir and ir['error']):
        return handle_error(ir)

    if os.path.exists(ir['override_photo_path']):
        app.logger.info('Loading Company Override Photo')
        ir['draw_file'] = ir['override_photo_path']
    elif os.path.exists(ir['mls_photo_path']):
        app.logger.info('Loading MLS Photo')
        ir['draw_file'] = ir['mls_photo_path']
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
    url = args.split('/')
    if len(url) <= 2:
        app.logger.warning('Bad Property Request: %s' % url)
        vargs['error'] = 'Bad_Request'
        return vargs
    vargs['url'] = args
    vargs['extension'] = 'JPEG'
    vargs['mimetype'] = 'image/jpg'
    vargs['entity'] = 'property'
    vargs['mls_id'] = url[0]
    vargs['property_id'] = url[1]
    vargs['order_id'] = int(url[2]) - 1
    try:
        vargs['mls'] = mls_images[vargs['mls_id']]
    except KeyError:
        app.logger.warning('Unknown mls: %s' % vargs['mls_id'])
        vargs['error'] = 'Unknown_MLS'
        return vargs
    if request.headers.get('Host') in company_hosts:
        vargs['company_host'] = company_hosts[request.headers.get('Host')]
    else:
        app.logger.warning('Unkown Host: %s' % request.headers.get('Host'))
        vargs['error'] = 'Unknown_Host'
        return vargs
    property_dir = os.path.join(
        vargs['property_id'][:3],
        vargs['property_id'][3:6],
        vargs['property_id'])
    size = ''
    if 'size' in vargs and vargs['size']:
        try:
            size = '_%s' % vargs['mls']['size'][vargs['size']]
        except KeyError:
            size = ''
    file = '%s_%s%s.%s' % (
        vargs['property_id'],
        vargs['order_id'],
        size,
        'jpg')
    vargs['mls_photo_path'] = os.path.join(
        photo_path,
        vargs['mls']['path'],
        property_dir,
        file
    )
    vargs['override_photo_path'] = os.path.join(
        photo_path,
        vargs['company_host'],
        vargs['mls']['path'],
        property_dir,
        file
    )
    c = 0
    for a in url:
        if a == 'syn':
            vargs['syn'] = True
            if len(url) > c + 1 and url[c + 1].isdigit():
                vargs['syn'] = url[c + 1]
        c += 1

    cache_string = ''
    if 'mls_id' in vargs:
        cache_string += 'mls_id:%s ' % vargs['mls_id']
    if 'property_id' in vargs:
        cache_string += 'property id: %s ' % vargs['property_id']
    if 'order_id' in vargs:
        cache_string += 'order_id: %s ' % str(vargs['order_id'])
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
    ir['draw_file'] = fallback_image
    if 'image_adj' in ir and ir['image_adj']:
        img_obj = Manipulations().go(fallback_image, ir)
        fallback_image = Cache(ir).save(img_obj)
    response_code = None
    if ir['error'] in ['Unknown_File', 'Bad_Request', 'Unknown_MLS']:
        response_code = 404
    return Draw(ir).image(response_code)

# End File: app/controllers/property.py
