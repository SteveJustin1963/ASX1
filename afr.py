import webbrowser
import time

print("Paste your ASX tickers (one per line), then press Ctrl+D (or Ctrl+Z on Windows) to finish:")

# Read multiline input from user
import sys
tickers_raw = sys.stdin.read()

# Split by lines and clean up
tickers = [line.strip().lower() for line in tickers_raw.splitlines() if line.strip()]

# AFR base URL
base_url = "https://www.afr.com/company/asx/{}"

# Open each ticker's AFR page in a new tab
for ticker in tickers:
    url = base_url.format(ticker)
    print(f"Opening {url}")
    webbrowser.open_new_tab(url)
    time.sleep(0.5)  # Optional delay
