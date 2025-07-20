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

                        // Remove the .env file immediately after build, as it's not needed for subsequent steps in this stage.
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

                        echo 'Waiting for database and web services to be healthy...'
                        sleep 10

                        // --- CRITICAL: Capture logs and container status for debugging ---
                        echo 'Capturing web service logs for debugging...'
                        sh "docker-compose logs web"
                        echo 'Capturing container status for debugging (should show exited containers)...'
                        sh "docker-compose ps -a"
                        // --- END CRITICAL ---

                        echo 'Running Django migrations...'
                        // The .env file is still present here for docker-compose to implicitly pick up
                        sh "docker-compose exec web /usr/local/bin/python manage.py migrate --noinput"

                        echo 'Collecting static files...'
                        sh "docker-compose exec web /usr/local/bin/python manage.py collectstatic --noinput"

                        echo 'Application deployed and migrations applied!'
                        // Remove the .env file after all commands that might need it
                        sh "rm ${envFilePath}"
                    }
                }
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
            // Ensure .env file is removed even if a previous stage failed to remove it
            sh "rm -f ${pwd()}/.env" // -f to force remove silently if not found
            sh 'docker-compose down -v'
            echo 'Cleanup complete for this build.'
        }
        failure {
            echo 'Pipeline failed. Check logs for errors.'
        }
    }
}
