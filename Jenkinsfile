pipeline {
    agent any

    stages {
        stage('Declarative: Checkout SCM') {
            steps {
                checkout scm
            }
        }
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
                dir('devOps_docker') { // Assuming your docker-compose.yml is in a 'devOps_docker' subdirectory
                    sh 'docker-compose build web'
                }
            }
        }
        stage('Deploy Application') {
            steps {
                echo 'Bringing up application services with Docker Compose...'
                dir('devOps_docker') {
                    sh 'docker-compose up -d'
                }

                echo 'Waiting for database to be healthy...'
                script {
                    def maxAttempts = 30
                    def attempt = 1
                    while (attempt <= maxAttempts) {
                        def dbStatus = sh(script: 'docker-compose ps db | grep "(healthy)"', returnStatus: true)
                        if (dbStatus == 0) {
                            echo 'Database is healthy and ready!'
                            break
                        } else {
                            echo "Database not ready yet, waiting... (${attempt}/${maxAttempts})"
                            sleep 5 // Wait for 5 seconds
                            attempt++
                        }
                    }
                    if (attempt > maxAttempts) {
                        error 'Database did not become healthy within the timeout.'
                    }
                }

                // --- ADD THIS NEW SECTION TO WAIT FOR THE 'WEB' SERVICE ---
                echo 'Waiting for web service to be healthy...'
                script {
                    def maxAttempts = 30 // You can adjust this
                    def attempt = 1
                    while (attempt <= maxAttempts) {
                        // Assuming your web service has a HEALTHCHECK in its Dockerfile
                        def webStatus = sh(script: 'docker-compose ps web | grep "(healthy)"', returnStatus: true)
                        if (webStatus == 0) {
                            echo 'Web service is healthy and ready!'
                            break
                        } else {
                            echo "Web service not ready yet, waiting... (${attempt}/${maxAttempts})"
                            sleep 5 // Wait for 5 seconds
                            attempt++
                        }
                    }
                    if (attempt > maxAttempts) {
                        error 'Web service did not become healthy within the timeout.'
                    }
                }
                // --- END NEW SECTION ---

                echo 'Running Django migrations...'
                dir('devOps_docker') {
                    sh 'docker-compose exec web /usr/local/bin/python manage.py migrate --noinput'
                }
            }
        }
        stage('Test Application') {
            steps {
                echo 'Running application tests...'
                dir('devOps_docker') {
                    // Add your test commands here, e.g.:
                    // sh 'docker-compose exec web /usr/local/bin/python manage.py test'
                    echo 'Tests would run here.' // Placeholder
                }
            }
        }
    }
    post {
        always {
            echo 'Cleaning up Docker containers and volumes...'
            dir('devOps_docker') {
                sh 'docker-compose down -v'
            }
            echo 'Cleanup complete for this build.'
        }
        success {
            echo 'Pipeline succeeded!'
        }
        failure {
            echo 'Pipeline failed. Check logs for errors.'
        }
    }
}
