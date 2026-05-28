"""
WSGI config for momo_project_final project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'momo_project_final.settings')

application = get_wsgi_application()
