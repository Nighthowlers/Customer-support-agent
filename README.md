# Customer Support Routing Agent

An automated, graph-based Customer Support Agent built with the Google Agent Development Kit (ADK). This project demonstrates multi-agent routing using directed workflows.

## Features
*   **Query Classification**: Automatically detects whether a query is related to shipping or unrelated topics.
*   **Specialized Sub-agents**:
    *   `classifier_agent`: Handles input labeling and routing.
    *   `faq_agent`: Provides playful, emoji-rich shipping details with free shipping alerts.
    *   `decline_agent`: Politely redirects non-shipping questions.
*   **Interactive Playground**: Built-in FastAPI/Uvicorn Web UI to test and trace agent decisions.

---

## Getting Started

### 1. Prerequisites
Make sure you have Python 3.11+ installed on your system.

### 2. Installation
Clone the repository and install the dependencies:
```bash
# Create a virtual environment
python -m venv .venv

# Activate the virtual environment
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Install Google ADK
pip install google-adk google-genai python-dotenv
```

### 3. Configuration
1. Copy the `.env.example` file to create a `.env` file:
   ```bash
   cp .env.example .env
   ```
2. Open `.env` and enter your Gemini API Key from [Google AI Studio](https://aistudio.google.com/):
   ```env
   GOOGLE_API_KEY=AIzaSy...
   ```

---

## Running the Agent

### Run via Command Line
To run a quick single query from your terminal:
```bash
# Windows (PowerShell):
$env:PYTHONIOENCODING="utf-8"; adk run . "how long does standard delivery take?"

# macOS/Linux:
PYTHONIOENCODING=utf-8 adk run . "how long does standard delivery take?"
```

### Run the Interactive Web Playground
To launch the browser UI:
```bash
adk web --port 8000 .
```
Open your browser and navigate to: **http://127.0.0.1:8000**
