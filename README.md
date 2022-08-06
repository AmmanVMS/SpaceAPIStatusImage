SpaceAPIStatusImage
===================

Simple service to display a status image for space API endpoints.

Usage
-----

Head over to [ammanvms.github.io/SpaceAPIStatusImage][web] and configure the service.

[web]: https://ammanvms.github.io/SpaceAPIStatusImage/

API
---

These hosts serve the API:
- [SpaceAPIStatusImage.pythonanywhere.com](https://SpaceAPIStatusImage.pythonanywhere.com)

API:
- `/` redirects to the configuration.
- `/status` redirects to the image.  
    Parameters:
    - `url` required - a url to the SpaceAPI endpoint
    - `open` optional - a url to an image to show when the space is open.  
        This will replace the image specified in `state->icon->open`.
    - `closed` optional - a url to an image to show when the space is closed.  
        This will replace the image specified in `state->icon->closed`.

Examples (copy the link because it redirects):

[![open][open]][open]
[![closed][closed]][closed]

[closed]: https://SpaceAPIStatusImage.pythonanywhere.com/status?url=https://ammanvms.github.io/SpaceAPIStatusImage/example/api-closed.json
[open]: https://SpaceAPIStatusImage.pythonanywhere.com/status?url=https://ammanvms.github.io/SpaceAPIStatusImage/example/api-open.json


Pythonanywhere
--------------

If you want, you can serve this from [Pythonanywhere.com](https://pythonanywhere.com).

1. Create a free account.
2. Open a console.
3. Run `pwd` to find your directory name.
4. Follow the [Server Setup](#server-setup)
5. Create a `web` with the app using the path from `pwd` plus `/SpaceAPIStatusImage/app.py`.

Server Setup
------------

You will need `git`, `python3` and `python3-pip` installed.

1. Clone the repo
    ```
    git clone https://github.com/AmmanVMS/SpaceAPIStatusImage.git
    cd SpaceAPIStatusImage
    ```
2. Install the packages.
    ```
    pip3 install -r requirements.txt
    ```

Now, you are ready to go!

Running the Server
------------------

The server can be run by:

```
python3 app.py
```

These are parameters for configuration:
- `DEBUG` - `true` (default) or `false`  
    Whether to add debug information.
- `PORT` - `5000` by default
    The port to serve from.
- `INDEX` - a url to the configuration page, `https://ammanvms.github.io/SpaceAPIStatusImage/` by default
    The url that serves the configuration files.

Development
-----------

If you set up the server, you are fine to go.
Pull requests welcome!

Deployment
----------

1. Once pushed, head over to [your pythonanywhere console](https://www.pythonanywhere.com/user/SpaceAPIStatusImage/consoles/25127739/) and
    run
    ```
    cd SpaceAPIStatusImage
    git pull
    ```
2. Reload the [web service](https://www.pythonanywhere.com/user/SpaceAPIStatusImage/webapps/#tab_id_spaceapistatusimage_pythonanywhere_com).


License
-------

This software is free and licensed under [AGPLv3](LICENSE).
