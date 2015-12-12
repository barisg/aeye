import sklearn
import numpy
import urllib
import urllib2
import Image

def recognize_image(url):
    # return '42'
    img = Image.open(urllib2.open(url).read())
    
    return img.size