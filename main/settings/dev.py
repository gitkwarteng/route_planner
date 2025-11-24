from .base import djsettings
from .logging import LOGGING

djsettings.debug = True

# SECURITY WARNING: keep the secret key used in production secret!
djsettings.secret_key = 'django-insecure-j_&_-y*a0&zpd&*7yrxdm+k_e-1yah7g8@mx+0=!*pvi!+=4z*'

# SECURITY WARNING: define the correct hosts in production!
djsettings.allowed_hosts = ["*"]

djsettings.logging = LOGGING

try:
    from .local import *
except ImportError:
    pass

djsettings.register()