import java.util.Base64

pipeline {
    agent any

    environment {
        // This variable is a placeholder. The actual DJANGO_SECRET_KEY value
        // will be injected securely from the Jenkins Secret Text Credential.
        DJANGO_SECRET_KEY_PLACEHOLDER = 'PLACEHOLDER_FOR_JENKINS_CREDENTIAL_VALUE'

        DB_NAME = 'mydjangoappdb'
        DB_USER = 'mydjangoappuser'
        DB_PASSWORD = 'mydjangoapppassword'
        DJANGO_ALLOWED_HOSTS = 'localhost,127.0.0.1' // Update if external IP is needed
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
                // Use withCredentials to securely inject the SECRET_KEY from Jenkins Credentials
                withCredentials([string(credentialsId: 'DJANGO_SECRET_KEY_CREDENTIAL', variable: 'DJANGO_SECRET_KEY_VAR')]) {
                    // Encode the secret key to Base64 before passing it to the shell
                    script {
                        def encodedSecretKey = Base64.encoder.encodeToString(DJANGO_SECRET_KEY_VAR.getBytes("UTF-8"))
                        withEnv([
                            "DJANGO_SECRET_KEY_B64=${encodedSecretKey}", // Pass the Base64 encoded key
                            "DB_NAME=${env.DB_NAME}",
                            "DB_USER=${env.DB_USER}",
                            "DB_PASSWORD=${env.DB_PASSWORD}",
                            "DJANGO_ALLOWED_HOSTS=${env.DJANGO_ALLOWED_HOSTS}",
                            "DJANGO_DEBUG=${env.DJANGO_DEBUG}"
                        ]) {
                            sh """
                            export DJANGO_SECRET_KEY_B64="${DJANGO_SECRET_KEY_B64}"
                            export DB_NAME="${DB_NAME}"
                            export DB_USER="${DB_USER}"
                            export DB_PASSWORD="${DB_PASSWORD}"
                            export DJANGO_ALLOWED_HOSTS="${DJANGO_ALLOWED_HOSTS}"
                            export DJANGO_DEBUG="${DJANGO_DEBUG}"
                            docker-compose build web
                            """
                        }
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
                        withEnv([
                            "DJANGO_SECRET_KEY_B64=${encodedSecretKey}",
                            "DB_NAME=${env.DB_NAME}",
                            "DB_USER=${env.DB_USER}",
                            "DB_PASSWORD=${env.DB_PASSWORD}",
                            "DJANGO_ALLOWED_HOSTS=${env.DJANGO_ALLOWED_HOSTS}",
                            "DJANGO_DEBUG=${env.DJANGO_DEBUG}"
                        ]) {
                            sh """
                            export DJANGO_SECRET_KEY_B64="${DJANGO_SECRET_KEY_B64}"
                            export DB_NAME="${DB_NAME}"
                            export DB_USER="${DB_USER}"
                            export DB_PASSWORD="${DB_PASSWORD}"
                            export DJANGO_ALLOWED_HOSTS="${DJANGO_ALLOWED_HOSTS}"
                            export DJANGO_DEBUG="${DJANGO_DEBUG}"
                            docker-compose up -d
                            """
                        }
                    }
                }

                echo 'Waiting for database and web services to be healthy...'
                sleep 10

                echo 'Running Django migrations...'
                withCredentials([string(credentialsId: 'DJANGO_SECRET_KEY_CREDENTIAL', variable: 'DJANGO_SECRET_KEY_VAR')]) {
                    script {
                        def encodedSecretKey = Base64.encoder.encodeToString(DJANGO_SECRET_KEY_VAR.getBytes("UTF-8"))
                        withEnv([
                            "DJANGO_SECRET_KEY_B64=${encodedSecretKey}",
                            "DB_NAME=${env.DB_NAME}",
                            "DB_USER=${env.DB_USER}",
                            "DB_PASSWORD=${env.DB_PASSWORD}",
                            "DB_HOST=db",
                            "DB_PORT=5432",
                            "DJANGO_ALLOWED_HOSTS=${env.DJANGO_ALLOWED_HOSTS}",
                            "DJANGO_DEBUG=${env.DJANGO_DEBUG}"
                        ]) {
                            sh """
                            export DJANGO_SECRET_KEY_B64="${DJANGO_SECRET_KEY_B64}"
                            export DB_NAME="${DB_NAME}"
                            export DB_USER="${DB_USER}"
                            export DB_PASSWORD="${DB_PASSWORD}"
                            export DB_HOST="${DB_HOST}"
                            export DB_PORT="${DB_PORT}"
                            export DJANGO_ALLOWED_HOSTS="${DJANGO_ALLOWED_HOSTS}"
                            export DJANGO_DEBUG="${DJANGO_DEBUG}"
                            docker-compose exec web /usr/local/bin/python manage.py migrate --noinput
                            """
                        }
                    }
                }

                echo 'Collecting static files...'
                withCredentials([string(credentialsId: 'DJANGO_SECRET_KEY_CREDENTIAL', variable: 'DJANGO_SECRET_KEY_VAR')]) {
                    script {
                        def encodedSecretKey = Base64.encoder.encodeToString(DJANGO_SECRET_KEY_VAR.getBytes("UTF-8"))
                        withEnv([
                            "DJANGO_SECRET_KEY_B64=${encodedSecretKey}",
                            "DB_NAME=${env.DB_NAME}",
                            "DB_USER=${env.DB_USER}",
                            "DB_PASSWORD=${env.DB_PASSWORD}",
                            "DB_HOST=db",
                            "DB_PORT=5432",
                            "DJANGO_ALLOWED_HOSTS=${env.DJANGO_ALLOWED_HOSTS}",
                            "DJANGO_DEBUG=${env.DJANGO_DEBUG}"
                        ]) {
                            sh """
                            export DJANGO_SECRET_KEY_B64="${DJANGO_SECRET_KEY_B64}"
                            export DB_NAME="${DB_NAME}"
                            export DB_USER="${DB_USER}"
                            export DB_PASSWORD="${DB_PASSWORD}"
                            export DB_HOST="${DB_HOST}"
                            export DB_PORT="${DB_PORT}"
                            export DJANGO_ALLOWED_HOSTS="${DJANGO_ALLOWED_HOSTS}"
                            export DJANGO_DEBUG="${DJANGO_DEBUG}"
                            docker-compose exec web /usr/local/bin/python manage.py collectstatic --noinput
                            """
                        }
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
