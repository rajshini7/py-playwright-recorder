# recorder/report_context.py

_STEP_RESULTS = []


def add_step_result(
    step,
    url,
    recorded,
    live,
    status,
    screenshot=None
):
    _STEP_RESULTS.append({
        "step": step,
        "url": url,
        "recorded": recorded,
        "live": live,
        "status": status,
        "screenshot": screenshot
    })


def get_results():
    return _STEP_RESULTS
