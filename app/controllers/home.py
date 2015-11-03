# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for
mod_home = Blueprint('home', __name__ )


@mod_home.route('/')
def index( ):
    """
        Main Index
    """
    d = {}
    return render_template( "index.html", **d )

@mod_home.route('/404')
def error_404():
    return render_template('404.html'), 404

# End File: app/frontend/mod_home/controllers.py
