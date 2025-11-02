import pandas as pd
import numpy as np
import re

RAW = "ebay_tech_deals.csv"
OUT = "cleaned_ebay_deals.csv"

def cleanse_money(s):
    if pd.isna(s): return np.nan
    s = str(s)
    match = re.search(r"\d+(?:\.\d+)?", s.replace(",", ""))
    return float(match.group()) if match else np.nan

def main():
    df = pd.read_csv(RAW, dtype=str)

    # Normalize and check columns
    df.columns = df.columns.str.strip().str.lower()
    for col in ["price","original_price","shipping","title","item_url","timestamp"]:
        if col not in df.columns:
            df[col] = ""

    # Drop N/A or empty product entries
    df = df.dropna(subset=["title"])
    df = df[df["title"].str.strip().str.lower() != "n/a"]
    df = df[df["item_url"].str.contains("/itm/")]

    # Clean price fields
    df["price"] = df["price"].map(cleanse_money)
    df["original_price"] = df["original_price"].map(cleanse_money)

    # Fill missing original price
    df["original_price"] = np.where(
        df["original_price"].isna() | (df["original_price"] == 0),
        df["price"],
        df["original_price"]
    )

    # Shipping info
    df["shipping"] = df["shipping"].fillna("").astype(str).str.strip()
    df["shipping"] = df["shipping"].replace(
        {"": "Shipping info unavailable", "N/A": "Shipping info unavailable"}
    )

    # Discount %
    df["discount_percentage"] = np.where(
        df["original_price"] > 0,
        np.round((df["original_price"] - df["price"]) / df["original_price"] * 100.0, 2),
        np.nan
    )

    df.to_csv(OUT, index=False)
    print(f"✅ Cleaned data saved to {OUT}. Rows kept: {len(df)}")

if __name__ == "__main__":
    main()
