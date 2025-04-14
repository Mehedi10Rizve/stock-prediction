# Daily Stock Price Movement Prediction

This project predicts the **next day's stock movement direction** (up or down) for **Apple Inc. (AAPL)** using historical data, technical indicators, and a machine learning pipeline. It automatically runs daily using GitHub Actions and outputs a prediction that can be used with GitHub Pages.

---

## Features

-  Automated daily prediction via GitHub Actions  
-  Uses historical stock data from Yahoo Finance  
-  Machine Learning with technical indicators as features  
-  Predicts UP or DOWN movement  
-  Output as `prediction.json` for easy frontend integration  
-  Logging with `prediction.log` for monitoring  

---

## Project Structure

```
.
├── .github
│   └── workflows
│       └── daily.yml                    # GitHub Actions workflow to automate daily predictions
├── data
│   ├── database
│   │   └── stock_data.db               # SQLite database storing processed stock data
│   ├── processed
│   │   └── AAPL_processed.csv          # Cleaned and feature-engineered AAPL stock data
│   └── raw
│       └── AAPL_daily.csv              # Raw daily stock price data fetched from yfinance
├── docs
│   ├── index.html                      # Frontend dashboard (GitHub Pages)
│   ├── prediction.json                 # Latest model prediction in JSON format
│   ├── scripts.js                      # JavaScript for dynamic frontend updates
│   └── styles.css                      # Styling for the frontend dashboard
├── logs
│   └── prediction.log                  # Logs of daily prediction activities (for monitoring)
├── models
│   ├── stock_price_predictor.pkl       # Trained binary classification model (UP/DOWN)
│   └── scaler.pkl                      # Scaler used for feature normalization during training
├── pipelines
│   ├── fetch_and_process.py            # Pipeline for fetching, processing, and storing stock data
│   └── predict_new_data.py             # Pipeline for loading latest data and making predictions
├── src
│   ├── fetch_stock_data.py             # Fetch stock data from yfinance
│   ├── data_processing.py              # Perform feature engineering and indicator calculation
│   ├── insert_to_database.py           # Save processed data into the SQLite database
│   └── training_model.py               # Train the machine learning model and save artifacts
├── requirements.txt                    # List of Python dependencies for the project
├── README.md                           # Project overview, setup instructions, and documentation

```
---

## How It Works

1. **`fetch_and_process.py`**
   - Fetches AAPL stock data (last 300 days)
   - Calculates indicators like RSI, MACD, ATR, etc.
   - Stores the latest record in SQLite

2. **`predict_new_data.py`**
   - Loads the latest record
   - Scales it with a pre-fitted scaler
   - Predicts stock movement using a trained ML model
   - Saves results to `docs/prediction.json` and logs it

3. **GitHub Actions (`.github/workflows/daily.yml`)**
   - Runs daily at **00:00 UTC**
   - Automatically commits and pushes the prediction + logs

---

## 🔍 Technical Stack

- **Data Source**: Yahoo Finance (`yfinance`)
- **Model**: Scikit-learn classifier (binary classification)
- **Features**:
  - Lagged close prices (`lag_1` to `lag_10`)
  - Moving Averages (`ma_5`, `ma_10`, `ma_50`, `ma_200`)
  - Indicators: `RSI`, `MACD`, `Stochastic Oscillator`, `ATR`
- **Storage**: SQLite (`stock_data.db`)
- **Deployment**: GitHub Actions (scheduled + manual dispatch)

---

## Evaluation & Monitoring

- **Model Evaluation**:
  - Trained using a **train/test split**
  - Accuracy and F1-Score used for performance
- **Monitoring**:
  - Logs saved in `logs/prediction.log`
  - Easily review trends and model stability

---

## Frontend Integration

You can consume `docs/prediction.json` with:
-  GitHub Pages static frontend

---

## 🧪 Installation

Install dependencies:

```bash
pip install -r requirements.txt
