// No Base64 import needed for this approach

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
                    // Set environment variables for the current shell context using withEnv.
                    // Then, within the sh command, use printf %q to robustly quote the values.
                    withEnv([
                        "DJANGO_SECRET_KEY_ENV=${DJANGO_SECRET_KEY_VAR}", // Pass the credential value to a new env var
                        "DB_NAME_ENV=${env.DB_NAME}",
                        "DB_USER_ENV=${env.DB_USER}",
                        "DB_PASSWORD_ENV=${env.DB_PASSWORD}",
                        "DJANGO_ALLOWED_HOSTS_ENV=${env.DJANGO_ALLOWED_HOSTS}",
                        "DJANGO_DEBUG_ENV=${env.DJANGO_DEBUG}"
                    ]) {
                        // Use triple single quotes (''') for the sh block to prevent Groovy interpolation
                        // This ensures printf %q output is passed literally to the shell.
                        sh '''
                        export DJANGO_SECRET_KEY=$(printf %q "${DJANGO_SECRET_KEY_ENV}")
                        export DB_NAME=$(printf %q "${DB_NAME_ENV}")
                        export DB_USER=$(printf %q "${DB_USER_ENV}")
                        export DB_PASSWORD=$(printf %q "${DB_PASSWORD_ENV}")
                        export DJANGO_ALLOWED_HOSTS=$(printf %q "${DJANGO_ALLOWED_HOSTS_ENV}")
                        export DJANGO_DEBUG=$(printf %q "${DJANGO_DEBUG_ENV}")
                        docker-compose build web
                        '''
                    }
                }
            }
        }

        stage('Deploy Application') {
            steps {
                echo 'Bringing up application services with Docker Compose...'
                withCredentials([string(credentialsId: 'DJANGO_SECRET_KEY_CREDENTIAL', variable: 'DJANGO_SECRET_KEY_VAR')]) {
                    script {
                        withEnv([
                            "DJANGO_SECRET_KEY_ENV=${DJANGO_SECRET_KEY_VAR}",
                            "DB_NAME_ENV=${env.DB_NAME}",
                            "DB_USER_ENV=${env.DB_USER}",
                            "DB_PASSWORD_ENV=${env.DB_PASSWORD}",
                            "DJANGO_ALLOWED_HOSTS_ENV=${env.DJANGO_ALLOWED_HOSTS}",
                            "DJANGO_DEBUG_ENV=${env.DJANGO_DEBUG}"
                        ]) {
                            sh '''
                            export DJANGO_SECRET_KEY=$(printf %q "${DJANGO_SECRET_KEY_ENV}")
                            export DB_NAME=$(printf %q "${DB_NAME_ENV}")
                            export DB_USER=$(printf %q "${DB_USER_ENV}")
                            export DB_PASSWORD=$(printf %q "${DB_PASSWORD_ENV}")
                            export DJANGO_ALLOWED_HOSTS=$(printf %q "${DJANGO_ALLOWED_HOSTS_ENV}")
                            export DJANGO_DEBUG=$(printf %q "${DJANGO_DEBUG_ENV}")
                            docker-compose up -d
                            '''
                        }
                    }
                }

                echo 'Waiting for database and web services to be healthy...'
                sleep 10

                echo 'Running Django migrations...'
                withCredentials([string(credentialsId: 'DJANGO_SECRET_KEY_CREDENTIAL', variable: 'DJANGO_SECRET_KEY_VAR')]) {
                    script {
                        withEnv([
                            "DJANGO_SECRET_KEY_ENV=${DJANGO_SECRET_KEY_VAR}",
                            "DB_NAME_ENV=${env.DB_NAME}",
                            "DB_USER_ENV=${env.DB_USER}",
                            "DB_PASSWORD_ENV=${env.DB_PASSWORD}",
                            "DB_HOST_ENV=db",
                            "DB_PORT_ENV=5432",
                            "DJANGO_ALLOWED_HOSTS_ENV=${env.DJANGO_ALLOWED_HOSTS}",
                            "DJANGO_DEBUG_ENV=${env.DJANGO_DEBUG}"
                        ]) {
                            sh '''
                            export DJANGO_SECRET_KEY=$(printf %q "${DJANGO_SECRET_KEY_ENV}")
                            export DB_NAME=$(printf %q "${DB_NAME_ENV}")
                            export DB_USER=$(printf %q "${DB_USER_ENV}")
                            export DB_PASSWORD=$(printf %q "${DB_PASSWORD_ENV}")
                            export DB_HOST=$(printf %q "${DB_HOST_ENV}")
                            export DB_PORT=$(printf %q "${DB_PORT_ENV}")
                            export DJANGO_ALLOWED_HOSTS=$(printf %q "${DJANGO_ALLOWED_HOSTS_ENV}")
                            export DJANGO_DEBUG=$(printf %q "${DJANGO_DEBUG_ENV}")
                            docker-compose exec web /usr/local/bin/python manage.py migrate --noinput
                            '''
                        }
                    }
                }

                echo 'Collecting static files...'
                withCredentials([string(credentialsId: 'DJANGO_SECRET_KEY_CREDENTIAL', variable: 'DJANGO_SECRET_KEY_VAR')]) {
                    script {
                        withEnv([
                            "DJANGO_SECRET_KEY_ENV=${DJANGO_SECRET_KEY_VAR}",
                            "DB_NAME_ENV=${env.DB_NAME}",
                            "DB_USER_ENV=${env.DB_USER}",
                            "DB_PASSWORD_ENV=${env.DB_PASSWORD}",
                            "DB_HOST_ENV=db",
                            "DB_PORT_ENV=5432",
                            "DJANGO_ALLOWED_HOSTS_ENV=${env.DJANGO_ALLOWED_HOSTS}",
                            "DJANGO_DEBUG_ENV=${env.DJANGO_DEBUG}"
                        ]) {
                            sh '''
                            export DJANGO_SECRET_KEY=$(printf %q "${DJANGO_SECRET_KEY_ENV}")
                            export DB_NAME=$(printf %q "${DB_NAME_ENV}")
                            export DB_USER=$(printf %q "${DB_USER_ENV}")
                            export DB_PASSWORD=$(printf %q "${DB_PASSWORD_ENV}")
                            export DB_HOST=$(printf %q "${DB_HOST_ENV}")
                            export DB_PORT=$(printf %q "${DB_PORT_ENV}")
                            export DJANGO_ALLOWED_HOSTS=$(printf %q "${DJANGO_ALLOWED_HOSTS_ENV}")
                            export DJANGO_DEBUG=$(printf %q "${DJANGO_DEBUG_ENV}")
                            docker-compose exec web /usr/local/bin/python manage.py collectstatic --noinput
                            '''
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
