import sys
import os

# Get project root
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

# Add to path safely
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from backend.step_generator import generate_steps


if __name__ == "__main__":
    goal = "Build a stock prediction model"
    steps = generate_steps(goal)

    print("\nSTEPS:\n", steps)