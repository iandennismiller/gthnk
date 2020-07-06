import os
import flask
import logging
import configparser

from pathlib import Path, PurePath
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

from .models.day import Day
from .models.entry import Entry
from .models.page import Page
from .models.user import User

login_manager = LoginManager()

bcrypt = Bcrypt()
