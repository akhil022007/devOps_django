pipeline {
    agent any

    environment {
        DJANGO_SECRET_KEY_PLACEHOLDER = 'PLACEHOLDER_FOR_JENKINS_CREDENTIAL_VALUE'

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
                withCredentials([string(credentialsId: 'DJANGO_SECRET_KEY_CREDENTIAL', variable: 'DJANGO_SECRET_KEY_VAR')]) {
                    script {
                        def envFilePath = "${pwd()}/.env"

                        writeFile(file: envFilePath, text: """
                        DJANGO_SECRET_KEY=${DJANGO_SECRET_KEY_VAR}
                        DB_NAME=${env.DB_NAME}
                        DB_USER=${env.DB_USER}
                        DB_PASSWORD=${env.DB_PASSWORD}
                        DJANGO_ALLOWED_HOSTS=${env.DJANGO_ALLOWED_HOSTS}
                        DJANGO_DEBUG=${env.DJANGO_DEBUG}
                        DB_HOST=db
                        DB_PORT=5432
                        """)

                        sh "docker-compose build web"

                        sh "rm ${envFilePath}"
                    }
                }
            }
        }

        stage('Deploy Application') {
            steps {
                echo 'Bringing up application services with Docker Compose...'
                withCredentials([string(credentialsId: 'DJANGO_SECRET_KEY_CREDENTIAL', variable: 'DJANGO_SECRET_KEY_VAR')]) {
                    script {
                        def envFilePath = "${pwd()}/.env"
                        writeFile(file: envFilePath, text: """
                        DJANGO_SECRET_KEY=${DJANGO_SECRET_KEY_VAR}
                        DB_NAME=${env.DB_NAME}
                        DB_USER=${env.DB_USER}
                        DB_PASSWORD=${env.DB_PASSWORD}
                        DJANGO_ALLOWED_HOSTS=${env.DJANGO_ALLOWED_HOSTS}
                        DJANGO_DEBUG=${env.DJANGO_DEBUG}
                        DB_HOST=db
                        DB_PORT=5432
                        """)
                        sh "docker-compose up -d"
                        sh "rm ${envFilePath}"
                    }
                }

                echo 'Waiting for database and web services to be healthy...'
                sleep 10

                echo 'Running Django migrations...'
                withCredentials([string(credentialsId: 'DJANGO_SECRET_KEY_CREDENTIAL', variable: 'DJANGO_SECRET_KEY_VAR')]) {
                    script {
                        def envFilePath = "${pwd()}/.env"
                        writeFile(file: envFilePath, text: """
                        DJANGO_SECRET_KEY=${DJANGO_SECRET_KEY_VAR}
                        DB_NAME=${env.DB_NAME}
                        DB_USER=${env.DB_USER}
                        DB_PASSWORD=${env.DB_PASSWORD}
                        DB_HOST=db
                        DB_PORT=5432
                        DJANGO_ALLOWED_HOSTS=${env.DJANGO_ALLOWED_HOSTS}
                        DJANGO_DEBUG=${env.DJANGO_DEBUG}
                        """)
                        sh "docker-compose exec web /usr/local/bin/python manage.py migrate --noinput"
                        sh "rm ${envFilePath}"
                    }
                }

                echo 'Collecting static files...'
                withCredentials([string(credentialsId: 'DJANGO_SECRET_KEY_CREDENTIAL', variable: 'DJANGO_SECRET_KEY_VAR')]) {
                    script {
                        def envFilePath = "${pwd()}/.env"
                        writeFile(file: envFilePath, text: """
                        DJANGO_SECRET_KEY=${DJANGO_SECRET_KEY_VAR}
                        DB_NAME=${env.DB_NAME}
                        DB_USER=${env.DB_USER}
                        DB_PASSWORD=${env.DB_PASSWORD}
                        DB_HOST=db
                        DB_PORT=5432
                        DJANGO_ALLOWED_HOSTS=${env.DJANGO_ALLOWED_HOSTS}
                        DJANGO_DEBUG=${env.DJANGO_DEBUG}
                        """)
                        sh "docker-compose exec web /usr/local/bin/python manage.py collectstatic --noinput"
                        sh "rm ${envFilePath}"
                    }
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
