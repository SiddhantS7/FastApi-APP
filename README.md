Workflow Engine(FastAPI)

A minimal backend system that runs a node-based workflow engine with shared state, basic branching, looping, and a sample Code Review Mini-Agent workflow.
---

## Overview
This project implements a minimal workflow/graph engine, inspired by LangGraph but intentionally simple.
It supports:

Nodes (Python functions)

Shared state passed between nodes

Basic edges (A → B → C)

Looping (repeat steps until condition met)

Conditional branching

In-memory run storage

FastAPI endpoints to run workflows

A sample workflow Code Review Mini-Agent is included.

---

## Exact folder structure (already provided)
workflow_engine/
    requirements.txt
    README.md
    app/
        _init_.py
        main.py
        engine.py
        models.py
        tools.py
        storage.py
        workflows.py

---

## Step-by-step Windows setup (copy-paste friendly)

1. **Install Python**
   - Go to https://python.org and download the latest Python 3 (3.8+).
   - Run the installer and **check "Add Python to PATH"** before finishing.

2. **Install VS Code (optional but recommended)**
   - Download from https://code.visualstudio.com and install.

3. **Create the project folder**
   - Open **PowerShell** (press Windows key, type `powershell`, Enter).
   - Pick a location, for example your Documents. Run:
     ```
     cd $env:USERPROFILE\Documents
     mkdir workflow_engine
     cd workflow_engine
     mkdir app
     ```
   - You now have `workflow_engine` and `workflow_engine\app`.

4. **Create files**
   - Open VS Code and open the `workflow_engine` folder, or use Notepad.
   - Create the files exactly as named and paste the content from this README (below) into each file.

   Files to create and where:
   - `workflow_engine/requirements.txt`
   - `workflow_engine/README.md` (this file)
   - `workflow_engine/app/_init_.py`
   - `workflow_engine/app/main.py`
   - `workflow_engine/app/engine.py`
   - `workflow_engine/app/models.py`
   - `workflow_engine/app/tools.py`
   - `workflow_engine/app/storage.py`
   - `workflow_engine/app/workflows.py`

   Tip: When saving files in Notepad, pick "All Files" and include the exact file name (no extra `.txt`).

5. **Install dependencies**
   - In PowerShell, inside `workflow_engine` folder run:
     ```
     python -m pip install --upgrade pip
     pip install -r requirements.txt
     ```

6. **Run the server**
   - Still in PowerShell (in the `workflow_engine` folder), run:
     ```
     uvicorn app.main:app --reload
     ```
   - You will see logs and a message: `Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)`

7. **Open the API docs in your browser**
   - Visit: `http://127.0.0.1:8000/docs`
   - This is an interactive Swagger UI where you can call the endpoints easily.

---

## How to use the API (very simple examples)

### 1. Get default graph id
- In browser: open `http://127.0.0.1:8000/graph/default`
- Or using PowerShell:

### 2) Run the workflow with some sample code
- The POST `/graph/run` accepts JSON:
{
"graph_id": "default",
"code": "def add(a, b):\n return a + b\n\n# TODO: implement multiply\n\ndef multiply(a, b, c, d, e):\n # pretend long function\n x = a + b\n x += c\n x += d\n x += e\n return x\n"
}
