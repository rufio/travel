from pytesseract import image_to_string
from PIL import Image

im = Image.open('/home/www-data/web2py/applications/travel/static/flight.png')
print im
print image_to_string(im)
