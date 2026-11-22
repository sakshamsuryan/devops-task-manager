pipeline {
  agent any
  environment { IMAGE = "taskflow:${BUILD_NUMBER}" }
  stages {
    stage('Checkout') { steps { checkout scm } }
    stage('Install & Test') {
      steps {
        sh 'python3 -m venv .venv'
        sh '. .venv/bin/activate && pip install -r requirements.txt'
        sh '. .venv/bin/activate && pytest -q'
      }
    }
    stage('Static Analysis') {
      steps {
        withSonarQubeEnv('SonarQube') {
          sh 'sonar-scanner -Dsonar.projectKey=taskflow -Dsonar.sources=app -Dsonar.tests=tests'
        }
      }
    }
    stage('Build Image') { steps { sh 'docker build -t $IMAGE .' } }
    stage('Image Scan') { steps { sh 'trivy image --exit-code 1 --severity HIGH,CRITICAL $IMAGE' } }
    stage('Push Image') {
      when { branch 'main' }
      steps {
        withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'REG_USER', passwordVariable: 'REG_PASS')]) {
          sh 'echo "$REG_PASS" | docker login -u "$REG_USER" --password-stdin'
          sh 'docker tag $IMAGE "$REG_USER/taskflow:$BUILD_NUMBER"'
          sh 'docker push "$REG_USER/taskflow:$BUILD_NUMBER"'
        }
      }
    }
  }
  post { always { junit allowEmptyResults: true, testResults: 'test-results/*.xml'; cleanWs() } }
}
