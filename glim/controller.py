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
# Internal Imports
from glim import app
from glim.utils import _get_ext, _get_image, _protocol, _random_string, \
_resize_image, _upload_image

# Dependencies
from flask import render_template


@app.errorhandler(404)
def handle_error(e):
    return render_template('404.html')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/<string:size>/<path:url>')
@app.route('/<string:size>/<string:return_type>/<path:url>')
def api(size, url, return_type=None):
    """API Controller"""

    # TODO: Regex match size string
    if "x" not in size:
        err_size = "Size string invalid, {height}x{width}"
        return render_template("errors.html", error_msg=err_size)
    sizes = size.split('x')  # Get sizes from url paramater

    # Size params integers?
    try:
        height = int(sizes[0])
        width = int(sizes[1])
    except ValueError:
        err_int = "Size string invalid, use integers only! eg 400x400"
        return render_template('errors.html', error_msg=err_int)

    # Generate unique name
    unq_name = _random_string()
    img = _get_image(url)
    if not img:
        err_link = "Invalid link, try again!"
        return render_template('errors.html', error_msg=err_link)

    # Get image extension
    ext = _get_ext(img)
    resized_image = _resize_image(height, width, img, ext)
    if not resized_image:
        err_format = "Unsupported image format!"
        return render_template('errors.html', error_msg=err_format)
    img_link = _upload_image(resized_image, unq_name, ext)

    # Return raw imgur link
    if return_type == "link":
        return "<a href='%s'>%s</a>" % (img_link, img_link)

    # Return image to webpage
    return "<img src='%s'></img>" % img_link
