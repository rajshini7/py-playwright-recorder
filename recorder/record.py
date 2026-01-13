from playwright.sync_api import sync_playwright, Page
from recorder.login import login
from recorder.content import extract_content
from recorder.steps_store import save_steps


def record(base_url: str, username: str, password: str):
    steps = []
    last_url = None

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page: Page = browser.new_page()

        # 1️⃣ Login first (blocking until successful)
        login(page, base_url, username, password)

        # Initialize last_url after login
        last_url = page.url

        # 2️⃣ Navigation handler
        def on_navigation(frame):
            nonlocal last_url

            if frame != page.main_frame:
                return

            current_url = last_url
            target_url = page.url

            # Avoid duplicates / self-navigation
            if current_url == target_url:
                return

            content = extract_content(page)

            # ✅ OPTION-1: runtime sanity check (ONLY addition)
            print(f"[RECORD] extracted {len(content.get('visible_items', []))} visible items")

            steps.append({
                "current_url": current_url,
                "target_url": target_url,
                "content": content
            })

            last_url = target_url

        page.on("framenavigated", on_navigation)

        print("🔴 Recording... Perform clicks. Close the browser window to stop.")

        # 3️⃣ Wait until user closes browser (NO crash)
        try:
            page.wait_for_event("close")
        except Exception:
            pass

        # 4️⃣ Persist steps AFTER browser closes
        save_steps(steps)

        try:
            browser.close()
        except Exception:
            pass
