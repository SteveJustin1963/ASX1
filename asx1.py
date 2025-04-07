import requests
import csv
import io
import yfinance as yf
import os
import pandas as pd
import itertools
import sys
import time
import statistics

# -- User input -----------------------------
letter = input("Enter first letter of ASX code (A-Z): ").strip().upper()
if not letter.isalpha() or len(letter) != 1:
    print("Invalid input. Please enter a single A-Z letter.")
    exit()

try:
    days = int(input("How many days of closing prices? (e.g. 10): ").strip())
    if days < 2:
        raise ValueError
except ValueError:
    print("Invalid number of days. Must be at least 2.")
    exit()

# -- Download ASX list ----------------------
url = 'https://www.asx.com.au/asx/research/ASXListedCompanies.csv'
response = requests.get(url)
response.raise_for_status()

csv_data = response.content.decode('utf-8')
csv_reader = csv.reader(io.StringIO(csv_data))
next(csv_reader)
next(csv_reader)

tickers = [row[1].strip() for row in csv_reader if row[1].strip().upper().startswith(letter)]

# -- Fetch and filter Yahoo Finance data ----
results = []
spinner = itertools.cycle(["|", "/", "-", "\\"])

for code in tickers:
    yahoo_ticker = code + ".AX"
    try:
        stock = yf.Ticker(yahoo_ticker)
        hist = stock.history(period=f"{days}d")

        closes = hist['Close'].dropna().tolist()
        volumes = hist['Volume'].dropna().tolist()

        if len(closes) < 2:
            continue

        closes_rounded = [round(c, 2) for c in closes]
        pct_change = round(((closes[-1] - closes[0]) / closes[0]) * 100, 2)

        avg_price = statistics.mean(closes)
        stdev = statistics.stdev(closes)
        pct_stdev = round((stdev / avg_price) * 100, 2)

        total_volume = int(sum(volumes))

        results.append({
            'ASX Code': code,
            f'Last {len(closes)} Closes': closes_rounded,
            'Change (%)': f"{pct_change}%",
            'Stdev (%)': f"{pct_stdev}%",
            'Volume Traded': total_volume
        })

    except:
        pass

    sys.stdout.write(f"\rProcessing {code}... {next(spinner)}")
    sys.stdout.flush()
    time.sleep(0.05)

# -- Save to Desktop ------------------------
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop", f"ASX_{letter}_{days}d_result.csv")
df = pd.DataFrame(results)
df.to_csv(desktop_path, index=False)

print(f"\nDone! Saved to: {desktop_path}")
