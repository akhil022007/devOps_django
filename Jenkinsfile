pipeline {
    agent any

    environment {
        // This is your actual, securely generated Django SECRET_KEY.
        // The triple quotes ensure Groovy handles it correctly.
        DJANGO_SECRET_KEY = '''1v3#rts0=9v*8hrrg1#$b7ai8%05(hil_(&r)f3gvvtac$)!4p'''
        DB_NAME = 'mydjangoappdb'
        DB_USER = 'mydjangoappuser'
        DB_PASSWORD = 'mydjangoapppassword'
        DJANGO_ALLOWED_HOSTS = 'localhost,127.0.0.1'
        DJANGO_DEBUG = 'False'
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out source code...'
                cleanWs()
                git branch: 'main', url: 'https://github.com/akhil022007/devOps_django.git'
            }
        }

        stage('Build Docker Images') {
            steps {
                echo 'Building Docker images...'
                withEnv([
                    // Pass environment variables with single quotes to prevent shell interpretation of special characters
                    "DJANGO_SECRET_KEY='${env.DJANGO_SECRET_KEY}'",
                    "DB_NAME='${env.DB_NAME}'",
                    "DB_USER='${env.DB_USER}'",
                    "DB_PASSWORD='${env.DB_PASSWORD}'",
                    "DJANGO_ALLOWED_HOSTS='${env.DJANGO_ALLOWED_HOSTS}'",
                    "DJANGO_DEBUG='${env.DJANGO_DEBUG}'"
                ]) {
                    sh 'docker-compose build web'
                }
            }
        }

        stage('Deploy Application') {
            steps {
                echo 'Bringing up application services with Docker Compose...'
                withEnv([
                    // Pass environment variables with single quotes to prevent shell interpretation of special characters
                    "DJANGO_SECRET_KEY='${env.DJANGO_SECRET_KEY}'",
                    "DB_NAME='${env.DB_NAME}'",
                    "DB_USER='${env.DB_USER}'",
                    "DB_PASSWORD='${env.DB_PASSWORD}'",
                    "DJANGO_ALLOWED_HOSTS='${env.DJANGO_ALLOWED_HOSTS}'",
                    "DJANGO_DEBUG='${env.DJANGO_DEBUG}'"
                ]) {
                    sh 'docker-compose up -d'
                }

                echo 'Waiting for database and web services to be healthy...'
                sleep 10

                echo 'Running Django migrations...'
                withEnv([
                    // Pass environment variables with single quotes for exec commands too
                    "DJANGO_SECRET_KEY='${env.DJANGO_SECRET_KEY}'",
                    "DB_NAME='${env.DB_NAME}'",
                    "DB_USER='${env.DB_USER}'",
                    "DB_PASSWORD='${env.DB_PASSWORD}'",
                    "DJANGO_ALLOWED_HOSTS='${env.DJANGO_ALLOWED_HOSTS}'",
                    "DJANGO_DEBUG='${env.DJANGO_DEBUG}'"
                ]) {
                    sh 'docker-compose exec web /usr/local/bin/python manage.py migrate --noinput'
                }


                echo 'Collecting static files...'
                withEnv([
                    // Pass environment variables with single quotes for exec commands too
                    "DJANGO_SECRET_KEY='${env.DJANGO_SECRET_KEY}'",
                    "DB_NAME='${env.DB_NAME}'",
                    "DB_USER='${env.DB_USER}'",
                    "DB_PASSWORD='${env.DB_PASSWORD}'",
                    "DJANGO_ALLOWED_HOSTS='${env.DJANGO_ALLOWED_HOSTS}'",
                    "DJANGO_DEBUG='${env.DJANGO_DEBUG}'"
                ]) {
                    sh 'docker-compose exec web /usr/local/bin/python manage.py collectstatic --noinput'
                }

                echo 'Application deployed and migrations applied!'
            }
        }

        stage('Test Application') {
            steps {
                echo 'Testing application accessibility...'
                sh 'curl -f http://localhost:8000 || { echo "Application not accessible! Check logs."; exit 1; }'
                echo 'Application is accessible!'
            }
        }
    }

    post {
        always {
            echo 'Cleaning up Docker containers and volumes...'
            sh 'docker-compose down -v'
            echo 'Cleanup complete for this build.'
        }
        failure {
            echo 'Pipeline failed. Check logs for errors.'
        }
    }
}
