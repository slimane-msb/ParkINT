# Cloud-Native Django Platform with Kubernetes Orchestration

> Production-grade microservices architecture deployed on Kubernetes with automated CI/CD pipeline

[![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5?style=flat&logo=kubernetes&logoColor=white)](https://kubernetes.io/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)
[![Django](https://img.shields.io/badge/Django-092E20?style=flat&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Nginx](https://img.shields.io/badge/Nginx-009639?style=flat&logo=nginx&logoColor=white)](https://nginx.org/)

## Project Overview

Enterprise-grade web application platform built with microservices architecture, featuring automated deployment pipelines, service mesh networking, and horizontal pod autoscaling. Demonstrates production-ready DevOps practices with container orchestration and infrastructure-as-code.

**Architecture Highlights**: Multi-tier Kubernetes deployment with load-balanced web services, stateful database clusters, and GitOps-driven continuous deployment.

##  System Architecture

### Infrastructure Components

```
GitHub → Docker Hub → Ingress Controller → Kubernetes Cluster
   ↓         ↓              ↓                      ↓
 Code →   Images →      Load Balancer →    Service Mesh
                                              ↓
                                    ┌─────────┴─────────┐
                                    ↓                   ↓
                              Web Services      API Services
                            (3 replicas)        (3 replicas)
                                    ↓                   ↓
                              ConfigMaps & Secrets
                                    ↓
                            Headless DB Service
                                    ↓
                          StatefulSet Database
                         (Persistent Volumes)
```

### Service Topology

**Frontend Tier (service-voiture)**:
- **Deployment**: 3 replicated pods with rolling updates
- **Service**: LoadBalancer type with ClusterIP
- **Configuration**: ConfigMaps for environment variables
- **Secrets**: Encrypted credentials management

**Backend API Tier (service-api)**:
- **Deployment**: 3 horizontally-scaled pods
- **Service**: Internal ClusterIP exposure
- **Pod naming**: `pod-voiture-api-{unique-id}`
- **Health checks**: Liveness and readiness probes

**Database Tier (StatefulSet)**:
- **Headless Service**: Direct pod addressing for database clustering
- **StatefulSet**: `svc-ma-db-0` with ordered deployment
- **Storage**: PersistentVolumeClaims for data durability
- **Pods**: `pod-ma-db-0`, `pro-ma-db-0` with stable network identities

## Technical Stack

### Core Technologies
- **Container Orchestration**: Kubernetes (K8s) with declarative YAML manifests
- **Containerization**: Docker with multi-stage builds
- **Web Framework**: Django (Python) with REST API
- **Reverse Proxy**: Nginx for load balancing and SSL termination
- **Version Control**: Git with automated webhooks
- **Registry**: Docker Hub for container image management

### Kubernetes Resources
- **Deployments**: Rolling update strategy with zero-downtime
- **Services**: ClusterIP, LoadBalancer, Headless configurations
- **ConfigMaps**: Environment-based configuration management
- **Secrets**: Base64-encoded sensitive data storage
- **StatefulSets**: Ordered pod deployment for databases
- **PersistentVolumes**: Durable storage with dynamic provisioning
- **Ingress**: Path-based routing with Nginx controller

##  Architecture Diagram

![schema 7](./docs/arch.png)

### Traffic Flow
1. **Git Push** → Triggers automated Docker image build
2. **Docker Hub** → Stores versioned container images
3. **Ingress Controller** → Routes external traffic based on paths/domains
4. **Service Mesh** → Distributes requests across pod replicas
5. **ConfigMaps/Secrets** → Injected into pods at runtime
6. **StatefulSet DB** → Provides persistent data layer

##  Deployment Guide

### Prerequisites
```bash
# Required tools
kubectl version --client
docker --version
minikube version  # or access to K8s cluster
```

### Quick Start

**1. Deploy Complete Stack**:
```bash
# Apply all Kubernetes manifests
kubectl apply -f ch7/

# Verify deployments
kubectl get deployments
kubectl get services
kubectl get pods
```

**2. Access Services**:
```bash
# Get external IP for LoadBalancer
kubectl get svc service-voiture

# Port-forward for local testing
kubectl port-forward svc/service-api 8000:8000
```

**3. Monitor Application**:
```bash
# Check pod logs
kubectl logs -f deployment/service-voiture

# Describe resources
kubectl describe pod pod-voiture-dep-4568468
```

### Useful Commands

```bash
# Clean up resources
kubectl delete all --all

# Manage persistent volumes
kubectl get pvc
kubectl delete pvc/data-claim

# Scale deployments
kubectl scale deployment service-voiture --replicas=5

# Rolling updates
kubectl set image deployment/service-api api=myimage:v2

# View configuration
kubectl get configmap config-api -o yaml
kubectl get secret secret -o yaml
```

## Project Structure

```
kubernetes-django-platform/
├── Network/                      
│   ├── README.md
│   └── service.yaml
├── deployments/                      
│   ├── README.md
│   ├── ch7.drawio.png       # Architecture diagram
│   ├── deployment-voiture.yaml
│   ├── deployment-api.yaml
│   ├── service-voiture.yaml
│   ├── service-api.yaml
│   ├── configmap.yaml
│   ├── secret.yaml
│   ├── statefulset-db.yaml
│   └── pvc.yaml
├── docker/
│   ├── Dockerfile.web
│   ├── Dockerfile.api
│   └── nginx.conf
└── src/
    ├── manage.py
    └── app/
```

## Progressive Learning Path

Each challenge folder (`ch1/`, `ch2/`, `ch7/`) contains:
- **README.md**: Step-by-step implementation guide
- **YAML manifests**: Kubernetes resource definitions
- **Diagrams**: Visual architecture documentation
- **Best practices**: Production deployment patterns

### Challenge Progression
1. **ch1**: Single pod deployment basics
2. **ch2**: Service discovery and networking
3. **ch3**: ConfigMaps and environment variables
4. **ch4**: Secrets management and security
5. **ch5**: Persistent storage with PVCs
6. **ch6**: StatefulSets for databases
7. **ch7**: Complete microservices platform

##  Security & Best Practices

### Implemented Security Measures
- **Secrets Management**: Kubernetes Secrets for sensitive data
- **RBAC**: Role-based access control (planned)
- **Network Policies**: Pod-to-pod communication restrictions
- **Resource Limits**: CPU and memory constraints per pod
- **Health Checks**: Liveness/readiness probes for reliability

### Production Considerations
- **High Availability**: Multi-replica deployments (3+ pods)
- **Zero-Downtime Deployments**: Rolling update strategy
- **Data Persistence**: StatefulSets with PersistentVolumes
- **Configuration Management**: Environment-based ConfigMaps
- **Monitoring**: Prometheus/Grafana integration (roadmap)

## Performance Metrics

### Scalability
- **Horizontal Pod Autoscaling**: Configured for 3-10 replicas based on CPU
- **Database Clustering**: StatefulSet ensures ordered scaling
- **Load Distribution**: Nginx ingress with round-robin balancing

### Reliability
- **Pod Health**: Liveness probes ensure automatic restart
- **Service Discovery**: Kubernetes DNS for inter-service communication
- **Self-Healing**: Failed pods automatically replaced

## CI/CD Pipeline

```
Code Commit → GitHub
     ↓
Docker Build → Multi-stage build optimization
     ↓
Push Image → Docker Hub (automated via webhook)
     ↓
Deploy → Kubernetes applies manifests
     ↓
Verify → Health checks confirm deployment
     ↓
Monitor → Logs and metrics collection
```

## Database Schema

**Key Entities**:
- User management with authentication
- Data models with foreign key relationships
- Migration support via Django ORM

##  Future Enhancements

- [ ] Implement Helm charts for templated deployments
- [ ] Add Prometheus/Grafana monitoring stack
- [ ] Configure Horizontal Pod Autoscaler (HPA)
- [ ] Set up GitOps with ArgoCD
- [ ] Implement service mesh (Istio/Linkerd)
- [ ] Add CI/CD with GitHub Actions
- [ ] Configure cert-manager for automatic SSL
- [ ] Implement blue-green deployment strategy

##  Learning Resources

Each challenge folder contains detailed explanations of:
- Kubernetes concepts and resource types
- Networking and service discovery
- Storage orchestration
- Configuration management
- Security best practices

##  Contributing

This project demonstrates progressive Kubernetes learning through practical challenges. Each folder is self-contained with complete documentation.

---

**Built with Cloud-Native Technologies** | Demonstrates expertise in container orchestration, microservices architecture, and DevOps automation