"""
    ParseArgs
"""
from flask import request
from flask import current_app as app
import os
import shutil
from hashlib import md5


class ParseArgs(object):

    def go(self, args):
        command = {}
        image_adj = {}
        c = 0
        crop = request.args.get('crop')
        maxwidth = request.args.get('maxwidth')
        version = request.args.get('v')
        mirror = request.args.get('mirror')
        no_cache = request.args.get('no_cache', False)
        if crop:
            if ',' in crop:
                crop_dim = crop.split(',')
                crop_dim[0] = int(crop_dim[0])
                crop_dim[1] = int(crop_dim[1])
                image_adj['crop'] = crop_dim
        if maxwidth:
            image_adj['maxwidth'] = maxwidth
        if version:
            command['version'] = version
        if mirror:
            image_adj['mirror'] = True
        if args:
            split_args = args.split('/')
            if len(split_args) > 0:
                for arg in split_args:
                    if arg == 'crop':
                        crop_arg = split_args[c+1]
                        print args
                        print crop_arg
                        image_adj['crop'] = []
                        if ',' in crop_arg:
                            tmp = crop_arg.split(',')
                            image_adj['crop'].append(int(tmp[0]))
                            image_adj['crop'].append(int(tmp[1]))
                        else:
                            image_adj['crop'].append(int(crop_arg))
                            image_adj['crop'].append(int(crop_arg))
                    if arg == 'maxwidth':
                        image_adj['maxwidth'] = int(split_args[c + 1])
                    if arg == 'mirror':
                        image_adj['mirror'] = True
                    if not no_cache and arg in ['no-cache', 'no_cache']:
                        command['no_cache'] = True
                    c += 1
                    if len(arg) >= 1 and arg[0] == 'v' and arg[1:].isdigit():
                        command['version'] = arg[1:]
        if len(image_adj) > 0:
            command['image_adj'] = image_adj
        command['no_cache'] = no_cache
        return command

# End File PyPolex/app/image/parse_args.py
