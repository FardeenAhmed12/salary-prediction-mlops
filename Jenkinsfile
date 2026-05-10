pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                sh 'docker build -t salary-prediction .'
            }
        }
        stage('Test') {
            steps {
                sh 'docker run salary-prediction pytest'
            }
        }
        stage('Deploy') {
            steps {
                sh 'kubectl apply -f kubernetes/'
            }
        }
    }
}