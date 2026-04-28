from fastapi import FastAPI, WebSocket
from src.app.agents import app as agent_app
from src.app.forms import RealtorForm
import json

app = FastAPI(title="Realtor AI Agent")

@app.post("/forms/{form_type}")
async def generate_form(form_type: str, data: dict):
    state = {"form_type": form_type, "form_data": data}
    result = agent_app.invoke(state)
    form = RealtorForm(**result["form_data"])
    return {"form": form.model_dump(), "html": render_template(form)}  # Jinja2 to HTML/PDF

@app.websocket("/chat")
async def websocket_chat(websocket: WebSocket):
    await websocket.accept()
    while True:
        msg = await websocket.receive_text()
        # Agent chat loop
        response = agent_app.invoke({"messages": [msg]})
        await websocket.send_text(json.dumps(response))
