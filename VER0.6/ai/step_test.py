import ollama
import json
import re


def clean_json_output(text):
    """
    Extract JSON array from model output
    """
    match = re.search(r'\[.*\]', text, re.DOTALL)
    if match:
        return match.group(0)
    return text


def generate_steps(goal, max_retries=2):
    prompt = f"""
You are a strict JSON generator.

You MUST follow the exact format.

Here is an example:

Goal: Build a chatbot

Output:
[
  {{
    "id": 1,
    "title": "Collect Data",
    "description": "Gather conversation datasets",
    "type": "data",
    "tools": ["python", "datasets"],
    "inputs": [],
    "outputs": ["raw_data"]
  }},
  {{
    "id": 2,
    "title": "Preprocess Data",
    "description": "Clean and prepare text data",
    "type": "processing",
    "tools": ["pandas"],
    "inputs": ["raw_data"],
    "outputs": ["clean_data"]
  }}
]

Now follow this EXACT format.

Goal: {goal}

Return ONLY JSON.
"""

    for attempt in range(max_retries + 1):

        response = ollama.chat(
            model='mistral',
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        output = response['message']['content']

        # 🔥 Clean output
        cleaned = clean_json_output(output)

        try:
            steps = json.loads(cleaned)
            return steps

        except:
            print(f"\n⚠️ Attempt {attempt + 1} failed")

            if attempt == max_retries:
                print("\n❌ FINAL FAILURE")
                print("\nRAW OUTPUT:\n", output)
                return None

            print("🔁 Retrying...\n")


if __name__ == "__main__":
    goal = "Build a stock prediction model"

    steps = generate_steps(goal)

    print("\n✅ FINAL PARSED STEPS:\n")

    if steps:
        for step in steps:
            print(f"{step['id']}. {step['title']} → {step['description']}")
    else:
        print("Failed to generate steps.")