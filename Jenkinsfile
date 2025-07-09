import java.util.Base64 // Import Base64 utility for encoding the secret key

pipeline {
    agent any // Run the pipeline on any available agent

    environment {
        // Placeholder for the Django Secret Key. Its actual value is
        // securely injected from Jenkins Credentials using 'withCredentials'.
        DJANGO_SECRET_KEY_PLACEHOLDER = 'PLACEHOLDER_FOR_JENKINS_CREDENTIAL_VALUE'

        // Other environment variables for your application
        DB_NAME = 'mydjangoappdb'
        DB_USER = 'mydjangoappuser'
        DB_PASSWORD = 'mydjangoapppassword'
        DJANGO_ALLOWED_HOSTS = 'localhost,127.0.0.1' // Update this if your Jenkins server has a different hostname/IP
        DJANGO_DEBUG = 'False' // Set to True for debugging, False for production
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out source code...'
                cleanWs() // Clean the workspace before checkout
                git branch: 'main', url: 'https://github.com/akhil022007/devOps_django.git' // Your GitHub repository
            }
        }

        stage('Build Docker Images') {
            steps {
                echo 'Building Docker images...'
                // Securely inject the DJANGO_SECRET_KEY from Jenkins Credentials
                // The credential ID MUST match the one created in Jenkins
                withCredentials([string(credentialsId: 'DJANGO_SECRET_KEY_CREDENTIAL', variable: 'DJANGO_SECRET_KEY_VAR')]) {
                    script {
                        // Encode the sensitive secret key to Base64 within Groovy
                        def encodedSecretKey = Base64.encoder.encodeToString(DJANGO_SECRET_KEY_VAR.getBytes("UTF-8"))

                        // Execute docker-compose build.
                        // CRITICAL FIX: Directly interpolate the Groovy 'encodedSecretKey' variable
                        // into the shell script using "${encodedSecretKey}".
                        // This ensures the value is passed correctly, avoiding shell re-interpretation.
                        sh """
                        export DJANGO_SECRET_KEY_B64="${encodedSecretKey}"
                        export DB_NAME="${env.DB_NAME}"
                        export DB_USER="${env.DB_USER}"
                        export DB_PASSWORD="${DB_PASSWORD}"
                        export DJANGO_ALLOWED_HOSTS="${DJANGO_ALLOWED_HOSTS}"
                        export DJANGO_DEBUG="${DJANGO_DEBUG}"
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
                        sh """
                        export DJANGO_SECRET_KEY_B64="${encodedSecretKey}"
                        export DB_NAME="${env.DB_NAME}"
                        export DB_USER="${DB_USER}"
                        export DB_PASSWORD="${DB_PASSWORD}"
                        export DJANGO_ALLOWED_HOSTS="${DJANGO_ALLOWED_HOSTS}"
                        export DJANGO_DEBUG="${DJANGO_DEBUG}"
                        docker-compose up -d
                        """
                    }
                }

                echo 'Waiting for database and web services to be healthy...'
                sleep 10

                echo 'Running Django migrations...'
                withCredentials([string(credentialsId: 'DJANGO_SECRET_KEY_CREDENTIAL', variable: 'DJANGO_SECRET_KEY_VAR')]) {
                    script {
                        def encodedSecretKey = Base64.encoder.encodeToString(DJANGO_SECRET_KEY_VAR.getBytes("UTF-8"))
                        sh """
                        export DJANGO_SECRET_KEY_B64="${encodedSecretKey}"
                        export DB_NAME="${DB_NAME}"
                        export DB_USER="${DB_USER}"
                        export DB_PASSWORD="${DB_PASSWORD}"
                        export DB_HOST="db"
                        export DB_PORT="5432"
                        export DJANGO_ALLOWED_HOSTS="${DJANGO_ALLOWED_HOSTS}"
                        export DJANGO_DEBUG="${DJANGO_DEBUG}"
                        docker-compose exec web /usr/local/bin/python manage.py migrate --noinput
                        """
                    }
                }

                echo 'Collecting static files...'
                withCredentials([string(credentialsId: 'DJANGO_SECRET_KEY_CREDENTIAL', variable: 'DJANGO_SECRET_KEY_VAR')]) {
                    script {
                        def encodedSecretKey = Base64.encoder.encodeToString(DJANGO_SECRET_KEY_VAR.getBytes("UTF-8"))
                        sh """
                        export DJANGO_SECRET_KEY_B64="${encodedSecretKey}"
                        export DB_NAME="${DB_NAME}"
                        export DB_USER="${DB_USER}"
                        export DB_PASSWORD="${DB_PASSWORD}"
                        export DB_HOST="db"
                        export DB_PORT="5432"
                        export DJANGO_ALLOWED_HOSTS="${DJANGO_ALLOWED_HOSTS}"
                        export DJANGO_DEBUG="${DJANGO_DEBUG}"
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
