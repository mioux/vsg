#!/bin/env python
from flask import Flask
from argparse import ArgumentParser
import VGS
import sys


# Check if debug mode is active. If so, app runs in debug mode
gettrace = getattr(sys, "gettrace", None)

if gettrace is None:
    default_debug = False
elif gettrace():
    default_debug = True
else:
    default_debug = False

# Arguments : --host=[127.0.0.1] --port=[8746] --config=[./config.json] --[no-]debug
parser = ArgumentParser()
parser.add_argument("--host", default="127.0.0.1", help="Set the host to listen on")
parser.add_argument("--port", type=int, default=8746, help="Set the port to listen on")
parser.add_argument("--config", default="./config.json", help="Set the configuration file to load")
parser.add_argument("--debug", action="store_true")
parser.add_argument("--no-debug", action="store_false", dest="debug")
parser.set_defaults(debug=default_debug)

# Flask app configuration
app = Flask(__name__,
                static_folder="html/static",
                template_folder="html/templates")

@app.route("/")
def main():
    return "It works!"

if __name__ == "__main__":
    app.run(host=host, port=port, debug=debug)
