pipeline {
   
    environment {
       
        DJANGO_SECRET_KEY = 'django-insecure-feao+6twuf$&$r*%qv&#k)mw@&n+=ctbru6djro7gx7^h3#ii8'
        DB_NAME = 'mydjangoappdb'
        DB_USER = 'mydjangoappuser'
        DB_PASSWORD = 'mydjangoapppassword'
     
        DJANGO_ALLOWED_HOSTS = 'localhost,127.0.0.1,your_jenkins_server_ip_or_hostname'
        DJANGO_DEBUG = 'False' # Set to False for deployment, True for local dev
    }

    
    stages {
        
        stage('Checkout') {
            steps {
                echo 'Checking out source code...'
                // Clean the workspace to ensure a fresh build
                cleanWs()
                // Use the SCM (Source Code Management) configured in the Jenkins job
                // This typically means pulling from the GitHub repository linked to the job
                git branch: 'main', url: 'https://github.com/akhil022007/devOps_django.git'
                // IMPORTANT: Replace 'your-username/my_django_project.git' with your actual GitHub repository URL
            }
        }

        // Stage 2: Build Docker Images
        stage('Build Docker Images') {
            steps {
                echo 'Building Docker images...'
                // Use docker-compose to build the 'web' service image
                // The '.' indicates the Dockerfile is in the current directory
                // Pass environment variables from Jenkins to docker-compose build process
                withEnv([
                    "DJANGO_SECRET_KEY=${env.DJANGO_SECRET_KEY}",
                    "DB_NAME=${env.DB_NAME}",
                    "DB_USER=${env.DB_USER}",
                    "DB_PASSWORD=${env.DB_PASSWORD}",
                    "DJANGO_ALLOWED_HOSTS=${env.DJANGO_ALLOWED_HOSTS}",
                    "DJANGO_DEBUG=${env.DJANGO_DEBUG}"
                ]) {
                    sh 'docker-compose build web'
                }
            }
        }

        // Stage 3: Deploy with Docker Compose
        stage('Deploy Application') {
            steps {
                echo 'Bringing up application services with Docker Compose...'
               
                withEnv([
                    "DJANGO_SECRET_KEY=${env.DJANGO_SECRET_KEY}",
                    "DB_NAME=${env.DB_NAME}",
                    "DB_USER=${env.DB_USER}",
                    "DB_PASSWORD=${env.DB_PASSWORD}",
                    "DJANGO_ALLOWED_HOSTS=${env.DJANGO_ALLOWED_HOSTS}",
                    "DJANGO_DEBUG=${env.DJANGO_DEBUG}"
                ]) {
                    sh 'docker-compose up -d'
                }

                echo 'Waiting for database to be healthy...'
                
                script {
                    def maxRetries = 30 
                    def retryCount = 0
                    def dbReady = false
                    while (retryCount < maxRetries && !dbReady) {
                        try {
                           
                            sh 'docker-compose ps db | grep "(healthy)"'
                            dbReady = true
                            echo "Database is healthy and ready!"
                        } catch (Exception e) {
                            echo "Database not ready yet, waiting... (${retryCount + 1}/${maxRetries})"
                            sleep 5 // Wait for 5 seconds before retrying
                            retryCount++
                        }
                    }
                    if (!dbReady) {
                        error "Database did not become healthy within the timeout. Check DB logs."
                    }
                }

                echo 'Running Django migrations...'
                // Execute migrations inside the 'web' container using its full path to python
                // --noinput prevents interactive prompts
                sh 'docker-compose exec web /usr/local/bin/python manage.py migrate --noinput'

                echo 'Collecting static files...'
                // Collect static files inside the 'web' container using its full path to python
                sh 'docker-compose exec web /usr/local/bin/python manage.py collectstatic --noinput'

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
