from playwright.sync_api import Page

def login(page: Page, base_url: str, username: str, password: str):
    page.goto(base_url)

    page.wait_for_selector("#username", timeout=15000)
    page.fill("#username", username)

    page.wait_for_selector("#password", timeout=15000)
    page.fill("#password", password)

    page.wait_for_selector("button#submit", timeout=15000)
    page.click("button#submit")

    page.wait_for_url("**/logged-in-successfully/**", timeout=15000)
