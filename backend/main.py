from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os
import json
from dotenv import load_dotenv
from backend.agent import run_agent

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

app = FastAPI(title="ResolveMind API")

class ChatRequest(BaseModel):
    customer_id: str
    message: str
    use_memory: bool = True

@app.post("/api/chat")
def chat(request: ChatRequest):
    try:
        response = run_agent(
            customer_id=request.customer_id,
            user_message=request.message,
            use_memory=request.use_memory
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/customers")
async def get_customers():
    data_path = os.path.join(os.path.dirname(__file__), "..", "data", "customers.json")
    try:
        with open(data_path, "r") as f:
            customers = json.load(f)
        return customers
    except Exception as e:
        raise HTTPException(status_code=500, detail="Could not load customers")

# Mount frontend
frontend_dir = os.path.join(os.path.dirname(__file__), "..", "frontend")
if os.path.exists(frontend_dir):
    app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")
