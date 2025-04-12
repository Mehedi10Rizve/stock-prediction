import sqlite3
import pandas as pd
import os

DB_PATH = "data/database/stock_data.db"
CSV_PATH = "data/processed/AAPL_processed.csv"

def create_table(cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS stock_data (
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
    )''')

def insert_data_to_db(df):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    create_table(c)

    columns = [
        'date', 'Close', 'High', 'Low', 'Open', 'Volume', 'symbol',
        'lag_1', 'lag_2', 'lag_3', 'lag_4', 'lag_5', 'lag_6', 'lag_7', 'lag_8', 'lag_9', 'lag_10',
        'ma_5', 'ma_10', 'ma_50', 'ma_200', 'RSI', 'StochasticOscillator', 'MACD', 'MACD_signal', 'ATR',
        'next_day_movement'
    ]

    placeholders = ','.join(['?'] * len(columns))
    insert_query = f'INSERT OR REPLACE INTO stock_data ({",".join(columns)}) VALUES ({placeholders})'

    for _, row in df.iterrows():
        values = tuple(row[col] for col in columns)
        c.execute(insert_query, values)

    conn.commit()
    conn.close()
    print("Database inserted successfully.")

def main():
    print("Loading processed data...")
    df = pd.read_csv(CSV_PATH)
    print("Creating database and table...")
    insert_data_to_db(df)

if __name__ == "__main__":
    main()
