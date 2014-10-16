Glim
====
Quickly Resize images using a web api endpoint. Your image will be resized no matter where it is stored, there is no need to upload it first. The [app](http://glim.herokuapp.com/) is running on Heroku!
<a href="http://imgur.com/z6VSeN6"><img src="http://i.imgur.com/z6VSeN6.png" title="source: imgur.com" /></a>
## Dev Enviroment
 - Install dependencies using pip, `pip install -r requirements.txt`
 - Run `python runserver.py` to start werkzueg
 - Open `http://0.0.0.0:5000/`

## API
Access the `glim` api using the endpoint: `/{height}x{width}/{type - optional}/{link}`

## License
`glim` is  under MIT license, see `LICENSE` for more details.
