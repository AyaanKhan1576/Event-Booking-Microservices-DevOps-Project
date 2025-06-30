# Event Booking Microservices with DevOps Automation

## Contributors

* Ayaan Khan  (22i-0832)
* Minahil Ali (22i-0849)
* Mishal Ali  (22i-1291)

---

## 1. Project Overview

This project implements a cloud-native Event Booking System using a microservices architecture. The platform allows users to:

* Register and manage accounts
* Browse and book events
* Receive notifications after successful booking

Each feature is modularized into dedicated services that communicate via REST and RabbitMQ. The system is containerized with Docker, orchestrated via Kubernetes, and automated using a complete DevOps stack (CI/CD, GitOps, Infrastructure as Code, Monitoring, and Configuration Management).

---

## 2. Microservices Overview

| Service              | Language | Database   | Purpose                                    |
| -------------------- | -------- | ---------- | ------------------------------------------ |
| user-service         | FastAPI  | PostgreSQL | Manages registration, login, profiles      |
| booking-service      | Flask    | PostgreSQL | Books events, processes payments, RabbitMQ |
| new-event-service    | Node.js  | MongoDB    | Event CRUD and discovery                   |
| notification-service | Node.js  | MongoDB    | Consumes booking events and notifies users |

Services are completely decoupled and interact via REST APIs and asynchronous message queues (RabbitMQ).

---

## 3. System Architecture

### Logical Architecture

* User interacts via a frontend (templated HTML rendered by user-service)
* Each service runs independently in containers
* Booking triggers RabbitMQ messages consumed by notification-service

### Tech Stack

| Component          | Stack                   |
| ------------------ | ----------------------- |
| Backend Services   | FastAPI, Flask, Node.js |
| Messaging Queue    | RabbitMQ                |
| Databases          | PostgreSQL, MongoDB     |
| Containerization   | Docker, Docker Compose  |
| Orchestration      | Kubernetes              |
| GitOps             | Argo CD                 |
| CI/CD              | GitHub Actions          |
| Infra Provisioning | Terraform               |
| Configuration Mgmt | Ansible                 |
| Monitoring         | Prometheus + Grafana    |

---

## 4. DevOps Stack and Workflows

### Docker and Docker Compose

All microservices include Dockerfiles.

To build and run everything locally:

Start all containers:

```bash
docker-compose up --build -d
```

Stop and remove all containers and volumes:

```bash
docker-compose down -v
```

Docker ensures consistent builds and isolated environments.

---

### Kubernetes

Used to orchestrate production workloads with resilience and scalability.

Apply manifests in sequence:

```bash
kubectl apply -f kubernetes/namespace.yaml
kubectl apply -f kubernetes/deployment-service-*.yaml
kubectl apply -f kubernetes/secrets.yaml
kubectl apply -f kubernetes/configmap.yaml
kubectl apply -f kubernetes/ingress.yaml
```

Ingress Controller is managed via NGINX. You can use the following command to test locally:

```bash
kubectl port-forward svc/user-service 8000:80 -n online-event-booking-ayaankhan
```

---

### GitHub Actions (CI/CD)

Each microservice has its own CI workflow in .github/workflows/

Actions include:

* On push or pull request to main branch
* Build Docker image
* Push to Docker Hub
* Update Kubernetes deployment YAML with new image tag
* Commit and push changes (for Argo CD auto-sync)

CI/CD is fully automated and follows modern DevOps practices.

---

### Argo CD (GitOps Delivery)

* Monitors GitHub repository for changes to Kubernetes manifests
* Auto-syncs changes to live Kubernetes cluster
* Port-forwarded to localhost:8081 for local access

Deploy the application:

```bash
kubectl apply -f kubernetes/argocd-application.yaml
```

Monitor Argo CD state:

```bash
argocd app list
argocd app sync online-event-booking
```

You can access the UI:

* URL: [http://localhost:8081](http://localhost:8081)
* Username: admin
* Password: Retrieved from Kubernetes secret

---

### Terraform (Infrastructure Provisioning)

Terraform provisions AWS infrastructure via Infrastructure-as-Code.

Steps:

```bash
cd terraform
terraform init
terraform plan
terraform apply
```

Outputs an EC2 instance public IP.

SSH into instance:

```bash
ssh -i ~/.ssh/id_rsa ec2-user@<public-ip>
```

---

### Ansible (Configuration Management)

Once EC2 instance is ready, Ansible configures it:

```bash
cd ansible
ansible-playbook site.yml
```

Installs:

* Docker
* Docker Compose
* Clones repo
* Deploys microservices

Verify deployment:

```bash
ssh ec2-user@<public-ip>
docker ps
curl http://localhost
```

---

### Prometheus & Grafana (Monitoring & Observability)

Services are instrumented with Prometheus clients:

* user-service and booking-service: prometheus-fastapi-instrumentator
* event-service and notification-service: prom-client and express-prom-bundle

Steps:

Install Helm:

```bash
choco install kubernetes-helm
```

Add Helm Repositories:

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update
```

Install Prometheus and Grafana:

```bash
helm install prometheus prometheus-community/prometheus --namespace monitoring --create-namespace
helm install grafana grafana/grafana --namespace monitoring
```

Port forward to access dashboards:

```bash
kubectl port-forward svc/prometheus-server 9090:80 -n monitoring
kubectl port-forward svc/grafana 3000:80 -n monitoring
```

Grafana credentials are stored in a Kubernetes secret. Retrieve them via:

```powershell
$encoded = kubectl get secret --namespace monitoring grafana -o jsonpath="{.data.admin-password}"
[System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String($encoded))
```

---

## 5. Setup Instructions

### Step 1: Clone Repository

```bash
git clone https://github.com/AyaanKhan1576/Event-Booking-Microservices-DevOps-Project.git
cd Event-Booking-Microservices-DevOps-Project
```

---

### Step 2: Setup Environment Files

For each microservice directory (user-service, booking-service, new-event-service, notification-service):

* Copy .env.example to .env
* Update the DB URLs, secret keys, and service URLs accordingly

---

### Step 3: Local Development via Docker Compose

Run all services locally:

```bash
docker-compose up --build -d
```

Stop and clean up:

```bash
docker-compose down -v
```

---

### Step 4: Kubernetes Setup

```bash
cd kubernetes
kubectl apply -f namespace.yaml
kubectl apply -f deployment-service-postgres.yaml
kubectl apply -f deployment-service-mongodb.yaml
kubectl apply -f deployment-service-rabbitmq.yaml
kubectl apply -f deployment-service-user.yaml
kubectl apply -f deployment-service-event.yaml
kubectl apply -f deployment-service-booking.yaml
kubectl apply -f deployment-service-notification.yaml
kubectl apply -f configmap.yaml
kubectl apply -f secrets.yaml
kubectl apply -f ingress.yaml
```

To test locally:

```bash
kubectl port-forward svc/user-service 8000:80 -n online-event-booking-ayaankhan
```

---

### Step 5: Argo CD Setup

Install Argo CD:

```bash
kubectl apply -f argocd-namespace.yaml
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

Expose Argo CD:

```bash
kubectl port-forward svc/argocd-server -n argocd 8081:443
```

Get the admin password:

```powershell
$b64 = kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}"
$bytes = [Convert]::FromBase64String($b64)
[Text.Encoding]::UTF8.GetString($bytes)
```

Deploy the Argo CD application:

```bash
kubectl apply -f kubernetes/argocd-application.yaml
```

Sync the app:

```bash
argocd app sync online-event-booking
```

---

### Step 6: Provision Infrastructure via Terraform

```bash
cd terraform
terraform init
terraform plan
terraform apply
```

Copy the EC2 instance IP and SSH:

```bash
ssh -i ~/.ssh/id_rsa ec2-user@<public-ip>
```

---

### Step 7: Deploy with Ansible

Ensure IP and private key are updated in inventory.ini.

Run the playbook:

```bash
cd ansible
ansible-playbook site.yml
```

---

## 6. Git Workflow

```bash
git checkout -b feature-branch
# Make changes
git add .
git commit -m "Add feature"
git push origin feature-branch
```

---

## 7. License

This project is licensed under the MIT License. See LICENSE for details.
