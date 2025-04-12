import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from ta.momentum import RSIIndicator, StochasticOscillator
from ta.trend import MACD
from ta.volatility import AverageTrueRange
import sqlite3

# Constants
STOCK_SYMBOL = "AAPL"
DB_PATH = "data/database/stock_data.db"
END_DATE = datetime.today().strftime('%Y-%m-%d')
START_DATE = (datetime.today() - timedelta(days=300)).strftime('%Y-%m-%d')  # 300 to cover long indicators

def fetch_stock_data(symbol):
    print(f"Fetching {symbol} from {START_DATE} to {END_DATE}...")
    stock_data = yf.download(symbol, start=START_DATE, end=END_DATE)

    if stock_data.empty:
        print(f"❌ No data fetched for {symbol}.")
        return None

    # Flatten the multi-level column names to make access easier
    stock_data.columns = [col[0] for col in stock_data.columns]

    stock_data.reset_index(inplace=True)
    stock_data['symbol'] = symbol
    print("Fetched DataFrame:", stock_data.head())
    return stock_data

def process_data(df):
    print("Processing data...")

    # Rename 'Date' to 'date' for consistency
    df.rename(columns={'Date': 'date'}, inplace=True)

    df = df[['date', 'Open', 'High', 'Low', 'Close', 'Volume', 'symbol']].copy()
    df.sort_values('date', inplace=True)
    df.reset_index(drop=True, inplace=True)

    for col in ['Open', 'High', 'Low', 'Close', 'Volume']:
        print(f"Checking column: {col} - Type: {type(df[col])}")
        if isinstance(df[col], pd.Series):
            df[col] = pd.to_numeric(df[col], errors='coerce')
        else:
            print(f"❌ Column {col} is not a pandas Series!")

    for lag in range(1, 11):
        df[f'lag_{lag}'] = df['Close'].shift(lag)

    df['ma_5'] = df['Close'].rolling(window=5).mean()
    df['ma_10'] = df['Close'].rolling(window=10).mean()
    df['ma_50'] = df['Close'].rolling(window=50).mean()
    df['ma_200'] = df['Close'].rolling(window=200).mean()

    if len(df) >= 14:
        df['RSI'] = RSIIndicator(close=df['Close']).rsi()
        stoch = StochasticOscillator(high=df['High'], low=df['Low'], close=df['Close'])
        df['StochasticOscillator'] = stoch.stoch()
        macd = MACD(close=df['Close'])
        df['MACD'] = macd.macd()
        df['MACD_signal'] = macd.macd_signal()
        atr = AverageTrueRange(high=df['High'], low=df['Low'], close=df['Close'])
        df['ATR'] = atr.average_true_range()
    else:
        df[['RSI', 'StochasticOscillator', 'MACD', 'MACD_signal', 'ATR']] = None

    # Calculate the next day movement (binary classification: 1 for up, 0 for down)
    df['next_day_movement'] = (df['Close'].shift(-1) > df['Close']).astype(int)

    df.dropna(inplace=True)
    print(f"Processed DataFrame:\n{df.tail()}")
    return df

def already_exists(date_str):
    # Ensure date_str is a string if it's a Timestamp
    if isinstance(date_str, pd.Timestamp):
        date_str = date_str.strftime('%Y-%m-%d')

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM stock_data WHERE date = ?", (date_str,))
    exists = c.fetchone()[0] > 0
    conn.close()
    return exists


def insert_data_to_db(df):
    if df.empty:
        print("❌ DataFrame is empty. No data to insert.")
        return

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    create_table_query = '''CREATE TABLE IF NOT EXISTS stock_data (
        date TEXT,
        Close REAL,
        High REAL,
        Low REAL,
        Open REAL,
        Volume INTEGER,
        symbol TEXT,
        lag_1 REAL,
        lag_2 REAL,
        lag_3 REAL,
        lag_4 REAL,
        lag_5 REAL,
        lag_6 REAL,
        lag_7 REAL,
        lag_8 REAL,
        lag_9 REAL,
        lag_10 REAL,
        ma_5 REAL,
        ma_10 REAL,
        ma_50 REAL,
        ma_200 REAL,
        RSI REAL,
        StochasticOscillator REAL,
        MACD REAL,
        MACD_signal REAL,
        ATR REAL,
        next_day_movement INTEGER,
        PRIMARY KEY (date, symbol)
    )'''
    c.execute(create_table_query)

    df['date'] = pd.to_datetime(df['Date']).dt.strftime('%Y-%m-%d')

    columns = [
        'date', 'Close', 'High', 'Low', 'Open', 'Volume', 'symbol',
        'lag_1', 'lag_2', 'lag_3', 'lag_4', 'lag_5',
        'lag_6', 'lag_7', 'lag_8', 'lag_9', 'lag_10',
        'ma_5', 'ma_10', 'ma_50', 'ma_200',
        'RSI', 'StochasticOscillator', 'MACD', 'MACD_signal', 'ATR', 'next_day_movement'
    ]
    placeholders = ','.join(['?'] * len(columns))
    insert_query = f'INSERT OR REPLACE INTO stock_data ({",".join(columns)}) VALUES ({placeholders})'

    for _, row in df.iterrows():
        values = tuple(row[col] for col in columns)
        c.execute(insert_query, values)

    conn.commit()
    conn.close()

def main():
    df = fetch_stock_data(STOCK_SYMBOL)
    if df is None:
        print("❌ No data to process.")
        return

    processed_df = process_data(df)
    if processed_df.empty:
        print("❌ Processed data is empty, nothing to insert.")
        return

    latest_df = processed_df.iloc[[-1]]
    latest_date = latest_df['date'].iloc[0]

    if already_exists(latest_date):
        print(f"ℹ️ Data for {latest_date} already exists. Skipping insert.")
    else:
        print(f"Inserting data for {latest_date}...")
        insert_data_to_db(latest_df)
        print("✅ Data inserted.")

if __name__ == "__main__":
    main()
