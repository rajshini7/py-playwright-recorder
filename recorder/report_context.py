# recorder/report_context.py

from typing import List, Dict

STEP_RESULTS: List[Dict] = []

def add_step_result(
    step: int,
    url: str,
    recorded: str,
    live: str,
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
