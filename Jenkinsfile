
pipeline {
    agent any
    
    environment{
        IMAGE="kitch-image:7.0"
        CONTAINER="kitch-pod"
    }

    stages {
        stage('Clone Repository') {
            steps {
                git url: "https://github.com/Dcomforter/New-Kitchen.git"
            }
        }
        
        stage('Remove Old Container') {
            steps {
                // sh "podman stop ${CONTAINER} && podman rm ${CONTAINER}"
                //sh "podman-compose down"
		sh "podman compose down"
            }
        }
        
        // stage('Remove Old Image') {
        //     steps {
        //         sh "podman rmi ${IMAGE}"
        //     }
        // }
        
        // stage('Build Image') {
        //     steps {
        //         sh "podman build -t ${IMAGE} ."
        //     }
        // }
        
        stage('Run Container') {
            steps {
                // sh "podman run -d -p 8600:8000 --name ${CONTAINER} ${IMAGE}"
                sh "podman compose up -d --build"
            }
        }
    }
    
    post {
        
        success {
            echo "Pipeline completed successfully!"
        }
        failure {
            echo "Pipeline failed."
        }
    }
}


