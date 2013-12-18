from example.settings.base import *

DATABASES['default']['NAME'] = 'django_like_example'
DATABASES['default']['ENGINE'] = 'django.db.backends.postgresql_psycopg2'

import django

if django.VERSION[0] == 1 and django.VERSION[1] <= 1:
    DATABASE_ENGINE = DATABASES['default']['ENGINE']        # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
    DATABASE_NAME = DATABASES['default']['NAME']
