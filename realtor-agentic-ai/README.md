# Realtor AI Agent
Agentic AI for realtors: conversational form filling → compliant docs.

## Quickstart (Local)
poetry install && uvicorn src.app.main:app --reload

## K8s Deploy
1. Push image.
2. kustomize build overlays/dev | kubectl apply -f -

## Endpoints
- POST /forms/listing {json data} → Filled form HTML/JSON
- WS /chat → Interactive agent

