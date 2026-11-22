# Technical Report: TaskFlow – End-to-End DevOps Pipeline

## Abstract
TaskFlow is a containerized task management web application delivered through an automated DevOps workflow. It combines version control, continuous integration, containerization, orchestration, infrastructure automation, monitoring, logging, security checks, blue-green delivery and GitOps.

## Problem Statement
Manual software delivery is slow, error-prone and difficult to reproduce. The project demonstrates an automated, observable and repeatable delivery process for a practical web application.

## Objectives
- Implement authenticated task management with persistent storage and REST APIs.
- Automate build, tests, static analysis and image security scanning.
- Deploy the application with Docker and Kubernetes.
- Automate host/configuration tasks with Ansible and infrastructure artifacts with Terraform.
- Monitor application metrics and centralize container logs.
- Demonstrate blue-green switching and GitOps reconciliation.

## Scope and requirements
The application supports registration, login, logout, user-scoped CRUD, admin user listing, validation, health and metrics endpoints, and responsive UI. DevOps requirements map to the Jenkinsfile, Docker assets, `k8s/`, `ansible/`, `terraform/`, `monitoring/`, `logging/`, `gitops/`, and security configuration.

## Architecture
See `architecture.mmd`. Developer commits are pushed to GitHub. Jenkins checks out source, installs dependencies, runs pytest, executes SonarQube analysis, builds a Docker image and scans it with Trivy. The image is published on main when registry credentials are configured. ArgoCD watches the Kubernetes manifest path and reconciles desired state. Kubernetes exposes the app and runs PostgreSQL with persistent storage. Prometheus scrapes Flask metrics; Grafana visualizes them.

## Technology stack
Python 3.12, Flask, Flask-SQLAlchemy, Flask-Login, Flask-WTF, PostgreSQL, Bootstrap, JavaScript, Git/GitHub, Jenkins, Docker, Kubernetes, Ansible, Terraform Docker provider, Prometheus, Grafana, SonarQube, Trivy and ArgoCD.

## Database design
`User(id, name, email, password_hash, role, created_at)` has a one-to-many relationship with `Task(id, title, description, status, priority, due_date, created_at, updated_at, user_id)`. Email is unique; `Task.user_id` references `User.id`. Task records are scoped to their owner unless the authenticated account has the administrator role.

## DFD and UML
Context/architecture diagram: `architecture.mmd`. Core use case: user registers/logs in, creates and manages tasks through Flask routes/API, and PostgreSQL persists records. Entity relationship: User 1 — * Task. Deployment blue-green is represented by two Kubernetes Deployments and a Service selector.

## Implementation
The Flask application is organized into auth, main, tasks and model modules. SQLAlchemy handles persistence; Werkzeug provides password hashing; Flask-Login manages sessions; Flask-WTF protects form POSTs with CSRF. API endpoints return JSON and enforce ownership and role checks. Docker Compose runs the web app and PostgreSQL. Kubernetes manifests include Deployment, Service, ConfigMap, Secret template and PVC.

## Testing and results
Automated tests are in `tests/`. Run `pytest -q`. Record actual test output, environment versions, deployment rollout output, screenshots and measured results during your demonstration. Do not report unexecuted checks as passed.

## Security
Passwords are hashed; sessions use HttpOnly and SameSite cookies; form CSRF protection is enabled; secrets are supplied through environment variables/Kubernetes Secrets/Jenkins Credentials; container runs as non-root; Trivy scans the built image; SonarQube performs static analysis. Production deployment must set a strong SECRET_KEY, secure cookies, TLS, database backups, network policies and restricted RBAC.

## Challenges
Document environment-specific issues encountered during installation, image loading, service exposure, credentials and cluster connectivity. Include the exact resolution and evidence.

## Future scope
Add email notifications, automated backups, Helm packaging, Ingress/TLS, richer audit logs, autoscaling validation, managed cloud infrastructure and AI-assisted log anomaly detection.

## Conclusion
TaskFlow provides a practical application and a modular reference implementation of an end-to-end DevOps pipeline. Successful completion is demonstrated by evidence from tests, pipeline runs, container health, Kubernetes rollout, metrics, logs, security scans and GitOps sync.

## References
- Flask documentation: https://flask.palletsprojects.com/
- Docker documentation: https://docs.docker.com/
- Kubernetes documentation: https://kubernetes.io/docs/
- Jenkins Pipeline documentation: https://www.jenkins.io/doc/book/pipeline/
- Prometheus documentation: https://prometheus.io/docs/
- Terraform documentation: https://developer.hashicorp.com/terraform/docs
- Ansible documentation: https://docs.ansible.com/
- Argo CD documentation: https://argo-cd.readthedocs.io/
