pipeline {
  
   agent any
     
         environment {
                    DOCKER_HUB_CREDS = credentials('dockerhub-creds')
                    IMAGE_NAME = "${DOCKER_HUB_CREDS_USR}/salesken-app"
                    IMAGE_TAG = "${BUILD_NUMBER}"
                     }
      stages{
         
        stage('Checkout'){
               steps{
                echo "Checking out the github..."
                 checkout scm
                    }
                          }

        stage('Build'){
          steps{
               echo "Building image: ${IMAGE_NAME}:${IMAGE_TAG}"
               sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ."
               sh "docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${IMAGE_NAME}:latest"
               }  
                      }
        
         stage('Test'){
           steps{
                 echo " Testing Docker Image...."
                 sh """
                 docker run -d --name jenkins-test-${BUILD_NUMBER} \
                 -p 5001:5000 \
                 sleep 5
                 docker ps | grep jenkins-test-${BUILD_NUMBER}
                 docker stop jenkins-test-${BUILD_NUMBER}
                 docker rm jenkins-test-${BUILD_NUMBER}
                   """
               } 
                      }

         stage('Push'){
           steps{
                echo " Pushing the Docker Image to Docker hub"
                 sh """
                echo  ${DOCKER_HUB_CREDS_PSW} |
                    docker login -u ${DOCKER_HUB_CREDS_USR} --password-stdin
                    docker push ${IMAGE_NAME}:${IMAGE_TAG}
                    docker push ${IMAGE_NAME}:latest
                    """
                  }
                     }

          stage('Cleanup'){
              steps{
                echo "Cleaning up local images....."
                sh "docker stop jenkins-test-${BUILD_NUMBER} 2>/dev/null ||true"
                sh "docker rm jenkins-test-${BUILD_NUMBER} 2>/dev/null ||true"
                sh "docker rmi ${IMAGE_NAME}:${IMAGE_TAG} 2>/dev/null ||true"
                sh "docker rmi ${IMAGE_NAME}:latest 2>/dev/null ||true"
                   } 
                          }
         }

          post { 
               success { 
                   echo "Pipeline succeeded!!! Image pushed: ${IMAGE_NAME}:${IMAGE_TAG}"
                       }
                failure {
                   echo "Pipeline failed at stage: ${STAGE_NAME}"
                        }
                 always{
                    echo "Pipeline finished. Build Number: ${BUILD_NUMBER}"
                     sh "docker rm -f jenkins-test-${BUILD_NUMBER} 2>/dev/null || true"
                       }
                }
}
