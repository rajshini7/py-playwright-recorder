import pytest
from recorder.report_context import STEP_RESULTS
from pytest_html import extras


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and STEP_RESULTS:
        html = "<h2>Replay Verification Details</h2>"

        for step in STEP_RESULTS:
            html += f"""
            <hr>
            <b>Step:</b> {step['step']}<br>
            <b>URL:</b> {step['url']}<br>
            <b>Status:</b> {step['status']}<br>
            <b>Recorded FirstP:</b><br>
            <pre>{step['recorded']}</pre>
            <b>Live FirstP:</b><br>
            <pre>{step['live']}</pre>
            """

            if step.get("screenshot"):
                html += f"""
                <b>Screenshot:</b><br>
                <img src="{step['screenshot']}" width="600">
                """

        report.extras = getattr(report, "extras", [])
        report.extras.append(extras.html(html))
