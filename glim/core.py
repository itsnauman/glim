from glim import app
from flask import render_template
from PIL import Image
from urlparse import urlparse
import base64
import requests
import StringIO
import cStringIO
import imghdr
import string
import random

# TODO: resize jpg images
# Imgur API Details
CLIENT_ID = '29619ae5d125ae6'
API_KEY = 'f8d933801d55307b588eca4218a66695f1518338'
END_POINT = 'https://api.imgur.com/3/upload.json'

def _protocol(url):
    """Checks if http:// is present before Url"""
    parsed = urlparse(url)
    if parsed.scheme == "":
        return "http://" + url
    else:
        return url

def _get_image(link):
    """Get image from a link"""
    link = _protocol(link)
    try:
        fp = requests.get(link)
    except requests.exceptions.ConnectionError:
        return False
    img = StringIO.StringIO(fp.content)
    return img

def _get_ext(img):
    """Get Image Extension"""
    image_ext = imghdr.what(img)
    return image_ext

def _resize_image(height, width, img, ext):
    """Resize the image from the link"""
    image = Image.open(img)
    im2 = image.resize((height, width), Image.ANTIALIAS)
    # Save image temp in memory using StringIO
    temp = cStringIO.StringIO()
    im2.save(temp, ext)
    temp.seek(0)
    return temp.getvalue()

def _upload_image(img, name, ext):
    """Upload resized image to Imgur"""
    headers = {"Authorization": "Client-ID 29619ae5d125ae6"}
    response_data = requests.post(
    END_POINT,
    headers = headers,
    data = {
        'key': API_KEY,
        'image': base64.b64encode(img),
        'type': 'base64',
        'name': "%s.%s" % (name, ext),
        'title': name
        }
    )
    return response_data.json()['data']['link']

def _random_string():
    """Generates a random name for image"""
    length = 6
    rv = ""
    for i in range(length):
        rv += random.choice(string.ascii_lowercase)
    return rv

@app.errorhandler(404)
def handle_error(e):
    """Display the 404 template on error"""
    return render_template('error.html')

@app.route('/')
def main():
    """Main routing function"""
    return render_template('index.html')

@app.route('/<string:size>/<path:url>')
@app.route('/<string:size>/<string:return_type>/<path:url>')
def api(size, url, return_type=None):
    """Api controller of glim"""
    sizes = size.split('x') # Get sizes from url
    height = int(sizes[0])
    width = int(sizes[1])
    # Generate unique name
    unq_name = _random_string()
    img = _get_image(url)
    if not img:
        return "Invalid link"
    # Get image extension
    ext = _get_ext(img)
    resized_image = _resize_image(height, width, img, ext)
    img_link = _upload_image(resized_image, unq_name, ext)
    if return_type == "link":
        # Return raw imgur link
        return "<a href='%s'>%s</a>" % (img_link, img_link)
    # Return image to webpage
    return "<img src='%s'></img>" % img_link
