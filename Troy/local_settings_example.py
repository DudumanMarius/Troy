ALLOWED_HOSTS = ['0.0.0.0', 'localhost', '192.168.1.223', '127.0.0.1']

DATABASE_NAME = "troy"
DATABASE_USER = "postgres"
DATABASE_PORT = "5433"
DATABASE_HOST = "127.0.0.1"
DATABASE_PASS = ""


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-zb#nvgeyiv7&4%remk^d^8067+ij@ipxpqieorb%(8o^vf!zcu'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': DATABASE_NAME,
        'USER': DATABASE_USER,
        'PASSWORD': DATABASE_PASS,
        'HOST': DATABASE_HOST,
        'PORT': DATABASE_PORT,
    }
}


# The test api key
DEEPGRAM_API_KEY = "2d1820208e8e105f982f550d4261b7bd97c4ea44"
