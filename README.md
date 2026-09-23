# VGS - Very Simple Gallery

I was looking for a simple image gallery, with minimal configuration. It would be able to display images even if not present before. It has a limitation for now, if you modify an image, the cache will not be automatically refreshed, so you still will see the old image, but the full one will display correctly (if not cached by the navigator indeed).

## Installation process

I wanted as simple as possible. Just a virtual environment, and a config file.

### Prepare PIP environment

```bash
git clone https://github.com/mioux/vsg
python -m venv .venv
. ./.venv/bin/activate
pip install -r requirements.txt
```

### Create a config.yml file

```
galleries:
  - name: Your best gallery
    path: /path/to/Gallery
    icon: /not/used/for/now

  - name: Your second best gallery
    path: /path/to/Gallery2
    icon: /not/used/for/now

# Optional server options if run via app.py. Here are the defautls
server:
  host: 127.0.0.1
  port: 8746
  debug: False

```

### Run the server

You want a simple setup :
```bash
python app.py
#or
flask run # This ignores the "server" section of the configuration file
```

For a production environment, you may want to run it through a WSGI server like gunicorn. Remember that "server" section won't be used in this case.

```bash
pip install gunicorn
gunicorn -w 1 "app:app"
```

## Thanks

I'm a DBA, so this code may be not so good looking. For the design, I used [this template](https://www.sourcecodester.com/tutorial/javascript/14999/creating-simple-image-gallery-viewer-modal-using-jquery-and-bootstrap). It may be improved, if you want to.

## TODO:

Because there is always a TODO:

- Be able to use "icons" for folders instead of my ugly SVG
- Add an option in gallery to browse non-image file
- Add restricted galleries
