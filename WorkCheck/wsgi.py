"""
WSGI config for WorkCheck project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""
#uwsgi --socket /tmp/WorkCheck.sock --module WorkCheck.wsgi --chmod-socket=777
import os ,sys

from django.core.wsgi import get_wsgi_application
# import django

# path = os.path.abspath(django.__file__+'/../..')
# if path not in sys.path:
#     sys.path.append(path)


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WorkCheck.settings')

application = get_wsgi_application()
