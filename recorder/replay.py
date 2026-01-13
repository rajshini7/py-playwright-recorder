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
            recorded = step["content"]

            page.goto(target_url)
            live = extract_content(page)

            # ---------- LENIENT NORMALIZATION ----------
            def normalize(content):
                texts = {
                    item["text"]
                    for item in content.get("visible_items", [])
                    if item.get("text")
                }

                return {
                    "title": content.get("title"),
                    "h1": content.get("h1"),
                    "firstP": content.get("firstP"),
                    "texts": texts
                }

            r = normalize(recorded)
            l = normalize(live)

            # ---------- CORE CHECKS ----------
            title_match = r["title"] == l["title"]
            h1_match = r["h1"] == l["h1"]
            firstp_match = r["firstP"] == l["firstP"]

            # ---------- TEXT COVERAGE CHECK ----------
            if r["texts"]:
                matched = len(r["texts"] & l["texts"])
                coverage = matched / len(r["texts"])
            else:
                coverage = 1.0

            passed = (
                title_match and
                h1_match and
                firstp_match and
                coverage >= 0.8   # 👈 leniency threshold
            )

            if passed:
                add_step_result(
                    step=index,
                    url=target_url,
                    recorded="Content matched (lenient)",
                    live=f"Coverage: {coverage:.0%}",
                    status="PASSED"
                )
            else:
                screenshot_path = f"reports/screenshots/step_{index}.png"
                page.screenshot(path=screenshot_path)

                add_step_result(
                    step=index,
                    url=target_url,
                    recorded="Recorded content",
                    live=f"Coverage: {coverage:.0%}",
                    status="FAILED",
                    screenshot=screenshot_path
                )

                raise AssertionError(
                    f"\n❌ Replay verification failed at step {index}\n"
                    f"URL: {target_url}\n"
                    f"Text coverage: {coverage:.0%}\n"
                    f"title_match={title_match}, h1_match={h1_match}, firstP_match={firstp_match}\n"
                )

        browser.close()
