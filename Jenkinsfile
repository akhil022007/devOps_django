pipeline {
    agent any

    environment {
        // These variables will be populated by the Jenkins credential or directly.
        // They are kept here for clarity of what env vars are expected.
        // The actual DJANGO_SECRET_KEY value will come from the Jenkins Secret Text Credential.
        DJANGO_SECRET_KEY_PLACEHOLDER = 'PLACEHOLDER_FOR_JENKINS_CREDENTIAL_VALUE' // This is just a placeholder
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
                // Use withCredentials to securely inject the SECRET_KEY
                withCredentials([string(credentialsId: 'DJANGO_SECRET_KEY_CREDENTIAL', variable: 'DJANGO_SECRET_KEY_VAR')]) {
                    script {
                        // Pass environment variables directly to docker-compose build using --build-arg or --env
                        // For build, --build-arg is preferred if the Dockerfile uses ARG.
                        // If Dockerfile uses ENV, then passing via --env is needed for the build context.
                        // Let's pass them as explicit env vars for the shell running docker-compose.
                        sh """
                        DJANGO_SECRET_KEY='${DJANGO_SECRET_KEY_VAR}' \\
                        DB_NAME='${env.DB_NAME}' \\
                        DB_USER='${env.DB_USER}' \\
                        DB_PASSWORD='${env.DB_PASSWORD}' \\
                        DJANGO_ALLOWED_HOSTS='${env.DJANGO_ALLOWED_HOSTS}' \\
                        DJANGO_DEBUG='${env.DJANGO_DEBUG}' \\
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
                        // Pass environment variables directly to docker-compose up using --env
                        sh """
                        DJANGO_SECRET_KEY='${DJANGO_SECRET_KEY_VAR}' \\
                        DB_NAME='${env.DB_NAME}' \\
                        DB_USER='${env.DB_USER}' \\
                        DB_PASSWORD='${env.DB_PASSWORD}' \\
                        DJANGO_ALLOWED_HOSTS='${env.DJANGO_ALLOWED_HOSTS}' \\
                        DJANGO_DEBUG='${env.DJANGO_DEBUG}' \\
                        docker-compose up -d
                        """
                    }
                }

                echo 'Waiting for database and web services to be healthy...'
                sleep 10

                echo 'Running Django migrations...'
                withCredentials([string(credentialsId: 'DJANGO_SECRET_KEY_CREDENTIAL', variable: 'DJANGO_SECRET_KEY_VAR')]) {
                    script {
                        // Pass environment variables directly to docker-compose exec
                        sh """
                        DJANGO_SECRET_KEY='${DJANGO_SECRET_KEY_VAR}' \\
                        DB_NAME='${env.DB_NAME}' \\
                        DB_USER='${env.DB_USER}' \\
                        DB_PASSWORD='${env.DB_PASSWORD}' \\
                        DJANGO_ALLOWED_HOSTS='${env.DJANGO_ALLOWED_HOSTS}' \\
                        DJANGO_DEBUG='${env.DJANGO_DEBUG}' \\
                        docker-compose exec web /usr/local/bin/python manage.py migrate --noinput
                        """
                    }
                }

                echo 'Collecting static files...'
                withCredentials([string(credentialsId: 'DJANGO_SECRET_KEY_CREDENTIAL', variable: 'DJANGO_SECRET_KEY_VAR')]) {
                    script {
                        // Pass environment variables directly to docker-compose exec
                        sh """
                        DJANGO_SECRET_KEY='${DJANGO_SECRET_KEY_VAR}' \\
                        DB_NAME='${env.DB_NAME}' \\
                        DB_USER='${env.DB_USER}' \\
                        DB_PASSWORD='${env.DB_PASSWORD}' \\
                        DJANGO_ALLOWED_HOSTS='${env.DJANGO_ALLOWED_HOSTS}' \\
                        DJANGO_DEBUG='${env.DJANGO_DEBUG}' \\
                        docker-compose exec web /usr/local/bin/python manage.py collectstatic --noinput
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
