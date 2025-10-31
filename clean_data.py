# clean_data.py
import pandas as pd
import numpy as np

RAW = "ebay_tech_deals.csv"
OUT = "cleaned_ebay_deals.csv"

def cleanse_money(s):
    if pd.isna(s): return np.nan
    s = str(s)
    # keep only the first money-like token if multiple appear
    s = s.split("\n")[0]
    s = s.replace("US", "").replace("$", "").replace(",", "").strip()
    return s if s else np.nan

def main():
    df = pd.read_csv(RAW, dtype=str)
    for col in ["price","original_price","shipping","title","item_url","timestamp"]:
        if col not in df.columns: df[col] = ""

    df["price"] = df["price"].map(cleanse_money)
    df["original_price"] = df["original_price"].map(cleanse_money)

    # If original_price missing -> use price
    df["original_price"] = np.where(df["original_price"].isna() | (df["original_price"]==""), df["price"], df["original_price"])

    # Shipping defaults
    df["shipping"] = df["shipping"].fillna("").astype(str).str.strip()
    df["shipping"] = df["shipping"].replace({"": "Shipping info unavailable", "N/A": "Shipping info unavailable"})

    # To numeric
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df["original_price"] = pd.to_numeric(df["original_price"], errors="coerce")

    # Discount %
    df["discount_percentage"] = np.where(
        df["original_price"]>0,
        np.round((df["original_price"] - df["price"]) / df["original_price"] * 100.0, 2),
        np.nan
    )

    df.to_csv(OUT, index=False)

if __name__ == "__main__":
    main()
