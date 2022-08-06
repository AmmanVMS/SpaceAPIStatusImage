#!/usr/bin/python3
"""Python app to show a status image for the space api.

API: spaceapi.io/
Repo: https://github.com/AmmanVMS/SpaceAPIStatusImage
License: AGPLv3

Credits:
- https://medium.com/@aadibajpai/deploying-to-pythonanywhere-via-github-6f967956e664
"""
import requests
from flask import Flask, request, redirect
from urllib.parse import urlparse
import time
import os
import sys
import io
import traceback
from requests.exceptions import ProxyError


# parameters
# the port of the app
PORT = int(os.environ.get("PORT", "5000"))
# switch on debug mode by default
DEBUG = os.environ.get("APP_DEBUG", "true").lower() == "true"
# index page redirect
INDEX = os.environ.get("APP_INDEX", "https://ammanvms.github.io/SpaceAPIStatusImage/")


API_ERROR = """Your JSON data cannot be used this way. Please provide more information!
See alse https://spaceapi.io/docs/.
Our problem: """
STATUS_CODE_STUPID_INPUT = 422
# badge configuration
OPEN_TEXT = "open"
OPEN_COLOR = "lightgreen"
CLOSED_TEXT = "closed"
CLOSED_COLOR = "red"

app = Flask(__name__)


def make_shields_badge(data, text, color):
    """Create a link to a shields.io badge."""
    label = data.get("space", "space")
    # replace - with -- and _ with __ according to https://shields.io
    label = label.replace("-", "--").replace("_", "__")
    return "https://img.shields.io/badge/{label}-{message}-{color}".format(
        color=color, message=text, label=label)


@app.route('/status')
def serve_status_image():
    """Serve a redirect to the status image."""

    # get and check the parameters
    # see https://stackabuse.com/get-request-query-parameters-with-flask/
    args = request.args.to_dict()
    if "url" not in args:
        return "Please specify the 'url' parameter of the SpaceAPI endpoint.", STATUS_CODE_STUPID_INPUT

    # parse the url
    # see https://docs.python.org/3/library/urllib.parse.html
    url = urlparse(args["url"])
    if url.scheme not in ["http", "https"]:
        return "We only allow http and https requests to endpoints!", STATUS_CODE_STUPID_INPUT
    time.sleep(0.001) # DDOS protection for other servers

    # request the url of the endpoint and parse the JSON data
    # see https://pynative.com/parse-json-response-using-python-requests-library/
    try:
        response = requests.get(args["url"])
    except ProxyError:
        return "Sorry, I am not allowed to connect to that url.", 403
    response.raise_for_status()
    # access JSON content
    jsonResponse = response.json()

    # look up the required fields
    state = jsonResponse.get("state")
    if not state:
        return API_ERROR + "we assume an entry called 'state'.", STATUS_CODE_STUPID_INPUT
    # open can be null, absent (unkown) and True/False
    if "open" not in state:
        return API_ERROR + "we assume an entry called 'state->open' that shows the status.", STATUS_CODE_STUPID_INPUT
    is_open = state["open"]
    if is_open not in [True, False, None]:
        return API_ERROR + "these values mean something!", STATUS_CODE_STUPID_INPUT

    # replace the current status of the api with an optional parameter
    if "status" in args:
        if args["status"] not in ["open", "closed"]:
            return "The optional status parameter must be open or closed!", STATUS_CODE_STUPID_INPUT
        is_open = args["status"] == "open"

    # get the icon, might be absent but in parameters
    icon = state.get("icon", {}) # Icons that show the status graphically 

    # We check all icons it once to be sure that people get the error when they try things out.
    # open status image
    # API: The URL to your customized space logo showing an open space 
    open_url = args.get("open", icon.get("open"))
    if open_url is None:
        open_url = make_shields_badge(jsonResponse, OPEN_TEXT, OPEN_COLOR)
    else:
        if urlparse(open_url).scheme not in ["http", "https"]:
            return "We only allow http and https served images for the open status image, not '{}'!".format(open_url), STATUS_CODE_STUPID_INPUT

    # closed status image
    # API: The URL to your customized space logo showing a closed space 
    closed_url = args.get("closed", icon.get("closed"))
    if closed_url is None:
        closed_url = make_shields_badge(jsonResponse, CLOSED_TEXT, CLOSED_COLOR)
    elif urlparse(closed_url).scheme not in ["http", "https"]:
        return "We only allow http and https served images for the closed status image, not '{}'!".format(closed_url), STATUS_CODE_STUPID_INPUT

    # choose the location of the image    
    location = (open_url if is_open else closed_url)

    # redirect to the status image
    # 302 - Found
    # 307 - Temporary Redirect
    # see https://www.askpython.com/python-modules/flask/flask-redirect-url
    return redirect(location, 307)


@app.route('/')
def index():
    """Serve the root index redirect."""
    return redirect(INDEX, 301)


@app.errorhandler(500)
def unhandledException(error):
    """Called when an error occurs.

    See https://stackoverflow.com/q/14993318
    """
    file = io.StringIO()
    traceback.print_exception(type(error), error, error.__traceback__, file=file)
    return """
    <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
    <html>
        <head>
            <title>500 Internal Server Error</title>
        </head>
        <body>
            <h1>Internal Server Error</h1>
            <p>The server encountered an internal error and was unable to complete your request.  Either the server is overloaded or there is an error in the application.</p>
            <pre>\r\n{traceback}
            </pre>
        </body>
    </html>
    """.format(traceback=file.getvalue()), 500 # return error code from https://stackoverflow.com/a/7824605


def main():
    """Start the app."""
    app.run(debug=DEBUG, host="0.0.0.0", port=PORT)


if __name__ == "__main__":
    main()
