from playwright.sync_api import sync_playwright
from engine.login import login
from engine.content import extract_content
from engine.steps_store import load_steps
from engine.report_context import add_step_result
import os


def run_test(base_url, username, password):
    steps = load_steps()

    if not steps:
        raise RuntimeError("No create_tested steps found")

    os.makedirs("reports/screenshots", exist_ok=True)

    has_failures = False

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        login(page, base_url, username, password)

        for index, step in enumerate(steps, start=1):
            target_url = step["target_url"]
            create_tested = step["content"]

            page.goto(target_url)
            live = extract_content(page)

            # ---------- STRICT NORMALIZATION ----------
            def normalize(content):
                return {
                    "title": content.get("title"),
                    "h1": content.get("h1"),
                    "firstP": content.get("firstP"),
                    "items": sorted(
                        [
                            (i.get("tag"), i.get("text"))
                            for i in content.get("visible_items", [])
                            if i.get("text")
                        ]
                    )
                }

            r = normalize(create_tested)
            l = normalize(live)

            if r == l:
                add_step_result(
                    step=index,
                    url=target_url,
                    create_tested=create_tested.get("firstP"),
                    live=live.get("firstP"),
                    status="PASSED"
                )
            else:
                has_failures = True

                screenshot_path = f"reports/screenshots/step_{index}.png"
                page.screenshot(path=screenshot_path)

                add_step_result(
                    step=index,
                    url=target_url,
                    create_tested=create_tested.get("firstP"),
                    live=live.get("firstP"),
                    status="FAILED",
                    screenshot=screenshot_path
                )

                # 🔍 EXACT FAILURE REASON (LOG ONLY)
                missing = set(r["items"]) - set(l["items"])

                print(
                    f"\n❌ run_test verification failed at step {index}\n"
                    f"URL: {target_url}\n\n"
                    f"create_tested firstP:\n{create_tested.get('firstP')}\n\n"
                    f"Live firstP:\n{live.get('firstP')}\n\n"
                    f"Missing elements (tag, text):\n"
                    + "\n".join(f"- {m[0]}: {m[1][:120]}" for m in list(missing)[:5])
                )

        browser.close()

        print("✅ run_test verification completed successfully for all pages.")


    if has_failures:
        raise AssertionError(
            "\n❌ run_test completed with one or more verification failures.\n"
            "See run_test-report.html and screenshots for details.\n"
        )
