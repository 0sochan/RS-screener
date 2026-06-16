
import yfinance as yf
import pandas as pd

# 取得する銘柄リスト（例としてS&P500の一部）
tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "META", "TSLA"]

data = []

for ticker in tickers:
    stock = yf.Ticker(ticker)
    hist = stock.history(period="6mo")

    if len(hist) == 0:
        continue

    # RS（相対力指数ではなく相対パフォーマンス）
    rs = hist["Close"].iloc[-1] / hist["Close"].iloc[0]

    data.append([ticker, rs])

df = pd.DataFrame(data, columns=["Ticker", "RS"])
df = df.sort_values("RS", ascending=False)

# 出力
df.to_csv("RS-screener/rs_top50.csv", index=False)
df.to_html("RS-screener/rs_top50.html", index=False)
df.to_json("RS-screener/rs_top50.json", orient="records")
