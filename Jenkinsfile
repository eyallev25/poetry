pipeline {
    agent any
    
    stages {
        stage('Build') {
            steps {
                echo 'Building..'
                sh 'curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3 -'
                sh "apt-get install -y python3-venv"
                sh "python3 -m venv venv"
                sh '. venv/bin/activate'
                sh "$HOME/.poetry/bin/poetry install --no-root"
            }
        }
        stage('Test') {
            steps {
                echo 'Testing..'
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying....'
            }
        }
    }
}