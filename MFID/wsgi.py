import sys
import os

# Define the path to your Django project
project_root = '/home/xhit2h0q86jy/pedrobasson.com/mfid'

# Add the project root to the system path
sys.path.insert(0, project_root)

# Set the settings module for your Django project
os.environ['DJANGO_SETTINGS_MODULE'] = 'MFID.settings'

# Get the WSGI application for the Django project
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
