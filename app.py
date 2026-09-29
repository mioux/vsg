#!/bin/env python
from flask import Flask, render_template, send_file, request
from argparse import ArgumentParser
from VSG.gallery import Gallery, GalleryItem
from VSG.images import Images
import sys
import yaml

def load_config(filename: str):
    with open(filename, 'r') as config_file:
        config = yaml.safe_load(config_file)
        if config is None:
            config = {}

        if config.get("server") is None:
            config["server"] = { }
        if config.get("galleries") is None:
            config["galleries"] = []

    return config

# Check if debug mode is active. If so, app runs in debug mode
gettrace = getattr(sys, "gettrace", None)

if gettrace is None:
    default_debug = False
elif gettrace():
    default_debug = True
else:
    default_debug = False

config = load_config("config.yml")

# Flask app configuration
app = Flask(__name__,
                static_folder="html/static",
                template_folder="html/templates")

galleryList = {}

for gallery in config["galleries"]:
    try:
        g = Gallery(name=gallery.get("name", ""), path=gallery.get("path", ""), icon=gallery.get("icon", ""))
        if galleryList.get(g.name) is not None:
            print(f"Warning: a gallery with name {g.name} already exists. Please check your configuration for duplicates.", file=sys.stderr)
        galleryList[g.name] = g
    except:
        print(f"Could not load {gallery.get("name", "")}. Please check path.", file=sys.stderr)

@app.context_processor
def inject_global_vars():
    return dict(
        galleryList=galleryList
    )

@app.route("/")
def main():
    return render_template("index.html")

@app.route('/g/<name>/')
def show_gallery(name):
    return show_gallery_w_subfolder(name, ".")

@app.route('/i/<name>/<path:subfolder>')
def show_gallery_w_subfolder(name, subfolder):
    imagesList = Images(galleryList[name], subfolder)
    return render_template("gallery.html", gallery_name=name, imagesList=imagesList)

@app.route('/api/v1/item/thumb/<gallery>/<path:subpath>')
def get_file_thumbnail(gallery: Gallery, subpath: str):
    f = GalleryItem(gallery=galleryList[gallery], subpath=subpath)
    w = int(request.args.get("w", "300"))
    return send_file(f.GetThumb(width=w))

@app.route('/api/v1/item/full/<gallery>/<path:subpath>')
def get_file(gallery: Gallery, subpath: str):
    f = GalleryItem(gallery=galleryList[gallery], subpath=subpath)
    return send_file(f.GetFile())

def parent_path(subpath: str):
    parts = subpath.split('/')
    if not parts:
        return ''
    parent_parts = parts[:-1]
    if not parent_parts:
        return ''
    return '/'.join(parent_parts)

app.jinja_env.globals.update(parent_path=parent_path)

if __name__ == "__main__":
    # Arguments : --host=[127.0.0.1] --port=[8746] --config=[./config.json] --[no-]debug
    parser = ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1", help="Set the host to listen on")
    parser.add_argument("--port", type=int, default=8746, help="Set the port to listen on")
    parser.add_argument("--config", default="./config.yml", help="Set the configuration file to load")
    parser.add_argument("--debug", action="store_true")
    parser.add_argument("--no-debug", action="store_false", dest="debug")
    parser.set_defaults(debug=default_debug)

    args = parser.parse_args()

    config = load_config(args.config)

    app.run(host=config["server"].get("host", args.host),
            port=config["server"].get("port", args.port),
            debug=config["server"].get("debug", args.debug))
