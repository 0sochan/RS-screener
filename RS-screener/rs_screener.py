import yfinance as yf
import pandas as pd
import os

# 出力先ディレクトリ（GitHub Actions でも確実に存在する）
OUTPUT_DIR = "RS-screener"

# ディレクトリが無ければ作成
os.makedirs(OUTPUT_DIR, exist_ok=True)

tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "META", "TSLA"]

data = []

for ticker in tickers:
    stock = yf.Ticker(ticker)
    hist = stock.history(period="6mo")

    if len(hist) == 0:
        continue

    rs = hist["Close"].iloc[-1] / hist["Close"].iloc[0]
    data.append([ticker, rs])

df = pd.DataFrame(data, columns=["Ticker", "RS"])
df = df.sort_values("RS", ascending=False)

# 出力（絶対に成功する）
df.to_csv(f"{OUTPUT_DIR}/rs_top50.csv", index=False)
df.to_html(f"{OUTPUT_DIR}/rs_top50.html", index=False)
df.to_json(f"{OUTPUT_DIR}/rs_top50.json", orient="records")
