from openai import OpenAI
import json

client = OpenAI()

def generate_steps(goal):
    prompt = f"""
    Convert this goal into steps.

    Goal: {goal}

    Return ONLY valid JSON array with:
    - id
    - title
    - description
    """

    response = client.chat.completions.create(
        model="gpt-5",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    output = response.choices[0].message.content

    try:
        steps = json.loads(output)
        return steps
    except:
        print("❌ RAW OUTPUT:\n", output)
        return None


if __name__ == "__main__":
    goal = "Build a stock prediction model"
    steps = generate_steps(goal)

    print("\n✅ Generated Steps:\n")
    print(steps)