from fastapi import FastAPI, HTTPException, BackgroundTasksfrom fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Dict, Any, Optional
import uvicorn
import asyncio
import os

from agents.conversation_agent import ConversationAgent
from agents.document_agent import DocumentAgent
from agents.validation_agent import ValidationAgent

app = FastAPI(title="Realtor AI Agent", version="1.0.0")

# Initialize agents
conversation_agent = ConversationAgent()
document_agent = DocumentAgent()
validation_agent = ValidationAgent()

# Store session data (in production use Redis)
sessions = {}

class MessageRequest(BaseModel):
session_id: str
message: str

class DocumentRequest(BaseModel):
session_id: str
document_type: str = "all"

@app.post("/chat")
async def chat(request: MessageRequest):
"""Process chat messages and continue conversation"""
if request.session_id not in sessions:
sessions[request.session_id] = {"conversation": ConversationAgent(), "data": {}}

session = sessions[request.session_id]
response = await session["conversation"].process({"message": request.message})

if response["type"] == "complete":
# Validate the collected data
validation = await validation_agent.process(response["data"])
if validation.get("errors"):
return {"type": "validation_error", "errors": validation["errors"]}

session["data"] = response["data"]
return response

return response

@app.post("/generate-documents")
async def generate_documents(request: DocumentRequest, background_tasks: BackgroundTasks):
"""Generate requested documents"""
if request.session_id not in sessions:
raise HTTPException(status_code=404, detail="Session not found")

session = sessions[request.session_id]
if not session["data"]:
raise HTTPException(status_code=400, detail="No property data available")

result = await document_agent.process({
"property_data": session["data"],
"document_type": request.document_type
})

# Store document paths in session
session["documents"] = result["documents"]

return result

@app.get("/download/{session_id}/{document_type}")
async def download_document(session_id: str, document_type: str):
"""Download a generated document"""
if session_id not in sessions:
raise HTTPException(status_code=404, detail="Session not found")

session = sessions[session_id]
documents = session.get("documents", [])

for doc in documents:
if doc["type"] == document_type:
if os.path.exists(doc["path"]):
return FileResponse(
doc["path"],
media_type="application/pdf",
filename=f"{document_type}_{session_id}.pdf"
)

raise HTTPException(status_code=404, detail="Document not found")

@app.get("/health")
async def health_check():
return {"status": "healthy", "agents": "ready"}

if __name__ == "__main__":
uvicorn.run(app, host="0.0.0.0", port=8000)
