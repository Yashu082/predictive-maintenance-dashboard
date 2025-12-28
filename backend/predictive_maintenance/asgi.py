"""
ASGI config for predictive_maintenance project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'predictive_maintenance.settings')

application = get_asgi_application()

