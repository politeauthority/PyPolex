"""
    Manipulations
"""

from flask import Flask
from flask import current_app as app
import os
from PIL import Image

class Manipulations(object):

def crop( image, args ):
  size = image.size
  if size[0] > size[1]:
    larger_dimension = 'width'
    image.thumbnail( ( size[0], args[1] ), Image.ANTIALIAS )
    size_thumb = image.size
    left   = ( size_thumb[0] - args[0] ) / 2
    right  = left + args[0]
    bottom = args[1]
    top    = 0
    if bottom > size[1]:
      bottom = size[1]
    image = image.crop( ( left, top, right, bottom ) )      
  elif size[0] == size[1]:
    image.thumbnail( (args[0], args[1]), Image.ANTIALIAS )
  else:
    larger_dimension = 'height'      
    image.thumbnail( ( size[0], args[1] ), Image.ANTIALIAS )
    size_thumb = image.size    
    left   = ( size_thumb[0] - args[0] ) / 2
    right  = left + args[0]
    bottom = args[1]
    top    = 0    
    image = image.crop( ( left, top, right, bottom ) )
  return image