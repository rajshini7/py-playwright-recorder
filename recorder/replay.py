from playwright.sync_api import sync_playwright
from recorder.login import login
from recorder.content import extract_content
from recorder.steps_store import load_steps
from recorder.report import generate_report
from pathlib import Path

def normalize(text):
    if not text:
        return ""
    return " ".join(text.split()).strip()

def replay(base_url, username, password):
    steps = load_steps()
    results = []
    failed = False

    screenshots_dir = Path("reports/screenshots")
    screenshots_dir.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Login
        login(page, base_url, username, password)

        for index, step in enumerate(steps, start=1):
            target_url = step["target_url"]
            recorded = normalize(step["content"].get("firstP"))

            page.goto(target_url)
            live = normalize(extract_content(page).get("firstP"))

            status = "PASS" if recorded == live else "FAIL"
            screenshot_path = None

            if status == "FAIL":
                failed = True
                screenshot_path = screenshots_dir / f"step_{index}.png"
                page.screenshot(path=str(screenshot_path), full_page=True)

            results.append({
                "step": index,
                "url": target_url,
                "recorded": recorded,
                "live": live,
                "status": status,
                "screenshot": str(screenshot_path) if screenshot_path else None
            })

            print(f"{'✅' if status == 'PASS' else '❌'} Step {index} → {target_url}")

        browser.close()

    # Always generate report
    generate_report(results)

    # Fail AFTER report is written
    if failed:
        raise AssertionError(
            "Replay verification failed. "
            "See reports/replay-report.html for details."
        )
