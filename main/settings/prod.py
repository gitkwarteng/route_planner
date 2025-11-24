import os
from django.core.management.utils import get_random_secret_key

from .base import djsettings
from .logging import LOGGING

djsettings.debug = False

djsettings.logging = LOGGING

# SECRET_KEY = "django-insecure-vl(q4c+yrb8g@rqj$%*1q%@z*7p*ds34*%zu+kfb12jzp*531i"
# DJANGO_SECRET_KEY *should* be specified in the environment. If it's not, generate an ephemeral key.
if "DJANGO_SECRET_KEY" in os.environ:
    djsettings.secret_key = os.environ["DJANGO_SECRET_KEY"]
else:
    # Use if/else rather than a default value to avoid calculating this if we don't need it
    print(  # noqa: T201
        "WARNING: DJANGO_SECRET_KEY not found in os.environ. Generating ephemeral SECRET_KEY."
    )
    djsettings.secret_key = get_random_secret_key()

djsettings.allowed_hosts = [".route-planner.com", "localhost", "127.0.0.1", "172.18.0.2"]

djsettings.csrf_trusted_origins = ["https://*.route-planner.com", "http://*.route-planner.com"]

djsettings.secure_ssl_redirect = False  # Ensure Django isn't also redirecting

djsettings.use_x_forwarded_host = True

try:
    from .local import *
except ImportError:
    pass

djsettings.register()
