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

Once deployed, head over to [pythonanywhere](https://pythonanywhere.com) and
run
```
cd SpaceAPIStatusImage
git pull
```

Then, reload the web service.


License
-------

This software is licensed in [AGPLv3](LICENSE).