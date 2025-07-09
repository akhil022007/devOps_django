import java.util.Base64

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
                        def encodedSecretKey = Base64.encoder.encodeToString(DJANGO_SECRET_KEY_VAR.getBytes("UTF-8"))
                        // Removed -e flags from build command as it's not supported
                        sh """
                        docker-compose build web
                        """
                    }
                }
            }
        }

        stage('Deploy Application') {
            steps {
                echo 'Bringing up application services with Docker Compose...'
                withCredentials([string(credentialsId: 'DJANGO_SECRET_KEY_CREDENTIAL', variable: 'DJANGO_SECRET_KEY_VAR')]) {
                    script {
                        def encodedSecretKey = Base64.encoder.encodeToString(DJANGO_SECRET_KEY_VAR.getBytes("UTF-8"))
                        // Keep -e flags for up command
                        sh """
                        docker-compose up -d \\
                        -e DJANGO_SECRET_KEY_B64="${encodedSecretKey}" \\
                        -e DB_NAME="${env.DB_NAME}" \\
                        -e DB_USER="${DB_USER}" \\
                        -e DB_PASSWORD="${DB_PASSWORD}" \\
                        -e DJANGO_ALLOWED_HOSTS="${DJANGO_ALLOWED_HOSTS}" \\
                        -e DJANGO_DEBUG="${DJANGO_DEBUG}"
                        """
                    }
                }

                echo 'Waiting for database and web services to be healthy...'
                sleep 10

                echo 'Running Django migrations...'
                withCredentials([string(credentialsId: 'DJANGO_SECRET_KEY_CREDENTIAL', variable: 'DJANGO_SECRET_KEY_VAR')]) {
                    script {
                        def encodedSecretKey = Base64.encoder.encodeToString(DJANGO_SECRET_KEY_VAR.getBytes("UTF-8"))
                        // Keep -e flags for exec command
                        sh """
                        docker-compose exec web /usr/local/bin/python manage.py migrate --noinput \\
                        -e DJANGO_SECRET_KEY_B64="${encodedSecretKey}" \\
                        -e DB_NAME="${DB_NAME}" \\
                        -e DB_USER="${DB_USER}" \\
                        -e DB_PASSWORD="${DB_PASSWORD}" \\
                        -e DB_HOST="db" \\
                        -e DB_PORT="5432" \\
                        -e DJANGO_ALLOWED_HOSTS="${DJANGO_ALLOWED_HOSTS}" \\
                        -e DJANGO_DEBUG="${DJANGO_DEBUG}"
                        """
                    }
                }

                echo 'Collecting static files...'
                withCredentials([string(credentialsId: 'DJANGO_SECRET_KEY_CREDENTIAL', variable: 'DJANGO_SECRET_KEY_VAR')]) {
                    script {
                        def encodedSecretKey = Base64.encoder.encodeToString(DJANGO_SECRET_KEY_VAR.getBytes("UTF-8"))
                        // Keep -e flags for exec command
                        sh """
                        docker-compose exec web /usr/local/bin/python manage.py collectstatic --noinput \\
                        -e DJANGO_SECRET_KEY_B64="${encodedSecretKey}" \\
                        -e DB_NAME="${DB_NAME}" \\
                        -e DB_USER="${DB_USER}" \\
                        -e DB_PASSWORD="${DB_PASSWORD}" \\
                        -e DB_HOST="db" \\
                        -e DB_PORT="5432" \\
                        -e DJANGO_ALLOWED_HOSTS="${DJANGO_ALLOWED_HOSTS}" \\
                        -e DJANGO_DEBUG="${DJANGO_DEBUG}"
                        """
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
