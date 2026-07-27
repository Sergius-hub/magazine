from django.core.management import BaseCommand
from django.db import connection


class Command( BaseCommand ):
    help = 'Очистка базы'

    def handle( self, *args, **options ):
        with connection.cursor() as cursor:
            cursor.execute("TRUNCATE TABLE catalog_category RESTART IDENTITY CASCADE;")

        self.stdout.write( self.style.SUCCESS( '✅ Таблицы очищены' ) )