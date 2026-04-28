# Realtor Agentic AI (Python + Docker + Kubernetes)

This project provides an **agentic AI workflow** for real estate transactions:

1. Starts a document session for standard realtor forms.
2. Asks questions one-by-one to collect missing details.
3. Generates filled-out document drafts from templates.

> ⚠️ Legal note: Generated forms are drafts for workflow automation and should be reviewed by a licensed real estate professional and attorney before use.

## Included Documents

- Residential Purchase Agreement
- Seller Disclosure
- Lead-Based Paint Disclosure
- Agency Disclosure

## API Endpoints

- `POST /sessions/start` — starts a session and returns the first question.
- `POST /sessions/{session_id}/answer` — submit an answer to the current question.
- `GET /sessions/{session_id}/documents` — fetch generated filled forms after all questions are answered.
- `GET /health` — health endpoint.

## Local Run (Python)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Docker

```bash
docker build -t realtor-agentic-ai:latest .
docker run --rm -p 8000:8000 realtor-agentic-ai:latest
```

## Kubernetes

```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/ingress.yaml
```

## Test

```bash
pytest
```

