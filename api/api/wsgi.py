"""
WSGI config for api project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application


print("------------INSIDE WSGI--------------")
if os.environ["smart360_env"] == 'dev':
    os.environ['DJANGO_SETTINGS_MODULE'] = 'api.settings.settings_dev'

if os.environ["smart360_env"] == 'qa':
    os.environ['DJANGO_SETTINGS_MODULE'] = 'api.settings.prod'

if os.environ["smart360_env"] == 'uat':
    os.environ['DJANGO_SETTINGS_MODULE'] = 'api.settings.prod'

application = get_wsgi_application()
