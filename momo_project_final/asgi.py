"""
ASGI config for momo_project_final project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'momo_project_final.settings')

application = get_asgi_application()
