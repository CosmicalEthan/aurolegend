from playwright.sync_api import sync_playwright
import requests
import time

PRODUCT_URL = "https://www.target.com/p/case-mate-licensed-kate-spade-defensive-hardshell-case-for-iphone-xs-and-x-clear-pin-dot-gems/-/A-93670348#lnk=sametab"
DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1521055555479801938/4nbA7DbqXC0ushr3VkoOVmfuYC0NF7KhR6zSX-q2Eddrq9UIZ8OOmNdIrXCUHMIF9PV2"

def notify():
    requests.post(DISCORD_WEBHOOK, json={
        "content": "🔥 IN STOCK:\n" + PRODUCT_URL
    })

def check_stock(page):
    page.goto(PRODUCT_URL, wait_until="domcontentloaded")

    try:
        add_to_cart = page.locator("button:has-text('Add to cart')")
        ship_it = page.locator("button:has-text('Ship it')")

        return add_to_cart.count() > 0 or ship_it.count() > 0
    except:
        return False


with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    print("🚀 monitoring started")

    while True:
        if check_stock(page):
            notify()
            print("🔥 IN STOCK FOUND")
            break
        else:
            print("❌ out of stock")

        time.sleep(6)
