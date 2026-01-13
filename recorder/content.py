from playwright.sync_api import Page


def extract_content(page: Page):
    # Ensure page is ready
    page.wait_for_load_state("domcontentloaded")

    # Run ONE browser-context extraction (fast & accurate)
    extracted = page.evaluate(
        """
        () => {
            const isVisible = (el) => {
                const style = window.getComputedStyle(el);
                const rect = el.getBoundingClientRect();
                return (
                    style &&
                    style.visibility !== "hidden" &&
                    style.display !== "none" &&
                    rect.width > 0 &&
                    rect.height > 0
                );
            };

            const seen = new Set();
            const items = [];

            const walker = document.createTreeWalker(
                document.body,
                NodeFilter.SHOW_ELEMENT,
                null
            );

            let node;
            while ((node = walker.nextNode())) {
                if (!isVisible(node)) continue;

                const text = node.innerText?.trim();
                if (!text || text.length < 20) continue;

                if (seen.has(text)) continue;
                seen.add(text);

                const rect = node.getBoundingClientRect();

                items.push({
                    tag: node.tagName.toLowerCase(),
                    text: text.slice(0, 500), // guard against huge blobs
                    bbox: {
                        top: Math.round(rect.top),
                        left: Math.round(rect.left),
                        width: Math.round(rect.width),
                        height: Math.round(rect.height)
                    },
                    scrollY: Math.round(window.scrollY)
                });
            }

            const firstParagraph = (() => {
                const ps = document.querySelectorAll("p");
                for (const p of ps) {
                    if (isVisible(p)) {
                        const t = p.innerText.trim();
                        if (t) return t;
                    }
                }
                return null;
            })();

            return {
                title: document.title || null,
                h1: document.querySelector("h1")?.innerText.trim() || null,
                firstP: firstParagraph,
                visible_items: items,
                maxScrollY: Math.max(
                    document.body.scrollHeight,
                    document.documentElement.scrollHeight
                )
            };
        }
        """
    )

    return extracted
