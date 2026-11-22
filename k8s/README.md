# Kubernetes deployment

Build/load image first (`docker build -t taskflow:local .`; for kind use `kind load docker-image taskflow:local`).
Create secrets out-of-band:
```bash
kubectl create namespace taskflow
kubectl -n taskflow create secret generic taskflow-secret --from-literal=SECRET_KEY="$(python -c 'import secrets;print(secrets.token_hex(32))')" --from-literal=DATABASE_URL='postgresql+psycopg://taskflow:CHANGE_ME@postgres:5432/taskflow'
kubectl -n taskflow create secret generic postgres-secret --from-literal=password='CHANGE_ME'
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/pvc.yaml -f k8s/postgres.yaml
kubectl apply -f k8s/deployment-blue.yaml -f k8s/service.yaml
```
Blue/green: apply `deployment-green.yaml`, wait for rollout, then switch Service selector with `kubectl -n taskflow patch svc taskflow --type merge -p '{"spec":{"selector":{"app":"taskflow","track":"green"}}}'`. Roll back by switching `track` to `blue`.
For rolling updates use `kubectl set image deployment/taskflow-blue web=YOUR_REGISTRY/taskflow:TAG -n taskflow`, then `kubectl rollout status` and `kubectl rollout undo`.
