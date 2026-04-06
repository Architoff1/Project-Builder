import openai
import json
from .prompts import STEP_GENERATION_PROMPT

def generate_steps(goal: str):
    prompt = STEP_GENERATION_PROMPT.format(goal=goal)

    response = openai.ChatCompletion.create(
        model="gpt-5",
        messages=[
            {"role": "system", "content": "You generate structured workflows."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    raw_output = response["choices"][0]["message"]["content"]

    try:
        steps = json.loads(raw_output)
        return steps
    except:
        return {"error": "Invalid JSON from AI", "raw": raw_output}