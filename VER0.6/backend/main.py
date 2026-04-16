# backend/main.py

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from backend.step_generator import generate_steps

app = FastAPI(
    title="AI Workflow Generator",
    description="API for generating structured workflow steps from user goals.",
    version="1.0.0"
)

# ======================================
# Enable CORS
# ======================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ======================================
# Request Model
# ======================================
class GoalRequest(BaseModel):
    goal: str


# ======================================
# Health Check Endpoint
# ======================================
@app.get("/", tags=["Health"])
def root():
    return {"message": "AI Workflow Generator API is running."}


# ======================================
# Step Generation Endpoint
# ======================================
@app.post("/generate-steps", tags=["Workflow"])
def generate(goal_request: GoalRequest):
    steps = generate_steps(goal_request.goal)

    if isinstance(steps, dict) and "error" in steps:
        return {"steps": [], "error": steps["error"]}

    return {"steps": steps}


# ======================================
# Chat Reset Endpoint
# ======================================
@app.post("/reset-chat", tags=["Workflow"])
def reset_chat():
    """
    Clears conversational context. Currently symbolic since the backend
    is stateless, but useful for future extensions.
    """
    return {"message": "Chat state reset successfully."}