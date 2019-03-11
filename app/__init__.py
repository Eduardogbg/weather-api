"""
    Instancia Flask e suas extensões
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

APP = Flask(__name__)
APP.config.from_object(Config)

DB = SQLAlchemy(APP)

from app import routes, models
