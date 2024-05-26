# Task Management API

## Introduction

This project is a simple REST API server for managing a task list. It provides endpoints to create, update, delete, and
view tasks. The application is containerized, deployed on a Kubernetes cluster, exposed using a loadbalancer and includes
monitoring with the Kube Prometheus Stack.

The CI/CD pipeline is automated using GitHub Actions.
    
    
## Setup and Installation
       
### Prerequisites

- Docker
- Kubernetes cluster (e.g., minikube, EKS, GKE, AKS)
- kubectl 
- Helm
- GitHub account

### Installation Steps

1. **Clone the repository:**
    
    ```bash
    git clone https://github.com/DevOpsGodd/Build-and-deploy-REST-Api-server.git
    cd task-api 
    ```

2. **Build the Docker image:**

    ```bash
    docker build -t yourusername/task-api:latest .
    ```

3. **Push the Docker image to a registry:**

    ```bash 
    docker push yourusername/task-api:latest
    ```

## API Endpoints
    
| Method | Endpoint        | Description          |
|--------|-----------------|----------------------|
| POST   | /tasks          | Create a new task    |
| PUT    | /tasks/{id}     | Update an existing task |
| DELETE | /tasks/{id}     | Delete a task        |
| GET    | /tasks          | View all tasks       |
    
## Containerization

The application is containerized using Docker. The Dockerfile is located in the `root` directory of the project.

```
# Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY app.py app.py

CMD ["python", "app.py"]
```

## Kubernetes Deployment

The Kubernetes deployment files are located in the k8s directory.

- `deployment.yaml:` Defines the Deployment for the task API.
- `svc.yaml:` Defines the Service to expose the Deployment using a LoadBalancer.


## Deploying to Kubernetes

Apply the deployment and service files:

```
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/svc.yaml
```

## CI/CD Pipeline

The CI/CD pipeline is automated using GitHub Actions. The workflow file is located in `.github/workflows/deploy.yml.`

**Key Steps in the Pipeline:**

- Build the Docker image
- Push the image to Docker Hub
- Deploy the application to Kubernetes
- Deploy the Kube Prometheus Stack for monitoring

```
name: Uthman CI/CD Pipeline

on:
  push:
    branches:
      - main

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout repository
      uses: actions/checkout@v2

    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'

    - name: Install dependencies
      run: |
        python -m venv venv
        . venv/bin/activate
        pip install -r requirements.txt
        pip install pytest

    - name: Upgrade Flask
      run: |
        source venv/bin/activate
        pip install --upgrade flask    

    - name: Run tests
      run: |
        . venv/bin/activate
        pytest

    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v1

    - name: Login to Docker Hub
      uses: docker/login-action@v2
      with:
        username: ${{ secrets.DOCKER_USERNAME }}
        password: ${{ secrets.DOCKER_PASSWORD }}

    - name: Build and push Docker image
      uses: docker/build-push-action@v2
      with:
        context: .
        push: true
        tags: uthycloud/task-api:latest

    - name: Set up kubectl
      uses: azure/setup-kubectl@v3
      with:
        version: 'latest'
        
    - name: Create .kube directory
      run: mkdir -p $HOME/.kube

    - name: Set up kubeconfig
      run: echo "${{ secrets.KUBE_CONFIG }}" | base64 --decode > $HOME/.kube/config

    - name: Verify kubeconfig
      run: kubectl config view
    
    - name: Deploy to Kubernetes
      run: |
        kubectl apply --validate=false -f k8s/deployment.yaml
        kubectl apply --validate=false -f k8s/svc.yaml

    - name: Set up Helm
      uses: azure/setup-helm@v1
      with:
        version: v3.6.3

    - name: Add Helm repo
      run: |
        helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
        helm repo update

    - name: Install Kube Prometheus Stack
      run: |
        helm install prometheus prometheus-community/kube-prometheus-stack
```

![Post Deployment Snapshot](images/post%20deployment.png)


Here are the pods and services running in my cluster, the application and monitoring stack inclusive.

![Pods and Services Overview](images/pods%20&%20services.png)

And here is our deployment with our application `task-api-deployment` running on 3 replicas. 

![Deployment Diagram](images/deployment.png)


## Monitoring with Kube Prometheus Stack

The Kube Prometheus Stack is deployed on the same Kubernetes cluster for monitoring.

**Steps to Deploy:**

- Add the Helm repository for Prometheus:

```
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
```

- Install the Kube Prometheus Stack:

```
helm install prometheus prometheus-community/kube-prometheus-stack
```

- Access Grafana:

Obtain the Grafana admin password:

```
kubectl get secret --namespace default prometheus-grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo
```

- Forward the Grafana port to your local machine:
```
kubectl port-forward service/prometheus-grafana 3000:80
```


- Access Grafana at `http://localhost:3000` and log in with the username admin and the password obtained in the previous 
step.


This is my prometheus successfully queried

![Prometheus Queried Metrics](images/prometheus%20queried.png)

This is my Grafana Dashboard

![Grafana Dashboard](images/grafana%20dashboard.png)

## Usage

After deployment, the Task API can be accessed through the LoadBalancer service. You can use tools like curl or Postman to 
interact with the API.

![Task GUI](images/taskgui.png)

Example:

### Create a new task

```
curl -X POST http://<load-balancer-ip>/tasks -d '{"title": "New Task", "description": "Task description"}' -H 
"Content-Type: application/json"
```
![Task CLI](images/taskcli.png)

## Conclusion

This project demonstrates a full cycle of application development and deployment, including containerization, Kubernetes 
deployment, CI/CD automation, and monitoring. 

This README serves as documentation to guide through each step and ensure the process is reproducible.

