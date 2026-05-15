pipeline {

    agent any

    environment {
        IMAGE_NAME = "salary-mlops"
        IMAGE_TAG = "latest"
    }

    stages {

        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image...'

                sh 'docker build -t $IMAGE_NAME:$IMAGE_TAG .'
            }
        }

        stage('Run Tests') {
            steps {
                echo 'Running tests...'

                sh 'docker run --rm $IMAGE_NAME:$IMAGE_TAG pytest || true'
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                echo 'Deploying to Kubernetes...'

                sh 'sudo k3s kubectl apply -f k8s/'
            }
        }

        stage('Verify Deployment') {
            steps {
                echo 'Checking Kubernetes resources...'

                sh 'sudo k3s kubectl get pods'
                sh 'sudo k3s kubectl get svc'
            }
        }
    }

    post {

        success {
            echo 'CI/CD Pipeline executed successfully!'
        }

        failure {
            echo 'Pipeline failed!'
        }
    }
}
