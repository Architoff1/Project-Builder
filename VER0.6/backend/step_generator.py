import json
import re
from .model_client import call_model


def clean_json_output(text):
    match = re.search(r'\[.*\]', text, re.DOTALL)
    if match:
        return match.group(0)
    return text


def generate_steps(goal, max_retries=2):
    prompt = f"""
Convert goal into 5 steps.

Goal: {goal}

Return JSON:
[
  {{
    "id": 1,
    "title": "...",
    "description": "..."
  }}
]
"""

    for attempt in range(max_retries + 1):

        output = call_model(prompt)
        print("\n🔍 RAW MODEL OUTPUT:\n", output)
        cleaned = clean_json_output(output)

        try:
            steps = json.loads(cleaned)
            return steps
        except:
            print(f"⚠️ Retry {attempt+1}")

    return {"error": "Failed to parse"}