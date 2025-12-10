"""
Very simple in-memory storage for run states.
Designed for demo/learning. Not persistent.
"""

import uuid
from typing import Dict, Any

# single module-level dict to hold runs
_RUNS: Dict[str, Dict[str, Any]] = {}


def create_run(graph_id: str, initial_shared: Dict[str, Any] = None) -> str:
    run_id = uuid.uuid4().hex
    state = {
        "run_id": run_id,
        "graph_id": graph_id,
        "status": "running",
        "nodes": [],
        "shared": initial_shared or {},
        "stopped": False,
    }
    _RUNS[run_id] = state
    return run_id


def get_run(run_id: str) -> Dict[str, Any]:
    return _RUNS.get(run_id)


def update_run(run_id: str, **kwargs) -> None:
    run = _RUNS.get(run_id)
    if not run:
        return
    for k, v in kwargs.items():
        run[k] = v


def append_node_result(run_id: str, node_result: Dict[str, Any]) -> None:
    run = _RUNS.get(run_id)
    if not run:
        return
    run["nodes"].append(node_result)
