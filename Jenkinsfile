
pipeline {
    agent any
    environment {
        dockerImageName = 'bartrcash/webapi'
        registryCredential = 'bartrcashDocker'
        dockerImage = ''
    }

    stages {
        stage('Build') {
            steps {
                sh 'echo Building image...'

                script {
                    dockerImage = docker.build(dockerImageName + ":$BUILD_NUMBER --no-cache")
                }
            }
        }
        // stage('Test') {
        //     steps {
        //         sh 'echo Testing...'
        //         script {
        //             dockerImage.inside {
        //                 sh 'cd /usr/src/app'
        //                 sh 'npm run test'
        //             }
        //         }
        //     }
        // }

        stage('Deploy') {
            steps {
                sh 'echo Deploying....'
                script {
                    sh 'echo Pushing to docker hub...'

                    docker.withRegistry( '', registryCredential ) {
                        dockerImage.push()
                        dockerImage.push('latest')
                    }

                    sh 'echo Getting lastest image version on server...'

                    withCredentials([sshUserPrivateKey(credentialsId: 'bartrcashEC2', usernameVariable: 'USERNAME', keyFileVariable: 'KEYFILE')]) {
                        def remote = [:]
                        remote.name = 'otto-serversdsd'
                        remote.host = 'ec2-52-90-133-116.compute-1.amazonaws.com'
                        remote.user = USERNAME
                        remote.identityFile = KEYFILE
                        remote.allowAnyHosts = true
                        sshScript remote: remote, script: 'jenkins/scripts/updateDockerContainer.sh'
                    }
                }
            }
        }
    }
}
