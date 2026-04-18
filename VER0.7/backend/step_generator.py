# backend/step_generator.py

import json
import re
from typing import List, Dict, Any, Optional, Union
from .model_client import call_model


# ==========================================
# Utility: Infer Outputs (VERY LIGHT HINTS)
# ==========================================
def infer_outputs_from_title(title: str) -> List[str]:
    title_lower = title.lower()

    # Only soft hints (no restriction)
    if "frontend" in title_lower or "ui" in title_lower:
        return ["index.html"]
    if "style" in title_lower:
        return ["style.css"]
    if "script" in title_lower or "logic" in title_lower:
        return ["script.js"]

    return []


# ==========================================
# Utility: Clean File Outputs
# ==========================================
def clean_outputs(outputs: List[str]) -> List[str]:
    cleaned = []

    for f in outputs:
        if not isinstance(f, str):
            continue

        f = f.strip()

        # Remove garbage
        if not f or len(f) < 3:
            continue
        if f.startswith("http"):
            continue
        if " " in f and "." not in f:
            continue

        cleaned.append(f)

    return list(set(cleaned))


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

        # 🔥 RELAXED TYPE HANDLING (NO RESTRICTION)
        step_type = step.get("type", "").lower()

        if step_type == "testing":
            step_type = "evaluation"

        if not step_type:
            step_type = "processing"

        step["type"] = step_type

        # Required fields
        step["title"] = step.get("title", f"Step {i}")
        step["description"] = step.get(
            "description", f"Execute {step['title']}."
        )

        step["tools"] = step.get("tools", [])
        step["inputs"] = step.get("inputs", [])
        step["outputs"] = step.get("outputs", [])

        # Light inference only
        if not step["outputs"]:
            step["outputs"] = infer_outputs_from_title(step["title"])

        # 🔥 Clean outputs
        step["outputs"] = clean_outputs(step["outputs"])

    return True


# ==========================================
# Main Function: Generate Steps
# ==========================================
def generate_steps(
    goal: str,
    max_retries: int = 2
) -> Union[List[Dict[str, Any]], Dict[str, str]]:

    prompt_template = """
You are an expert software system planner.

Return ONLY a JSON array (NOT an object).
DO NOT wrap in {{"steps": ...}}
DO NOT add explanations or markdown.

────────────────────────
TASK
────────────────────────
Break the user goal into a sequence of logical development steps.

Each step must represent a REAL development action in building a COMPLETE system.

────────────────────────
STEP FORMAT
────────────────────────
[
  {{
    "id": 1,
    "title": "short title",
    "description": "clear explanation (REQUIRED, not empty)",
    "type": "any meaningful category",
    "tools": ["tool1"],
    "inputs": ["input1"],
    "outputs": ["file names with extensions"]
  }}
]

────────────────────────
SYSTEM THINKING RULES
────────────────────────
- Think like a software architect
- Steps must form a logical pipeline
- Each step should depend on outputs of previous steps
- Build a COMPLETE system, not isolated parts

────────────────────────
GENERALITY
────────────────────────
- The system can be ANY type (web, backend, ML, CLI, etc.)
- Choose appropriate technologies based on the goal
- DO NOT assume a fixed tech stack

────────────────────────
QUALITY CONTROL
────────────────────────
- Avoid redundant steps
- Avoid meaningless steps
- Each step must produce meaningful outputs
- Outputs must be usable in later steps

────────────────────────
OUTPUT RULES
────────────────────────
- Output MUST be a JSON ARRAY only
- id MUST be integer
- description MUST NOT be empty
- outputs MUST contain realistic file names
- DO NOT include URLs or explanations

────────────────────────
GOAL
────────────────────────
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