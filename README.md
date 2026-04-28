# Realtor AI Agent System
An intelligent multi-agent system that automatically generates real estate documents through conversational AI.

## Features

- 🤖 **Conversational Agent**: Natural language interaction to gather property information
- 📄 **Document Generation**: Creates Purchase Agreements, Listing Agreements, and Disclosure Forms
- ✅ **Validation Agent**: Ensures all required information is complete and valid
- 🐳 **Dockerized**: Complete containerization for easy deployment
- ☸️ **Kubernetes Ready**: Production-grade orchestration with auto-scaling
- 🔄 **Session Management**: Persistent conversations with progress tracking

## Quick Start

### Prerequisites
- Docker & Docker Compose
- Kubernetes cluster (for production)
- OpenAI API key

### Local Development
```bash
# Clone repository
git clone https://github.com/yourusername/realtor-ai-agent.git
cd realtor-ai-agent

# Set up environment
cp .env.example .env
# Add your OPENAI_API_KEY to .env

# Run with docker-compose
docker-compose -f docker/docker-compose.yml up

# Test the API
curl -X POST http://localhost:8000/chat \
-H "Content-Type: application/json" \
-d '{"session_id":"test123","message":"123 Main St"}'
