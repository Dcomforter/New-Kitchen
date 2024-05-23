pipeline {
    agent any
    stages {
        stage("Clone Repository") {
            steps {
                echo "Cloning the Repository"
                git url: "https://github.com/Dcomforter/New-Kitchen.git", branch: "master"
            }
        }
        stage("Build Image") {
            steps {
                echo "Building the Docker image"
                sh "docker build -t my-kitchen ."
            }
        }
        stage("Push to DockerHub") {
            steps {
                echo "Pushing the Docker image to Docker Hub"
                withCredentials([usernamePassword(credentialsId: "dockerHub", passwordVariable: "dockerHubPass", usernameVariable: "dockerHubUser")]) {
                    sh "docker tag my-kitchen ${env.dockerHubUser}/my-kitchen"
                    sh "docker login -u ${env.dockerHubUser} -p ${env.dockerHubPass}"
                    sh "docker push ${env.dockerHubUser}/my-kitchen"
                }
            }
        }
        stage("Deploy to Production") {
            steps {
                echo "Deploying the container"
                sh "docker-compose down && docker-compose up -d"
            }
        }        
        stage("Slack Notification") {
            steps {
                echo "Sending Slack Notification"
                slackSend(message: "Build Started: ${env.JOB_NAME} ${env.BUILD_NUMBER}, Status: ${currentBuild.currentResult}, Build URL: ${env.BUILD_URL}")
            }
        }
    }
}
