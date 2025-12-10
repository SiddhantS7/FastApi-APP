"""
Simple, beginner-friendly models used by the engine and API.
No external complexity, plain Python data structures and pydantic models for request validation.
"""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel


class RunRequest(BaseModel):
    graph_id: str
    code: str


class NodeResult(BaseModel):
    node_id: str
    status: str
    output: Optional[Dict[str, Any]] = None


class RunState(BaseModel):
    run_id: str
    graph_id: str
    status: str
    nodes: List[NodeResult]
    shared: Dict[str, Any]
    stopped: bool = False
