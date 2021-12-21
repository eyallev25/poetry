pipeline {
    agent any
    // environment {
    //     POETRY_UNINSTALL=1
        
    // }
    stages {
        stage('Build') {
            steps {
                echo 'Building..'
                sh 'curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3 -'
                sh "$HOME/.poetry/bin/poetry install --no-root"
                sh ". .venv/bin/activate"
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