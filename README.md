# AI Workflow Generator

This project is an AI-powered guided builder that translates user goals into structured development steps and generates the corresponding code. It consists of a Python/FastAPI backend and a vanilla HTML/JS frontend.

## 📁 Project Structure
The project assumes the following basic structure based on the imports:
* `backend/` - Contains the FastAPI application and generation logic (`main.py`, `step_generator.py`, etc.)
* `test/` - Contains test scripts (`step_test.py`)
* `index.html` - The frontend user interface
* `requirements.txt` - Python dependencies

---

## ⚙️ Setup & Installation

### 1. Prerequisites
* **Python 3.8+** installed on your system.
* A modern web browser.

### 2. Create a Virtual Environment (Recommended)
It's best practice to isolate your project dependencies. Open your terminal in the root directory of the project and run:

**For Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```
**For Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

With your virtual environment activated, install the required packages using the requirements.txt file:
```bash
pip install -r requirements.txt
```

### 4. Running the Project
To use the Guided Builder, you need to have both the backend running in your terminal and the frontend open in your browser.

**Step 1: Start the Backend API**
From the root directory of your project, start the FastAPI server using Uvicorn. (Note: Since your main.py is inside the backend folder, you reference it as backend.main:app):

```bash
uvicorn backend.main:app --reload
```

1. You should see output indicating the server is running on http://127.0.0.1:8000.
2. The --reload flag ensures the server automatically restarts if you make changes to your Python files.

**Step 2: Open the Frontend**
The frontend is a standalone HTML file that communicates with your local backend.
1. Locate the index.html file in your file explorer.
2. Double-click it to open it directly in your web browser (or right-click and select "Open with" -> Chrome/Edge/Firefox).
3. Type a prompt into the chat window and click Send to start generating workflows!


### 5. Testing
If you want to test the step generation logic purely via the command line without the API or frontend, you can run the provided test script:

```Bash
python test/step_test.py
```

This will run a hardcoded goal ("Build a stock prediction model") and output the parsed steps directly to your terminal.

**🔧 Environment Variables (Optional)**
The backend relies on an external model API endpoint (Mistral via ngrok). By default, it uses a hardcoded URL. If that ngrok tunnel expires or changes, you can override it without changing the code by setting an environment variable before starting the backend:

**Mac/Linux:**
```Bash
export MODEL_API_URL="[https://your-new-ngrok-url.dev/generate](https://your-new-ngrok-url.dev/generate)"
```

**Windows (PowerShell):**
```PowerShell
$env:MODEL_API_URL="[https://your-new-ngrok-url.dev/generate](https://your-new-ngrok-url.dev/generate)"
```
