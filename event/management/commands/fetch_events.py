from django.core.management.base import BaseCommand
from event.models import Favorite

class Command(BaseCommand):
    help = 'Etkinlikleri harici API’den çeker'

    def handle(self, *args, **options):
        Favorite.etkinlikleri_getir()
        self.stdout.write(self.style.SUCCESS('Etkinlikler başarıyla çekildi.'))
