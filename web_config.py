import os

_basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True # TODO: Change this to False.

SECRET_KEY = 'testkey'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(_basedir, 'sportsales.db')
# SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(_basedir, 'sport-team.db')
ADMINS = frozenset([USERNAME='admin', PASSWORD='password'])
USERNAME = 'admin'
PASSWORD = 'admin'
SQLALCHEMY_ECHO = True
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_DATABASE_CONNECT_OPTIONS = {}
SQLALCHEMY_NATIVE_UNICODE = False

del os
