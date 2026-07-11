import time

from django.core.management import BaseCommand
from django.db import OperationalError, connection
from django.db.backends.mysql.base import BaseDatabaseWrapper

connection: BaseDatabaseWrapper = connection

class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("Waiting database...")
        con_db = False

        while not con_db:
            try:
                connection.ensure_connection()
                con_db = True
            except OperationalError:
                self.stdout.write("Database unavailable, wait 3 seconds...")
                time.sleep(3)

        self.stdout.write(self.style.SUCCESS("Database available."))