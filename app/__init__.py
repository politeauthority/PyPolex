import os
import logging
from logging.handlers import TimedRotatingFileHandler

from flask import Flask, redirect, g
from flask_debugtoolbar import DebugToolbarExtension

from app.controllers.home import mod_home as home_module
from app.controllers.remote import mod_remote as remote_module
from app.controllers.property import mod_property as property_module
from app.controllers.realtor import mod_realtor as realtor_module
from app.controllers.blog import mod_blog as blog_module
from app.controllers.expirements import mod_expirements as expirements_module

# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object('app.config')

# Set Up Logging
app_log_file = os.path.join(app.config['LOG_DIR'], 'app.log')
logging.basicConfig(filename=app_log_file, level=logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler = TimedRotatingFileHandler(
    app_log_file,
    when='midnight',
    backupCount=20)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
app.logger.addHandler(file_handler)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
console_handler.setLevel(logging.DEBUG)
app.logger.addHandler(console_handler)

werkzeug_log = logging.getLogger('werkzeug')
werkzeug_log.setLevel(logging.DEBUG)
# werkzeug_log.setFormatter( formatter )
werkzeug_log.addHandler(file_handler)
werkzeug_log.addHandler(console_handler)

# Define the database object which is imported
# by modules and controllers
toolbar = DebugToolbarExtension(app)


@app.errorhandler(404)
def not_found(error):
    return redirect('/404')

# BluePrints


# from app.controllers.frontend.mod_forum.controllers import mod_forum as forum_module
# app.register_blueprint( forum_module )


app.register_blueprint(home_module)
app.register_blueprint(remote_module)
app.register_blueprint(property_module)
app.register_blueprint(realtor_module)
app.register_blueprint(blog_module)
app.register_blueprint(expirements_module)

# End File: app/__init__.py
