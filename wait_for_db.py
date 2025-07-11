        import os
        import time
        import psycopg2
        from django.db import connections
        from django.db.utils import OperationalError

        if __name__ == "__main__":
            db_conn = None
            max_retries = 30
            retry_interval = 2 # seconds

            db_name = os.environ.get('DB_NAME', 'mydjangoappdb')
            db_user = os.environ.get('DB_USER', 'mydjangoappuser')
            db_password = os.environ.get('DB_PASSWORD', 'mydjangoapppassword')
            db_host = os.environ.get('DB_HOST', 'db')
            db_port = os.environ.get('DB_PORT', '5432')

            print(f"Waiting for database at {db_host}:{db_port}...")

            for i in range(1, max_retries + 1):
                try:
                    db_conn = psycopg2.connect(
                        dbname=db_name,
                        user=db_user,
                        password=db_password,
                        host=db_host,
                        port=db_port
                    )
                    print("Database connection successful!")
                    db_conn.close()
                    break
                except OperationalError as e:
                    print(f"Database unavailable, retrying ({i}/{max_retries})... Error: {e}")
                    time.sleep(retry_interval)
                except Exception as e:
                    print(f"An unexpected error occurred: {e}")
                    time.sleep(retry_interval)
            else:
                print(f"Database did not become available after {max_retries} retries. Exiting.")
                exit(1)
        