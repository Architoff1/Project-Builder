# backend/step_generator.py

import json
import re
from typing import List, Dict, Any, Optional, Union
from .model_client import call_model

# Allowed step types
ALLOWED_TYPES = {
    "data", "processing", "model",
    "training", "evaluation", "deployment"
}

# ==========================================
# Utility: Infer Outputs if Missing
# ==========================================
def infer_outputs_from_title(title: str) -> List[str]:
    title_lower = title.lower()

    if "html" in title_lower:
        return ["index.html"]
    if "css" in title_lower:
        return ["style.css"]
    if "javascript" in title_lower or "js" in title_lower:
        return ["script.js"]
    if "api" in title_lower:
        return ["app.py"]
    if "java" in title_lower:
        return ["Main.java"]
    if "node" in title_lower:
        return ["app.js", "package.json"]

    return ["main.py"]


# ==========================================
# Utility: Clean and Extract JSON
# ==========================================
def clean_json_output(text: str) -> Optional[List[Dict[str, Any]]]:
    if not text:
        return None

    text = re.sub(r"```json\s*|```", "", text, flags=re.IGNORECASE).strip()

    try:
        parsed = json.loads(text)
        if isinstance(parsed, list):
            return parsed
        if isinstance(parsed, dict) and "steps" in parsed:
            return parsed["steps"]
    except json.JSONDecodeError:
        pass

    match = re.search(r"\[\s*{.*?}\s*\]", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            pass

    return None


# ==========================================
# Utility: Validate and Normalize Steps
# ==========================================
def validate_steps(steps: List[Dict[str, Any]]) -> bool:
    if not isinstance(steps, list) or len(steps) == 0:
        return False

    for i, step in enumerate(steps, start=1):
        if not isinstance(step, dict):
            return False

        # Normalize ID
        if isinstance(step.get("id"), str) and step["id"].isdigit():
            step["id"] = int(step["id"])
        if not isinstance(step.get("id"), int):
            return False

        # Normalize type
        step_type = step.get("type", "").lower()
        if step_type == "testing":
            step_type = "evaluation"
        if step_type not in ALLOWED_TYPES:
            step_type = "processing"
        step["type"] = step_type

        # Ensure required fields
        step["title"] = step.get("title", f"Step {i}")
        step["description"] = step.get(
            "description", f"Execute {step['title']}."
        )

        step["tools"] = step.get("tools", [])
        step["inputs"] = step.get("inputs", [])
        step["outputs"] = step.get("outputs", [])

        # Infer outputs if missing
        if not step["outputs"]:
            step["outputs"] = infer_outputs_from_title(step["title"])

    return True


# ==========================================
# Main Function: Generate Steps
# ==========================================
def generate_steps(
    goal: str,
    max_retries: int = 2
) -> Union[List[Dict[str, Any]], Dict[str, str]]:

    prompt_template = """
You are a strict JSON generator.

Return ONLY a JSON array (NOT an object).
DO NOT wrap in {{"steps": ...}}
DO NOT add explanations or markdown.

Each step MUST follow:

[
  {{
    "id": 1,
    "title": "short title",
    "description": "clear explanation (REQUIRED, not empty)",
    "type": "data | processing | model | training | evaluation | deployment",
    "tools": ["tool1"],
    "inputs": ["input1"],
    "outputs": ["actual file names with extensions"]
  }}
]

Rules:
- Output MUST be a JSON ARRAY only
- id MUST be integer (not string)
- description MUST NOT be empty
- Each step must depend on previous outputs
- "outputs" MUST contain realistic file names with proper extensions.

Examples:
- Web app → ["index.html", "style.css", "script.js"]
- Python app → ["main.py", "requirements.txt"]
- Java app → ["Main.java", "pom.xml"]
- Node.js app → ["app.js", "package.json"]

Goal:
{goal}
"""

    prompt = prompt_template.format(goal=goal.strip())

    for attempt in range(max_retries + 1):
        print(f"\n🔄 Attempt {attempt + 1}")

        try:
            raw_output = call_model(prompt)
            print("\n🔍 RAW MODEL OUTPUT:\n", raw_output)

            steps = clean_json_output(raw_output)

            if steps and validate_steps(steps):
                print("✅ Steps validated successfully.")
                return steps

            print("⚠️ Validation failed. Retrying...")

        except Exception as e:
            print(f"❌ Error during model call: {str(e)}")

    return {"error": "Failed to parse valid steps after retries."}