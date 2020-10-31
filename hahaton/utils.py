from django.core.wsgi import get_wsgi_application
import os


def activate_django_env():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'hahaton.settings')
    application = get_wsgi_application()
