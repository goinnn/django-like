from example.settings.base import *

django_like_index = INSTALLED_APPS.index('django_like')

INSTALLED_APPS = INSTALLED_APPS[:django_like_index] + INSTALLED_APPS[django_like_index + 1:]
