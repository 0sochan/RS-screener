import yfinance as yf
import pandas as pd
import os

OUTPUT_DIR = "RS-screener"
os.makedirs(OUTPUT_DIR, exist_ok=True)

tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "META", "TSLA"]

data = []

for ticker in tickers:
    stock = yf.Ticker(ticker)

    # GitHub Actions でも確実に返る interval="1d" 指定
    hist = stock.history(period="180d", interval="1d")

    if hist is None or hist.empty:
        print(f"No data for {ticker}")
        continue

    rs = hist["Close"].iloc[-1] / hist["Close"].iloc[0]
    data.append([ticker, rs])

df = pd.DataFrame(data, columns=["Ticker", "RS"])
df = df.sort_values("RS", ascending=False)

df.to_csv(f"{OUTPUT_DIR}/rs_top50.csv", index=False)
df.to_html(f"{OUTPUT_DIR}/rs_top50.html", index=False)
df.to_json(f"{OUTPUT_DIR}/rs_top50.json", orient="records")
