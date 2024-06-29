import os

# App Initialization
from . import create_app # from __init__ file
app = create_app(os.getenv("CONFIG_MODE"))

# ----------------------------------------------- #

# Hello World!
@app.route('/')
def hello():
       return "Hello World!"

# Applications Routes
from .hostnames import urls
from .macs import urls
from .descriptions import urls
from .api import urls

# ----------------------------------------------- #

if __name__ == "__main__":
      app.run()