import os
import yfinance as yf
import time
from datetime import datetime, timedelta

# Stock symbol for Apple
STOCK_SYMBOL = "AAPL"
SAVE_PATH = "data/raw"

# Calculate date range (2 years ago to today)
END_DATE = datetime.today()
START_DATE = END_DATE - timedelta(days=2*365)

def fetch_stock_data(symbol):
    print(f"Fetching {symbol}...")
    try:
        stock_data = yf.download(symbol, start=START_DATE, end=END_DATE)
        
        # Add a symbol column to identify the stock in the data
        stock_data['symbol'] = symbol

        # Reset index and rename columns
        stock_data.reset_index(inplace=True)
        stock_data.rename(columns={'Date': 'date'}, inplace=True)

        # Save the data to a CSV file
        filename = os.path.join(SAVE_PATH, f"{symbol}_daily.csv")
        stock_data.to_csv(filename, index=False)
        print(f"Saved {symbol} to {filename}")
    except Exception as e:
        print(f"Error fetching {symbol}: {e}")

def main():
    os.makedirs(SAVE_PATH, exist_ok=True)
    fetch_stock_data(STOCK_SYMBOL)

if __name__ == "__main__":
    main()
