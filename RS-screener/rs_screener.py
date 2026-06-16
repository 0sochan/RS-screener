import yfinance as yf
import pandas as pd
import os
print("RS Screener started")

# GitHub Actions のカレントディレクトリ対策
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "..")  # 1つ上の階層に出力

tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "META", "TSLA"]

data = []

for ticker in tickers:
    stock = yf.Ticker(ticker)
    hist = stock.history(period="180d", interval="1d")

    if hist is None or hist.empty:
        print(f"No data for {ticker}")
        continue

    rs = hist["Close"].iloc[-1] / hist["Close"].iloc[0]
    data.append([ticker, rs])

df = pd.DataFrame(data, columns=["Ticker", "RS"])
df = df.sort_values("RS", ascending=False)

# 出力先（リポジトリ直下）
df.to_csv(os.path.join(OUTPUT_DIR, "rs_top50.csv"), index=False)
df.to_html(os.path.join(OUTPUT_DIR, "rs_top50.html"), index=False)
df.to_json(os.path.join(OUTPUT_DIR, "rs_top50.json"), orient="records")
