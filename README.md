# eBay Tech Deals — Scrape · Clean · Analyze

## What this repo does
- Scrapes all visible products from eBay Global Tech Deals (no hard limit).
- Appends to `ebay_tech_deals.csv`.
- GitHub Actions runs every 3 hours to grow the dataset (≈2 days).
- Cleans to `cleaned_ebay_deals.csv`.
- EDA notebook visualizes price/discount/time/keywords/shipping.

## How to run locally
```bash
pip install -r requirements.txt
python scraper.py
python clean_data.py
jupyter notebook EDA.ipynb
