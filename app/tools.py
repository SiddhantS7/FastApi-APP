"""
Tool functions used by the Node functions.
These are intentionally simple implementations for learning / demo purposes.
"""

import re
from typing import Dict, List, Tuple


def extract_functions(code: str) -> List[Dict[str, str]]:
    """
    Very simple function extractor using regex.
    Returns a list of dicts: { 'name': <fn_name>, 'body': <fn_body> }
    This is not a full parser — it's intentionally simple.
    """
    pattern = r"def\s+([A-Za-z_]\w*)\s*\((.*?)\)\s*:\s*((?:\n(?:\s+).+)*)"
    matches = re.finditer(pattern, code, re.MULTILINE)
    results = []
    for m in matches:
        name = m.group(1)
        params = m.group(2)
        body = m.group(3)
        # trim leading indentation from body
        body_lines = [line[4:] if line.startswith("    ") else line for line in body.splitlines()]
        body_text = "\n".join(body_lines).strip()
        results.append({"name": name, "params": params.strip(), "body": body_text})
    return results


def check_complexity(fn_body: str) -> int:
    """
    A very rudimentary complexity metric: number of lines in the function body.
    The larger the number, the higher (worse) the complexity number returned.
    """
    if not fn_body:
        return 0
    lines = [l for l in fn_body.splitlines() if l.strip() != ""]
    return len(lines)


def detect_smells(fn: Dict[str, str]) -> List[str]:
    """
    Detect simple 'smells' like:
    - long functions
    - too many parameters
    - presence of TODO comments
    """
    smells = []
    name = fn.get("name", "")
    params = fn.get("params", "")
    body = fn.get("body", "")

    # too many parameters
    param_count = 0
    if params.strip():
        param_count = len([p for p in params.split(",") if p.strip() != ""])
    if param_count > 4:
        smells.append(f"{name}: too_many_parameters ({param_count})")

    # long function
    complexity = check_complexity(body)
    if complexity > 20:
        smells.append(f"{name}: long_function ({complexity} lines)")

    # TODO comments
    if "TODO" in body or "todo" in body:
        smells.append(f"{name}: contains_TODO")

    return smells


def suggest_improvements(smells: List[str]) -> Tuple[List[str], int]:
    """
    Convert detected smells into human-friendly suggestions and compute a quality score (0-100).
    The more smells, the lower the quality score.
    """
    suggestions = []
    penalty = 0
    for s in smells:
        if "too_many_parameters" in s:
            suggestions.append("Consider grouping parameters into a dataclass or reduce parameter count.")
            penalty += 20
        elif "long_function" in s:
            suggestions.append("Split long functions into smaller helper functions.")
            penalty += 25
        elif "contains_TODO" in s:
            suggestions.append("Resolve TODO comments or add tests/implementation.")
            penalty += 10
        else:
            suggestions.append(f"Investigate: {s}")
            penalty += 5

    # base quality is 100, subtract penalty
    quality_score = max(0, 100 - penalty)
    return suggestions, quality_score
