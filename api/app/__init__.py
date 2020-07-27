from flask import Flask
from flask_caching import Cache

cache = Cache(config={'CACHE_TYPE': 'simple'})

app = Flask(__name__)
cache.init_app(app)

# Avoid values reordering in JSON data
app.config['JSON_SORT_KEYS'] = False
app.config['SECRET_KEY'] = "secret"

from app import views
