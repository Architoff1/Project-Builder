# test/step_test.py

import sys
import os
import json
import time

# ===============================
# Ensure Project Root is in Path
# ===============================
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)

if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Import after path adjustment
try:
    from backend.step_generator import generate_steps
except ImportError as e:
    print("❌ Import Error:", e)
    sys.exit(1)


def main():
    goal = "Build a stock prediction model"
    print(f"\n🎯 Goal: {goal}")

    start_time = time.time()

    try:
        steps = generate_steps(goal)
    except Exception as e:
        print("\n❌ Exception during step generation:", str(e))
        sys.exit(1)

    end_time = time.time()
    elapsed_time = end_time - start_time

    # ===============================
    # Output Handling
    # ===============================
    if isinstance(steps, list):
        print(f"\n✅ Parsed {len(steps)} Steps Successfully (⏱ {elapsed_time:.2f}s):\n")

        for step in steps:
            print(f"🔹 Step {step.get('id')}: {step.get('title')}")
            print(f"   Description : {step.get('description')}")
            print(f"   Type        : {step.get('type')}")
            print(f"   Tools       : {', '.join(step.get('tools', []))}")
            print(f"   Inputs      : {', '.join(step.get('inputs', []))}")
            print(f"   Outputs     : {', '.join(step.get('outputs', []))}")
            print("-" * 60)

        # Pretty JSON Output for Debugging
        print("\n📦 Full JSON Output:\n")
        print(json.dumps(steps, indent=2))

    else:
        print("\n❌ Error: Failed to generate valid steps.")
        print("Response:", steps)


if __name__ == "__main__":
    main()