# scraper.py (fixed stable version)
import csv, os, time, re
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

URL = "https://www.ebay.com/globaldeals/tech"
OUT = "ebay_tech_deals.csv"

def setup_driver():
    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--window-size=1920,1080")
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=opts)

def scroll_to_bottom(driver, pause=1.0, stagnant_rounds=3):
    last_h = 0
    still = 0
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(pause)
        h = driver.execute_script("return document.body.scrollHeight")
        if h == last_h:
            still += 1
            if still >= stagnant_rounds:
                break
        else:
            still = 0
            last_h = h

def safe_text(node, selector):
    try:
        return node.find_element(By.CSS_SELECTOR, selector).text.strip()
    except Exception:
        return "N/A"

def safe_href(node, selector):
    try:
        return node.find_element(By.CSS_SELECTOR, selector).get_attribute("href")
    except Exception:
        return "N/A"

def clean_shipping(text):
    if not text:
        return "Shipping info unavailable"
    text = re.sub(r"\s+", " ", text.strip())
    text = re.sub(
        r"(?i)(see details( for shipping)?|read item description( or contact seller for shipping options)?|contact seller for shipping options)",
        "",
        text,
    )
    return text.strip(" .")

def main():
    driver = setup_driver()
    driver.get(URL)

    WebDriverWait(driver, 15).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".dne-itemtile, li.ebayui-dne-item-featured-card"))
    )
    scroll_to_bottom(driver)

    tiles = driver.find_elements(By.CSS_SELECTOR, ".dne-itemtile, li.ebayui-dne-item-featured-card")
    print(f"Found {len(tiles)} products")

    # First: gather static info (no navigation yet)
    product_data = []
    for t in tiles:
        title = safe_text(t, "h3.dne-itemtile-title, a.dne-itemtile-title")
        price = safe_text(t, ".dne-itemtile-price .itemtile-price-bold, .dne-itemtile-price .first, .dne-itemtile-price")
        original_price = safe_text(t, ".itemtile-price-strikethrough, .strike")
        item_url = safe_href(t, "a.dne-itemtile-title, a")
        product_data.append([title, price, original_price, item_url])

    ts = datetime.now().isoformat(timespec="seconds")
    rows = []

    # Second: visit each URL and grab shipping
    for i, (title, price, original_price, item_url) in enumerate(product_data, start=1):
        try:
            driver.get(item_url)
            shipping_elem = WebDriverWait(driver, 7).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.ux-labels-values__values-content"))
            )
            shipping = clean_shipping(shipping_elem.text)
        except Exception:
            shipping = "Shipping info unavailable"

        rows.append([ts, title, price, original_price, shipping, item_url])
        print(f"[{i}/{len(product_data)}] Scraped: {title[:60]}")
        time.sleep(1.0)

    # Save CSV
    write_header = not os.path.exists(OUT)
    with open(OUT, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if write_header:
            writer.writerow(["timestamp", "title", "price", "original_price", "shipping", "item_url"])
        writer.writerows(rows)

    driver.quit()
    print(f"✅ Scraping complete. Saved {len(rows)} rows to {OUT}")

if __name__ == "__main__":
    main()
