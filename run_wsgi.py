import sys
import os

_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0,_path)

from app import app as application


# End File: run_wsgi.py

