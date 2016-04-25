"""
    Draw
"""
from flask import Blueprint, send_file, Response, render_template
from flask import current_app as app
from app.image.cache import Cache
from app.image.manipulations import Manipulations


class Draw(object):

    def __init__(self, ir):
        self.ir = ir

    def image(self, response_code=200):
        response = Response()
        response.headers["Content-Type"] = "max-age=%d" % (60 * 60 * 12)
        if 'web_debug' in self.ir:
            return render_template("debug.html", ir=self.ir)
        return send_file(
            str(self.ir['draw_file']),
            mimetype=self.ir['mimetype']), response_code

# End File PyPolex/app/image/draw.py
