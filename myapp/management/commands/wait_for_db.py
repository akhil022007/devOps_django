import os
import time
import psycopg2
from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    """Django command to pause execution until database is available"""
    help = 'Waits for database to be available'

    def handle(self, *args, **options):
        self.stdout.write('Waiting for database...')
        db_conn = None
        max_retries = 30
        retry_interval = 2 # seconds

        db_name = os.environ.get('DB_NAME', 'mydjangoappdb')
        db_user = os.environ.get('DB_USER', 'mydjangoappuser')
        db_password = os.environ.get('DB_PASSWORD', 'mydjangoapppassword')
        db_host = os.environ.get('DB_HOST', 'db')
        db_port = os.environ.get('DB_PORT', '5432')

        for i in range(1, max_retries + 1):
            try:
                conn = psycopg2.connect(
                    dbname=db_name,
                    user=db_user,
                    password=db_password,
                    host=db_host,
                    port=db_port
                )
                conn.close()
                db_conn = True
                self.stdout.write(self.style.SUCCESS('Database connection successful!'))
                break
            except OperationalError as e:
                self.stdout.write(f'Database unavailable, retrying ({i}/{max_retries})... Error: {e}')
                time.sleep(retry_interval)
            except Exception as e:
                self.stdout.write(f'An unexpected error occurred: {e}')
                time.sleep(retry_interval)
        else:
            self.stderr.write(self.style.ERROR(f'Database did not become available after {max_retries} retries. Exiting.'))
            exit(1)

