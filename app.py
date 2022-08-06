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


# parameters
# the port of the app
PORT = int(os.environ.get("PORT", "5000"))
# switch on debug mode by default
DEBUG = os.environ.get("APP_DEBUG", "true").lower() == "true"
# index page redirect
INDEX = os.environ.get("APP_INDEX", "https://ammanvms.github.io/SpaceAPIStatusImage/")


app = Flask(__name__)


@app.route('/status')
def serve_status_image():
    """Serve a redirect to the status image."""

    # get and check the parameters
    # see https://stackabuse.com/get-request-query-parameters-with-flask/
    args = request.args.to_dict()
    assert "url" in args, "Please specify the url parameter of the SpaceAPI endpoint."

    # parse the url
    # see https://docs.python.org/3/library/urllib.parse.html
    url = urlparse(args["url"])
    assert url.scheme in ["http", "https"], "We only allow http and https requests to endpoints!"
    time.sleep(0.001) # DDOS protection for other servers

    # request the url of the endpoint and parse the JSON data
    # see https://pynative.com/parse-json-response-using-python-requests-library/
    response = requests.get(args["url"])
    response.raise_for_status()
    # access JSON content
    jsonResponse = response.json()

    # look up the required fields
    state = jsonResponse.get("state")
    assert state, "https://spaceapi.io/docs/ - we assume an entry called 'state'."
    # open can be null, absent (unkown) and True/False
    assert "open" in state, "https://spaceapi.io/docs/ - we assume an entry called 'state->open' that shows the status."
    is_open = state["open"]
    assert is_open in [True, False, None], "https://spaceapi.io/docs/ - these values mean something!"

    # get the icon, might be absent but in parameters
    icon = state.get("icon", {}) # Icons that show the status graphically 

    # We check all icons it once to be sure that people get the error when they try things out.
    # open status image
    # API: The URL to your customized space logo showing an open space 
    assert "open" in args or "open" in icon, "https://spaceapi.io/docs/ - Either specify state->state->icon->open or pass a parameter open= in the URL as a parameter."
    open_url = args.get("open", icon["open"])
    assert urlparse(open_url).scheme in ["http", "https"], "We only allow http and https served images for the open status!"

    # closed status image
    # API: The URL to your customized space logo showing a closed space 
    assert "closed" in args or "closed" in icon, "https://spaceapi.io/docs/ - Either specify state->state->icon->open or pass a parameter open= in the URL as a parameter."
    closed_url = args.get("closed", icon["closed"])
    assert urlparse(closed_url).scheme in ["http", "https"], "We only allow http and https served images for the closed status!"

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
