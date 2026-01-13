# create_tester/report_context.py

from typing import List, Dict, Any

STEP_RESULTS: List[Dict[str, Any]] = []


def add_step_result(
    step: int,
    url: str,
    create_tested: Any,   # ⬅ can now be full content dict
    live: Any,       # ⬅ can now be full content dict
    status: str,
    screenshot: str | None = None
):
    STEP_RESULTS.append({
        "step": step,
        "url": url,
        "create_tested": create_tested,
        "live": live,
        "status": status,
        "screenshot": screenshot
    })
