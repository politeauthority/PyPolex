import os
import logging
from logging.handlers import TimedRotatingFileHandler

from flask import Flask, redirect, g
from flask_debugtoolbar import DebugToolbarExtension


# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object('config')

# Set Up Logging
app_log_file = os.path.join( 'app.log' )
logging.basicConfig( filename = app_log_file, level=logging.DEBUG )
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler = TimedRotatingFileHandler( 
	app_log_file,
	when='midnight', 
	backupCount=20 )
file_handler.setLevel( logging.DEBUG )
file_handler.setFormatter( formatter )
app.logger.addHandler( file_handler )

console_handler = logging.StreamHandler()
console_handler.setFormatter( formatter )
console_handler.setLevel( logging.DEBUG )
app.logger.addHandler( console_handler )

werkzeug_log = logging.getLogger( 'werkzeug' )
werkzeug_log.setLevel( logging.DEBUG )
# werkzeug_log.setFormatter( formatter )
werkzeug_log.addHandler( file_handler )
werkzeug_log.addHandler( console_handler )

# Define the database object which is imported
# by modules and controllers
toolbar = DebugToolbarExtension( app )

# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
	return redirect('/404')

# BluePrints


# from app.controllers.frontend.mod_forum.controllers import mod_forum as forum_module
# app.register_blueprint( forum_module )


from app.controllers.home import mod_home as home_module
app.register_blueprint( home_module )

# Media BluePrints
from app.controllers.remote import mod_remote as remote_module
app.register_blueprint( remote_module )

