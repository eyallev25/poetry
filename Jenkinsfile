pipeline {
    parameters {
            string(name: 'cluster_name', description: 'Cluster name.', defaultValue:"agent-tests")
        }
    triggers {
             cron('0 2 * * *')
         }
    agent any
    environment {
        BRANCH_NAME_FULL = "develop"
        EKS_CLUSTER = "${params.cluster_name}"
        CLUSTER_NAME="${BRANCH_NAME_FULL.hashCode()}-${BUILD_NUMBER}"
        
    }
    stages {
        stage('Build') {
            steps {
                echo 'Building..'
                echo "Hello ${params.cluster_name}"
                echo "${CLUSTER_NAME}"
                echo "${EKS_CLUSTER}"

                
                }
        }
        
        
    }
}