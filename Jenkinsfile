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
                    script {
                        // Pass environment variables using the 'env' parameter of the 'sh' step.
                        // Jenkins handles the correct quoting and escaping for the shell.
                        sh(script: 'docker-compose build web', env: [
                            DJANGO_SECRET_KEY: DJANGO_SECRET_KEY_VAR, // Value comes from Jenkins Credential
                            DB_NAME: env.DB_NAME,
                            DB_USER: env.DB_USER,
                            DB_PASSWORD: env.DB_PASSWORD,
                            DJANGO_ALLOWED_HOSTS: env.DJANGO_ALLOWED_HOSTS,
                            DJANGO_DEBUG: env.DJANGO_DEBUG
                        ])
                    }
                }
            }
        }

        stage('Deploy Application') {
            steps {
                echo 'Bringing up application services with Docker Compose...'
                withCredentials([string(credentialsId: 'DJANGO_SECRET_KEY_CREDENTIAL', variable: 'DJANGO_SECRET_KEY_VAR')]) {
                    script {
                        sh(script: 'docker-compose up -d', env: [
                            DJANGO_SECRET_KEY: DJANGO_SECRET_KEY_VAR,
                            DB_NAME: env.DB_NAME,
                            DB_USER: env.DB_USER,
                            DB_PASSWORD: env.DB_PASSWORD,
                            DJANGO_ALLOWED_HOSTS: env.DJANGO_ALLOWED_HOSTS,
                            DJANGO_DEBUG: env.DJANGO_DEBUG
                        ])
                    }
                }

                echo 'Waiting for database and web services to be healthy...'
                sleep 10

                echo 'Running Django migrations...'
                withCredentials([string(credentialsId: 'DJANGO_SECRET_KEY_CREDENTIAL', variable: 'DJANGO_SECRET_KEY_VAR')]) {
                    script {
                        sh(script: '/usr/local/bin/python manage.py migrate --noinput', env: [
                            DJANGO_SECRET_KEY: DJANGO_SECRET_KEY_VAR,
                            DB_NAME: env.DB_NAME,
                            DB_USER: env.DB_USER,
                            DB_PASSWORD: env.DB_PASSWORD,
                            DB_HOST: 'db',    // Explicitly set DB_HOST for exec commands
                            DB_PORT: '5432',  // Explicitly set DB_PORT for exec commands
                            DJANGO_ALLOWED_HOSTS: env.DJANGO_ALLOWED_HOSTS,
                            DJANGO_DEBUG: env.DJANGO_DEBUG
                        ])
                    }
                }

                echo 'Collecting static files...'
                withCredentials([string(credentialsId: 'DJANGO_SECRET_KEY_CREDENTIAL', variable: 'DJANGO_SECRET_KEY_VAR')]) {
                    script {
                        sh(script: '/usr/local/bin/python manage.py collectstatic --noinput', env: [
                            DJANGO_SECRET_KEY: DJANGO_SECRET_KEY_VAR,
                            DB_NAME: env.DB_NAME,
                            DB_USER: env.DB_USER,
                            DB_PASSWORD: env.DB_PASSWORD,
                            DB_HOST: 'db',
                            DB_PORT: '5432',
                            DJANGO_ALLOWED_HOSTS: env.DJANGO_ALLOWED_HOSTS,
                            DJANGO_DEBUG: env.DJANGO_DEBUG
                        ])
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
