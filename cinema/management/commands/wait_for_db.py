import time
from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("Waiting for database...")
        db_conn = None
        attempts = 0
        max_attempts = 20

        while attempts < max_attempts:
            try:
                db_conn = connections["default"]
                db_conn.cursor()
                self.stdout.write(self.style.SUCCESS(
                    f"Database available after {attempts} attempts!"
                ))
                return
            except OperationalError:
                attempts += 1
                self.stdout.write(
                    f"Database unavailable"
                    f" (attempt {attempts}/{max_attempts}), waiting 1s..."
                )
                time.sleep(1)

        self.stdout.write(self.style.ERROR(
            "Database unavailable after maximum attempts. Exiting."
        ))
        exit(1)
