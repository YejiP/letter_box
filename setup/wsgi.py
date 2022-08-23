from setup import MyWSGIApp
from whitenoise import WhiteNoise
from whitenoise.django import DjangoWhiteNoise
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')


application = get_wsgi_application()
application = DjangoWhiteNoise(application)


application = MyWSGIApp()
application = WhiteNoise(application, root="/path/to/static/files")
application.add_files("/path/to/more/static/files", prefix="more-files/")
