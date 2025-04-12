import pandas as pd
from ta.momentum import RSIIndicator, StochasticOscillator
from ta.trend import MACD
from ta.volatility import AverageTrueRange
import os

STOCK_SYMBOL = "AAPL"
RAW_DATA_PATH = "data/raw/AAPL_daily.csv"
PROCESSED_DATA_PATH = "data/processed/AAPL_processed.csv"

def process_data(df):
    print("Processing data...")

    df = df[['date', 'Open', 'High', 'Low', 'Close', 'Volume', 'symbol']].copy()
    df.sort_values('date', inplace=True)
    df.reset_index(drop=True, inplace=True)

    # Ensure numeric columns are really numeric
    for col in ['Open', 'High', 'Low', 'Close', 'Volume']:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # Lag features (1-10)
    for lag in range(1, 11):
        df[f'lag_{lag}'] = df['Close'].shift(lag)

    # Moving averages
    df['ma_5'] = df['Close'].rolling(window=5).mean()
    df['ma_10'] = df['Close'].rolling(window=10).mean()
    df['ma_50'] = df['Close'].rolling(window=50).mean()
    df['ma_200'] = df['Close'].rolling(window=200).mean()

    # Technical indicators
    df['RSI'] = RSIIndicator(close=df['Close']).rsi()
    stoch = StochasticOscillator(high=df['High'], low=df['Low'], close=df['Close'])
    df['StochasticOscillator'] = stoch.stoch()
    macd = MACD(close=df['Close'])
    df['MACD'] = macd.macd()
    df['MACD_signal'] = macd.macd_signal()
    atr = AverageTrueRange(high=df['High'], low=df['Low'], close=df['Close'])
    df['ATR'] = atr.average_true_range()

    # Calculate the next day movement (binary classification: 1 for up, 0 for down)
    df['next_day_movement'] = (df['Close'].shift(-1) > df['Close']).astype(int)

    # Drop rows with NaNs
    df.dropna(inplace=True)

    return df

def main():
    df = pd.read_csv(RAW_DATA_PATH)
    processed_df = process_data(df)
    os.makedirs(os.path.dirname(PROCESSED_DATA_PATH), exist_ok=True)
    processed_df.to_csv(PROCESSED_DATA_PATH, index=False)
    print(f"Saved processed data to {PROCESSED_DATA_PATH}")

if __name__ == "__main__":
    main()
