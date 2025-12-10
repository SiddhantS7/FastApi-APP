"""
Definition of simple workflow graphs.

We provide one default graph:
- id: "default"
- nodes: run in sequence:
    1) extract
    2) complexity
    3) detect
    4) suggest
- The engine will run node-by-node, passing a shared state dict between nodes.
- The workflow stops early when shared['quality_score'] >= shared['threshold'].
"""

from typing import Dict, Any, List

DEFAULT_GRAPH_ID = "default"


def get_default_graph() -> Dict[str, Any]:
    """
    Returns a simple graph definition.
    Graph format (very small DSL):
    {
        "id": "default",
        "nodes": [
            {"id": "extract", "fn": "node_extract"},
            {"id": "complexity", "fn": "node_complexity"},
            {"id": "detect", "fn": "node_detect"},
            {"id": "suggest", "fn": "node_suggest"},
        ],
        "threshold": 80  # quality_score threshold to stop early
    }
    """
    return {
        "id": DEFAULT_GRAPH_ID,
        "nodes": [
            {"id": "extract", "fn": "node_extract"},
            {"id": "complexity", "fn": "node_complexity"},
            {"id": "detect", "fn": "node_detect"},
            {"id": "suggest", "fn": "node_suggest"},
        ],
        "threshold": 80,
    }


def get_graph(graph_id: str) -> Dict[str, Any]:
    # for now we only support the default graph
    if graph_id == DEFAULT_GRAPH_ID:
        return get_default_graph()
    # fallback: return default
    return get_default_graph()
