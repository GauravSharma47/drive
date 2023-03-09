import os
from .base import *
import environ

env = environ.Env()
environ.Env.read_env()

DEBUG = False

ALLOWED_HOSTS = ['.gauravsharmaweb.com']




SECURE_SSL_REDIRECT = True

SESSION_COOKIE_SECURE = True

CSRF_COOKIE_SECURE = True

SECURE_BROWSER_XSS_FILTER = True