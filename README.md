# TaskFlow – DevOps Capstone

A full-stack Flask + PostgreSQL task manager and DevOps capstone implementation aligned to ENSP461.

## Features
- Registration, login/logout, hashed passwords and CSRF protection.
- Role-based access (`user` and `admin`); users only access their own tasks, admins can access all tasks and list users.
- Task CRUD through REST API and responsive dashboard.
- Health (`/health`) and Prometheus metrics (`/metrics`) endpoints.
- Docker/Compose, Kubernetes blue-green manifests, Jenkins CI, Ansible, Terraform, Prometheus/Grafana and ArgoCD examples.

## Run locally (Ubuntu WSL2 / Linux / macOS)
```bash
git clone <your-repository-url>
cd devops-task-manager
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit SECRET_KEY and passwords in .env before use
python run.py
```
Open http://localhost:5000. SQLite is used by default if DATABASE_URL is not set. For a quick local test this avoids requiring PostgreSQL.

## Run with Docker Compose
```bash
cp .env.example .env
# Change SECRET_KEY and POSTGRES_PASSWORD; ensure DATABASE_URL is not hardcoded in .env
docker compose up --build -d
docker compose ps
docker compose logs -f web
```
Open http://localhost:5000. Stop with `docker compose down`; preserve database with `docker compose down` (volume remains), remove data only with `docker compose down -v`.

## API
All API routes require a logged-in session (browser session cookie).
| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/tasks` | List accessible tasks |
| POST | `/api/tasks` | Create task |
| GET | `/api/tasks/{id}` | Get task |
| PUT/PATCH | `/api/tasks/{id}` | Update task |
| DELETE | `/api/tasks/{id}` | Delete task |
| GET | `/api/admin/users` | Admin-only user list |
| GET | `/health` | Health check |
| GET | `/metrics` | Prometheus metrics |

POST/PATCH JSON example:
```json
{"title":"Prepare demo","description":"Record walkthrough","status":"in_progress","priority":"high","due_date":"2026-12-01"}
```

## Tests
```bash
pytest -q
```

## DevOps labs
- Git: create GitHub repository, branches, merge, and commit history.
- Jenkins: configure a Pipeline job from SCM; install/configure SonarQube, Docker CLI/daemon, Trivy and a SonarQube server; create Jenkins credentials `dockerhub-creds`; configure SonarQube server name `SonarQube`. Configure a GitHub webhook to trigger builds on push.
- Docker: `docker build -t taskflow:local .`; `docker compose up --build`.
- Kubernetes: follow `k8s/README.md`; build/load image into the local cluster first. Kubernetes manifests are templates; supply real secrets out-of-band.
- Blue-green: deploy both colors and patch Service selector as described in `k8s/README.md`.
- Ansible: `ansible-playbook -i ansible/inventory.ini ansible/configure-host.yml`; other playbooks may require sudo and a real Kubernetes context.
- Terraform: `cd terraform && terraform init && terraform plan && terraform apply`; uses Docker provider and builds the local image. `terraform destroy` removes the Terraform-managed image resource.
- Monitoring: `docker compose -f compose.yaml -f monitoring/compose.monitoring.yaml up --build`; Prometheus :9090, Grafana :3000. Add a Prometheus data source `http://prometheus:9090` in Grafana.
- Logging: app logs are stdout/stderr and available via `docker compose logs`. Run the ELK stack with `docker compose -f compose.yaml -f logging/compose.logging.yaml up -d`; Kibana is at :5601 and Elasticsearch at :9200. Filebeat reads Docker container JSON logs and forwards them through Logstash. This lab stack disables Elasticsearch security and must not be exposed publicly.
- GitOps: install Argo CD in a Kubernetes cluster, update `gitops/argocd-application.yaml` with your GitHub URL, then `kubectl apply -f gitops/argocd-application.yaml -n argocd`.

## Important production notes
This is a lab implementation, not a hardened production deployment. Replace all example credentials. Use TLS, secure cookies, managed secrets, least-privilege Kubernetes RBAC, database migrations/backups, network policies, resource quotas and image signing before production. The Kubernetes PostgreSQL manifest is a single-replica lab example.

## Evidence checklist
Capture: registration/login; task create/update/delete; pytest output; Jenkins stages; SonarQube quality gate; Trivy scan; Docker containers; Kubernetes pods/services/rollout/rollback; Ansible play recap; Terraform plan/apply; Prometheus target; Grafana dashboard; log records; ArgoCD sync; blue-green service selector before/after.
