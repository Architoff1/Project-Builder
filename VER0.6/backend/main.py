from fastapi import FastAPI
from pydantic import BaseModel
from step_generator import generate_steps

app = FastAPI()

class GoalRequest(BaseModel):
    goal: str

@app.post("/generate-steps")
def generate(goal_request: GoalRequest):
    steps = generate_steps(goal_request.goal)
    return {"steps": steps}