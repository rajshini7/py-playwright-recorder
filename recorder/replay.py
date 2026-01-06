from playwright.sync_api import sync_playwright
from recorder.login import login
from recorder.content import extract_content
from recorder.steps_store import load_steps
from recorder.report_context import add_step_result
import os



def replay(base_url, username, password):
    steps = load_steps()

    if not steps:
        raise RuntimeError("No recorded steps found")

    os.makedirs("reports/screenshots", exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        login(page, base_url, username, password)

        for index, step in enumerate(steps, start=1):
            target_url = step["target_url"]
            recorded_first_p = step["content"]["firstP"]

            page.goto(target_url)
            live = extract_content(page)
            live_first_p = live["firstP"]

            if live_first_p == recorded_first_p:
                add_step_result(
                    step=index,
                    url=target_url,
                    recorded=recorded_first_p,
                    live=live_first_p,
                    status="PASSED"
                )
            else:
                screenshot_path = f"reports/screenshots/step_{index}.png"
                page.screenshot(path=screenshot_path)

                add_step_result(
                    step=index,
                    url=target_url,
                    recorded=recorded_first_p,
                    live=live_first_p,
                    status="FAILED",
                    screenshot=screenshot_path
                )

                raise AssertionError(
                    f"\n❌ Replay verification failed at step {index}\n"
                    f"URL: {target_url}\n\n"
                    f"Recorded:\n{recorded_first_p}\n\n"
                    f"Live:\n{live_first_p}\n"
                )

        browser.close()
