import yfinance as yf
import os
import pandas as pd
import statistics
import matplotlib.pyplot as plt

# -- User input -----------------------------
try:
    days = int(input("How many days of Bitcoin closing prices? (e.g. 10): ").strip())
    if days < 2:
        raise ValueError
except ValueError:
    print("Invalid number of days. Must be at least 2.")
    exit()

# -- Bitcoin Data Fetch ---------------------
btc = yf.Ticker("BTC-USD")
btc_hist = btc.history(period=f"{days}d")
btc_closes = btc_hist['Close'].dropna().tolist()

if len(btc_closes) < 2:
    print("Not enough Bitcoin data available.")
    exit()

btc_closes_rounded = [round(c, 2) for c in btc_closes]
btc_pct_change = round(((btc_closes[-1] - btc_closes[0]) / btc_closes[0]) * 100, 2)
avg_price = statistics.mean(btc_closes)
stdev = statistics.stdev(btc_closes)
pct_stdev = round((stdev / avg_price) * 100, 2)

# -- Save data to CSV on Desktop ------------
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
csv_path = os.path.join(desktop_path, f"Bitcoin_{days}d_result.csv")

df = pd.DataFrame([{
    f'Last {len(btc_closes)} Closes': btc_closes_rounded,
    'Change (%)': f"{btc_pct_change}%",
    'Stdev (%)': f"{pct_stdev}%"
}])
df.to_csv(csv_path, index=False)

# -- Plot closing prices --------------------
plt.figure(figsize=(10, 5))
plt.plot(btc_closes_rounded, marker='o', linestyle='-')
plt.title(f"Bitcoin Closing Prices (Last {days} Days)")
plt.xlabel("Days Ago (0 = Most Recent)")
plt.ylabel("Price (USD)")
plt.grid(True)

# -- Save plot to PNG on Desktop ------------
plot_path = os.path.join(desktop_path, f"Bitcoin_{days}d_plot.png")
plt.savefig(plot_path)

print(f"\nDone! Data saved to:\n{csv_path}\nPlot saved to:\n{plot_path}")
