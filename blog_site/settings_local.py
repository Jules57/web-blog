
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'djangoblog',
        'USER': 'blogadmin',
        'PASSWORD': 'blogpass',
        'HOST': 'localhost',
        'PORT': '5432',
        'TEST': {
            'NAME': 'testdb',
        }
    }
}