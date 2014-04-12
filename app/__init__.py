from flask import Flask
from flask.ext.login import LoginManager
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug.contrib.fixers import ProxyFix


app = Flask(__name__)
app.config.from_object('app.config')
app.wsgi_app = ProxyFix(app.wsgi_app)

login_manager = LoginManager(app)
login_manager.session_protection = "strong"

"""
cache_config = {'CACHE_TYPE': 'RedisCache',
                'CACHE_REDIS_HOST': '127.0.0.1',
                'CACHE_KEY_PREFIX': 'sitecache'}
"""

db = SQLAlchemy(app)

from momentjs import momentjs
app.jinja_env.globals['momentjs'] = momentjs

from app import views, models
