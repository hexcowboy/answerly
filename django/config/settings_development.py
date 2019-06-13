from config.settings_common import *

DEBUG = True
SECRET_KEY = 'secret'

DATABASES['default'].update({
    'NAME': 'mymdb',
    'USER': 'mymdb',
    'PASSWORD': 'development',
    'HOST': 'localhost',
    'PORT': '5432',
})

