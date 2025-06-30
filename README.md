# Event Booking Microservices Platform

## Contributors

* Ayaan Khan (22i-0832)
* Minahil Ali (22i-0849)
* Mishal Ali (22i-1291)

## Table of Contents

1. Project Overview
2. Architecture Overview
3. Microservices Explained
4. DevOps Stack and Workflows

   * Docker and Docker Compose
   * Kubernetes
   * GitHub Actions CI/CD
   * Terraform (Infrastructure as Code)
   * Ansible (Configuration Management)
   * Argo CD (GitOps Continuous Delivery)
   * Prometheus & Grafana (Monitoring & Observability)
5. Setup Instructions
6. Testing Each Component
7. Project Structure
8. API Documentation
9. Git Workflow
10. License

---

## 1. Project Overview

This project is a fully containerized microservices-based Event Booking platform built with DevOps-first principles. The system supports user registration, event listings, ticket bookings, payment processing, and notifications. Every major DevOps lifecycle aspect—CI/CD, Infrastructure Provisioning, Configuration Management, Observability, and GitOps-based delivery—is implemented using cutting-edge tools like:

* Docker & Docker Compose
* Kubernetes
* GitHub Actions
* Argo CD
* Terraform
* Ansible
* Prometheus
* Grafana

---

## 2. Architecture Overview

The application is composed of the following microservices:

* User Service (FastAPI + PostgreSQL)
* Event Service (Node.js + MongoDB)
* Booking Service (Flask + PostgreSQL + RabbitMQ)
* Notification Service (Express.js + MongoDB + RabbitMQ)

All services are containerized and communicate via REST APIs and message queues. Metrics endpoints are exposed for monitoring via Prometheus and Grafana.

---

## 3. Microservices Explained

| Microservice         | Tech Stack                    | Responsibilities                        |
| -------------------- | ----------------------------- | --------------------------------------- |
| User Service         | FastAPI, PostgreSQL           | Authentication, user profiles, frontend |
| Event Service        | Node.js, MongoDB              | CRUD operations for events              |
| Booking Service      | Flask, PostgreSQL, RabbitMQ   | Bookings, payments, publishes events    |
| Notification Service | Express.js, MongoDB, RabbitMQ | Sends emails/alerts based on bookings   |

---

## 4. DevOps Stack and Workflows

### Docker and Docker Compose

Each service has a Dockerfile. The docker-compose.yml builds and starts all services:

Start:

docker-compose up --build -d

Stop:

docker-compose down -v

Docker allows consistent local and cloud execution.

### Kubernetes

Used for production-grade orchestration of services.

Apply manifests in sequence:

kubectl apply -f kubernetes/namespace.yaml
kubectl apply -f kubernetes/deployment-service-\*.yaml
kubectl apply -f kubernetes/secrets.yaml
kubectl apply -f kubernetes/configmap.yaml
kubectl apply -f kubernetes/ingress.yaml

Ingress is configured via NGINX.

Test locally using:

kubectl port-forward svc/user-service 8000:80 -n online-event-booking-ayaankhan

### GitHub Actions (CI/CD)

Each microservice has its own GitHub Actions workflow (.github/workflows/):

On every push or PR to main:

* Builds Docker image
* Pushes to Docker Hub
* Updates Kubernetes Deployment YAML with new image tag
* Commits back for Argo CD

CI and CD are completely automated.

### Argo CD (GitOps Delivery)

* Monitors Kubernetes YAML manifests in GitHub
* Auto-syncs changes to live Kubernetes cluster
* Hosted on localhost:8081 (via port forwarding)
* Login using initial admin password

Deploy Application:

kubectl apply -f kubernetes/argocd-application.yaml

Monitor:

argocd app list
argocd app sync online-event-booking

### Terraform (Infrastructure Provisioning)

Provisions AWS EC2 infrastructure via IaC.

Steps:

cd terraform
terraform init
terraform plan
terraform apply

* Automatically creates EC2 instance
* Outputs public IP
* SSH using private key

Example:

ssh -i \~/.ssh/id\_rsa ec2-user@<public-ip>

### Ansible (Configuration Management)

Once EC2 is created, configure via:

cd ansible
ansible-playbook site.yml

This:

* Installs Docker, Docker Compose
* Deploys services
* Opens necessary ports

Verify via:

ssh into EC2
docker ps
curl [http://localhost](http://localhost)

### Prometheus & Grafana (Monitoring & Observability)

Instrumented metrics from:

* User and Booking (Python: prometheus-fastapi-instrumentator)
* Event and Notification (Node.js: prom-client)

Helm charts used for deployment:

helm repo add prometheus-community [https://prometheus-community.github.io/helm-charts](https://prometheus-community.github.io/helm-charts)
helm repo add grafana [https://grafana.github.io/helm-charts](https://grafana.github.io/helm-charts)
helm install prometheus prometheus-community/prometheus --namespace monitoring --create-namespace
helm install grafana grafana/grafana --namespace monitoring

Access:

kubectl port-forward svc/prometheus-server 9090:80 -n monitoring
kubectl port-forward svc/grafana 3000:80 -n monitoring

Grafana credentials decoded from Kubernetes secret.

---

## 5. Setup Instructions

1. Clone Repository

git clone [https://github.com/AyaanKhan1576/Event-Booking-Microservices-DevOps-Project.git](https://github.com/AyaanKhan1576/Event-Booking-Microservices-DevOps-Project.git)

2. Setup Environment Files

For each service (user, booking, event, notification), copy .env.example → .env and set appropriate DB URLs, keys, ports.

3. Local Run via Docker Compose

docker-compose up --build -d

4. Kubernetes Setup

cd kubernetes
Apply all manifests as described earlier.

5. Argo CD Setup

kubectl apply -f argocd-namespace.yaml
kubectl apply -n argocd -f [https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml](https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml)
Expose ArgoCD:

kubectl port-forward svc/argocd-server -n argocd 8081:443

6. Terraform + Ansible Deployment

terraform apply
Copy IP and SSH into EC2
ansible-playbook site.yml

---

## 6. Testing Each Component

* Test APIs: Postman / curl endpoints.
* Test RabbitMQ: Use test-producer.js in notification-service.
* Check Prometheus targets at localhost:9090
* Monitor Grafana dashboards at localhost:3000
* Confirm deployments via: kubectl get pods -n online-event-booking-ayaankhan

---

## 7. Project Structure

See the full project structure inside README above or explore directories:

* user-service/
* booking-service/
* new-event-service/
* notification-service/
* terraform/
* ansible/
* kubernetes/
* .github/workflows/

---

## 8. API Documentation

User Service:

* POST /register
* POST /login
* GET /users/{id}

Event Service:

* GET /events
* GET /events/{id}

Booking Service:

* POST /book
* GET /bookings/{user\_id}

Notification Service:

* GET /notifications/{user\_id}

All services return JSON.

---

## 9. Git Workflow

git checkout -b feature-branch

# make changes

git add .
git commit -m "new feature"
git push origin feature-branch

---

## 10. License

This project is licensed under the MIT License.
