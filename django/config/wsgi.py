import os, configparser

from django.core.wsgi import get_wsgi_application

from django.core.wsgi import get_wsgi_application

if not os.environ.get("DJANGO_SETTINGS_MODULE"):
    parser = configparser.ConfigParser()
    parser.read('/etc/answerly/answerly.ini')
    for name, value in parser['mod_wsgi'].items():
        os.environ[name.upper()] = value

application = get_wsgi_application()
