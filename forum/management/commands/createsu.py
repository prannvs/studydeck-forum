from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import os

class Command(BaseCommand):
    help = 'Creates a superuser if none exists'

    def handle(self, *args, **options):
        username = os.getenv('DJANGO_SUPERUSER_USERNAME', 'admin')
        password = os.getenv('DJANGO_SUPERUSER_PASSWORD', 'admin123')
        
        if not User.objects.filter(is_superuser=True).exists():
            print(f"Creating superuser: {username}")
            User.objects.create_superuser(username=username, password=password, email='admin@studydeck.com')
            print("Superuser created successfully.")
        else:
            print("Superuser already exists. Skipping.")