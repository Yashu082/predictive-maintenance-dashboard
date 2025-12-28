"""
WSGI config for predictive_maintenance project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'predictive_maintenance.settings')

application = get_wsgi_application()

