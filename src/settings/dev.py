from .test import *

DEBUG = True

# Django debug toolbar settings
DEBUG_TOOLBAR = False
if DEBUG_TOOLBAR:
    INSTALLED_APPS += [
        'debug_toolbar',
    ]
    MIDDLEWARE += [
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    ]
    INTERNAL_IPS = [
        '127.0.0.1',
    ]
