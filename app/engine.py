"""
A very small, beginner-friendly workflow engine.
- Runs nodes one by one.
- Shares a dict "shared" between nodes.
- Stops early when stop condition is met: shared['quality_score'] >= threshold
- Node functions are simple and named:
    node_extract, node_complexity, node_detect, node_suggest
"""

from typing import Dict, Any, List
from . import tools
from . import storage
from .workflows import get_graph
import time

# Node function signatures: async functions that accept the shared dict and return output dict
# Keep everything straightforward and readable.


async def node_extract(shared: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract functions from code and put them into shared['functions'].
    """
    code = shared.get("code", "")
    funcs = tools.extract_functions(code)
    out = {"functions": funcs}
    # store in shared so later nodes can use
    shared["functions"] = funcs
    return out


async def node_complexity(shared: Dict[str, Any]) -> Dict[str, Any]:
    """
    Check complexity for each extracted function and write results to shared['complexities'].
    """
    funcs = shared.get("functions", [])
    complexities = []
    for fn in funcs:
        c = tools.check_complexity(fn.get("body", ""))
        complexities.append({"name": fn.get("name"), "complexity": c})
    shared["complexities"] = complexities
    return {"complexities": complexities}


async def node_detect(shared: Dict[str, Any]) -> Dict[str, Any]:
    """
    Detect code smells for each function and write to shared['smells'].
    """
    funcs = shared.get("functions", [])
    all_smells = []
    for fn in funcs:
        smells = tools.detect_smells(fn)
        if smells:
            all_smells.append({"function": fn.get("name"), "smells": smells})
    shared["smells"] = all_smells
    return {"smells": all_smells}


async def node_suggest(shared: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create suggestions based on detected smells and calculate a quality score.
    Stores suggestions and quality_score in shared.
    """
    smells_list = []
    # gather all smell strings
    if "smells" in shared:
        for entry in shared["smells"]:
            smells_list.extend(entry.get("smells", []))

    suggestions, quality_score = tools.suggest_improvements(smells_list)
    shared["suggestions"] = suggestions
    shared["quality_score"] = quality_score

    # Optionally mark "stop" condition in shared; engine will check threshold
    return {"suggestions": suggestions, "quality_score": quality_score}


NODE_FN_MAP = {
    "node_extract": node_extract,
    "node_complexity": node_complexity,
    "node_detect": node_detect,
    "node_suggest": node_suggest,
}


async def run_graph(graph_id: str, code: str) -> Dict[str, Any]:
    """
    Run the graph step-by-step.
    Returns the run_id and final state summary.
    """
    graph = get_graph(graph_id)
    threshold = graph.get("threshold", 80)

    # initialize shared state
    shared: Dict[str, Any] = {"code": code, "threshold": threshold, "quality_score": 0}

    run_id = storage.create_run(graph_id, initial_shared=shared)

    nodes = graph.get("nodes", [])
    for node_def in nodes:
        node_id = node_def.get("id")
        fn_name = node_def.get("fn")
        node_fn = NODE_FN_MAP.get(fn_name)
        node_output = {"node_id": node_id, "status": "skipped", "output": None}

        if not node_fn:
            node_output["status"] = "error"
            node_output["output"] = {"error": f"Node function '{fn_name}' not found."}
            storage.append_node_result(run_id, node_output)
            continue

        # Run the node function and catch exceptions; keep everything simple
        try:
            node_output["status"] = "running"
            storage.append_node_result(run_id, node_output)

            result = await node_fn(shared)

            node_output = {"node_id": node_id, "status": "completed", "output": result}
            storage.append_node_result(run_id, node_output)

            # update the stored shared state
            storage.update_run(run_id, shared=shared)

            # check stop condition after node finishes
            current_quality = shared.get("quality_score", 0)
            if current_quality >= threshold:
                storage.update_run(run_id, stopped=True, status="completed")
                # write a final node indicating stop
                storage.append_node_result(run_id, {
                    "node_id": "stop",
                    "status": "stopped_by_threshold",
                    "output": {"quality_score": current_quality, "threshold": threshold}
                })
                return {"run_id": run_id, "status": "completed", "shared": shared}

            # tiny sleep to simulate step progression (not required, but readable)
            time.sleep(0.01)

        except Exception as e:
            node_output = {"node_id": node_id, "status": "failed", "output": {"error": str(e)}}
            storage.append_node_result(run_id, node_output)
            storage.update_run(run_id, status="failed")
            return {"run_id": run_id, "status": "failed", "error": str(e), "shared": shared}

    # finished all nodes
    storage.update_run(run_id, status="completed", shared=shared)
    return {"run_id": run_id, "status": "completed", "shared": shared}
