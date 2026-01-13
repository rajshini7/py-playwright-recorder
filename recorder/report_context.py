# recorder/report_context.py

from typing import List, Dict, Any

STEP_RESULTS: List[Dict[str, Any]] = []


def add_step_result(
    step: int,
    url: str,
    recorded: Any,   # ⬅ can now be full content dict
    live: Any,       # ⬅ can now be full content dict
    status: str,
    screenshot: str | None = None
):
    STEP_RESULTS.append({
        "step": step,
        "url": url,
        "recorded": recorded,
        "live": live,
        "status": status,
        "screenshot": screenshot
    })
