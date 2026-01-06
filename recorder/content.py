from playwright.sync_api import Page

def extract_content(page: Page):
    # Ensure page is fully loaded
    page.wait_for_load_state("domcontentloaded")

    # Prefer semantic containers
    content_root = None

    for selector in ["main", "article", "#content", ".content"]:
        if page.locator(selector).count() > 0:
            content_root = page.locator(selector)
            break

    if content_root is None:
        content_root = page.locator("body")

    # Get first visible paragraph inside content
    paragraphs = content_root.locator("p").filter(has_text="")

    first_p = None
    for i in range(paragraphs.count()):
        p = paragraphs.nth(i)
        if p.is_visible():
            text = p.inner_text().strip()
            if text:
                first_p = text
                break

    return {
        "title": page.title(),
        "h1": page.locator("h1").first.inner_text().strip()
              if page.locator("h1").count() > 0 else None,
        "firstP": first_p
    }
