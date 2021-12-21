pipeline {
    agent any
    
    stages {
        stage('Build') {
            steps {
                echo 'Building..'
                sh 'curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3 -'
                sh "$HOME/.poetry/bin/poetry install --no-root"
                sh "$HOME/.poetry/bin/poetry shell"
            }
        }
        stage('Test') {
            steps {
                echo 'Testing..'
                sh 'python3 poetey/onboard.py'
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying....'
            }
        }
    }
}