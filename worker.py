from fastapi import FastAPI
from playwright.async_api import async_playwright

app = FastAPI()

@app.get("/search")
async def search(q: str):

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-dev-shm-usage"]
        )

        page = await browser.new_page()

        await page.goto(f"https://iparts.by/search/?q={q}", timeout=60000)
        await page.wait_for_timeout(3000)

        items = []

        elements = await page.query_selector_all("div")

        for el in elements:
            text = await el.inner_text()

            if "BYN" in text and len(text) < 200:
                lines = text.split("\n")

                if len(lines) >= 2:
                    items.append({
                        "name": lines[0],
                        "price": lines[-1]
                    })

            if len(items) >= 10:
                break

        await browser.close()

        return items
