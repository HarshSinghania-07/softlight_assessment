# softlight_assessment

Take home assessment for Softlight AI Engineer

## Steps to run this project :

### 1. Create and activate a Python virtual environment:

```
python3 -m venv venv
source venv/bin/activate   # Activates the venv created above
```

### 2. Install dependencies :

```
pip install -r requirements.txt
playwright install
```

### 3. Run command to execute project :

```
python main.py
```

Using a local Llama 2 GGUF model via llama-cpp-python, the agent dynamically generates a step-by-step workflow plan and controls the browser using Playwright to perform the described actions, capturing UI states and screenshots at each step.

The system demonstrates generalization across tasks and applications, aligning with the assessment goal of real-time, agentic behavior
