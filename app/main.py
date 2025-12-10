"""
FastAPI app exposing the workflow engine endpoints.
Keep endpoints simple and easy to read.
"""

from fastapi import FastAPI, HTTPException
from typing import Dict, Any
from .models import RunRequest, RunState, NodeResult
from .workflows import DEFAULT_GRAPH_ID, get_graph, get_default_graph
from . import engine
from . import storage

app = FastAPI(title="Mini Workflow Engine (FastAPI)")

@app.get("/graph/default")
async def get_default():
    """
    Return the default graph id and a tiny hint about nodes.
    """
    graph = get_default_graph()
    return {"default_graph_id": graph["id"], "nodes": [n["id"] for n in graph["nodes"]]}


@app.post("/graph/run")
async def run_graph(req: RunRequest):
    """
    Start a workflow run. Request body: { "graph_id": "...", "code": "..." }
    Returns run_id and a small summary.
    """
    graph_id = req.graph_id or DEFAULT_GRAPH_ID
    graph = get_graph(graph_id)
    if not graph:
        raise HTTPException(status_code=400, detail="Graph not found")

    result = await engine.run_graph(graph_id, req.code)
    return result


@app.get("/graph/state/{run_id}")
async def get_state(run_id: str):
    """
    Return stored run state for a given run_id.
    """
    run = storage.get_run(run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
    return run
