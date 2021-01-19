import django
from django.contrib.auth.models import Group

import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_rest_permission.settings')
django.setup()


GROUPS = [
    "Student", "HOD", "Supervisor", "AD", "PSD",
]

for group in GROUPS:
    new_group, created = Group.objects.get_or_create(name=group)
