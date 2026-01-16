import pytest
import base64
import os
from engine.report_context import STEP_RESULTS
from pytest_html import extras


def _img_to_base64(path: str) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and STEP_RESULTS:
        extra = getattr(report, "extras", [])

        html = "<h2>run_test Verification Details</h2>"

        for step in STEP_RESULTS:
            html += f"""
            <hr>
            <b>Step:</b> {step['step']}<br>
            <b>URL:</b> {step['url']}<br>
            <b>Status:</b> {step['status']}<br>
            <b>create_tested FirstP:</b>
            <pre>{step['create_tested']}</pre>
            <b>Live FirstP:</b>
            <pre>{step['live']}</pre>
            """

            if step.get("screenshot"):
                encoded = _img_to_base64(step["screenshot"])
                html += f"""
                <b>Screenshot:</b><br>
                <img src="data:image/png;base64,{encoded}" width="700"><br>
                """

        extra.append(extras.html(html))
        report.extras = extra

        # 🔥 THIS LINE REMOVES THE GREY STACK TRACE
        report.longrepr = None
