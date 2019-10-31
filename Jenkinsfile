podTemplate(label: 'ui-tests', containers: [
  containerTemplate(name: 'docker', image: 'docker', ttyEnabled: true, command: 'cat', envVars: [
    envVar(key: 'DOCKER_HOST', value: 'tcp://docker-host-docker-host:2375')
  ])
]) {
  node('ui-tests') {
    stage('Run Build') {
      container('docker') {
        def scmVars = checkout scm

        withCredentials([
          string(
            credentialsId: 'aws_account_id',
            variable: 'aws_account_id'
          )
        ]) {
          def awsRegistry = "${env.aws_account_id}.dkr.ecr.eu-central-1.amazonaws.com"
          docker.withRegistry("https://${awsRegistry}", "ecr:eu-central-1:ecr-credentials") {
            sh "docker build -t ${awsRegistry}/ui-tests:${env.BRANCH_NAME} -t ${awsRegistry}/ui-tests:${scmVars.GIT_COMMIT} ."
            sh "docker push ${awsRegistry}/ui-tests:${env.BRANCH_NAME}"
            sh "docker push ${awsRegistry}/ui-tests:${scmVars.GIT_COMMIT}"
          }
        }
      }
    }
  }
}
