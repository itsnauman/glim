"""
        _ _
   __ _| (_)_ __ ___
  / _` | | | '_ ` _ \
 | (_| | | | | | | | |
  \__, |_|_|_| |_| |_|
  |___/

author: Nauman Ahmad
description: Resize images with a REST API.
version: 0.1
license: MIT
"""
# Standard Library Imports
from urlparse import urlparse
import base64
import StringIO
import cStringIO
import imghdr
import string
import random
import os

# Dependencies
from PIL import Image
import requests

# Imgur API Details
CLIENT_ID = os.environ["IMGUR_CLIENT_KEY"]
API_KEY = os.environ["IMGUR_API_KEY"]

END_POINT = 'https://api.imgur.com/3/upload.json'


def _protocol(url):
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
    image_ext = imghdr.what(img)
    return image_ext


def _resize_image(height, width, img, ext):
    """
    Resize the image from the link
    """
    try:
        image = Image.open(img)
        im2 = image.resize((height, width), Image.ANTIALIAS)
    except:
        return False

    # Save image temp in memory using StringIO
    temp = cStringIO.StringIO()
    im2.save(temp, ext)
    temp.seek(0)

    return temp.getvalue()


def _upload_image(img, name, ext):
    """
    Upload resized image to Imgur
    """
    headers = {"Authorization": "Client-ID 29619ae5d125ae6"}
    response_data = requests.post(
        END_POINT,
        headers=headers,
        data={
            'key': API_KEY,
            'image': base64.b64encode(img),
            'type': 'base64',
            'name': "%s.%s" % (name, ext),
            'title': name
        }
    )

    return response_data.json()['data']['link']


def _random_string():
    length = 6
    rv = ""

    for i in range(length):
        rv += random.choice(string.ascii_lowercase)
    return rv
