import traceback

@app.get("/search")
async def search(q: str):

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=True,
                args=[
                    "--no-sandbox",
                    "--disable-dev-shm-usage"
                ]
            )

            page = await browser.new_page()
            await page.goto(f"https://iparts.by/search/?q={q}", timeout=60000)

            await page.wait_for_timeout(4000)

            items = []

            texts = await page.locator("div").all_inner_texts()

            for t in texts:
                if "BYN" in t and len(t) < 200:
                    items.append({
                        "name": t[:80],
                        "price": "BYN"
                    })

                if len(items) >= 10:
                    break

            await browser.close()

            return items

    except Exception as e:
        return {
            "error": str(e),
            "trace": traceback.format_exc()
        }
