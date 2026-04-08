import requests

API_URL = "https://unsetting-chelsea-unturbidly.ngrok-free.dev/generate"

def call_model(prompt):
    try:
        response = requests.post(
            API_URL,
            json={"prompt": prompt},
            timeout=120
        )

        # Checks status
        if response.status_code != 200:
            print("❌ API Error:", response.status_code)
            return ""

        # Safe JSON parse
        try:
            return response.json().get("response", "")
        except:
            print("❌ Invalid JSON from API")
            print(response.text)
            return ""

    except requests.exceptions.RequestException as e:
        print("❌ Request failed:", e)
        return ""