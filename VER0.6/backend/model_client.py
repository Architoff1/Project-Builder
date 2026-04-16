# backend/model_client.py

import requests
import os

# Allow environment-based configuration
API_URL = os.getenv(
    "MODEL_API_URL",
    "https://unsetting-chelsea-unturbidly.ngrok-free.dev/generate"
)

def call_model(prompt, timeout=120):
    try:
        response = requests.post(
            API_URL,
            json={"prompt": prompt},
            timeout=timeout
        )

        response.raise_for_status()
        data = response.json()

        if "response" not in data:
            print("❌ Unexpected API response:", data)
            return ""

        return data["response"]

    except requests.exceptions.Timeout:
        print("❌ Request timed out.")
    except requests.exceptions.RequestException as e:
        print("❌ Request failed:", e)
    except ValueError:
        print("❌ Invalid JSON response:", response.text)

    return ""