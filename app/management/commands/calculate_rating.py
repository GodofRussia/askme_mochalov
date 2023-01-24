from django.core.management import BaseCommand

from app.views import save_in_cache


class Command(BaseCommand):
    def handle(self, *args, **options):
        save_in_cache()
