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

## 🛠️ Project Structure

stock-prediction/ │ ├── data/ │ └── database/ │ └── stock_data.db # SQLite database │ ├── models/ │ ├── stock_price_predictor.pkl # Trained model │ └── scaler.pkl # Fitted MinMaxScaler │ ├── pipelines/ │ ├── fetch_and_process.py # Fetch data + feature engineering │ └── predict_new_data.py # Load model + make prediction │ ├── docs/ │ └── prediction.json # Latest prediction output │ ├── logs/ │ └── prediction.log # Log file for monitoring │ ├── .github/ │ └── workflows/ │ └── daily.yml # GitHub Actions workflow │ └── README.md # This file

---

## ⚙️ How It Works

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

## 📊 Evaluation & Monitoring

- **Model Evaluation**:
  - Trained using a **train/test split**
  - Accuracy and F1-Score used for performance
- **Monitoring**:
  - Logs saved in `logs/prediction.log`
  - Easily review trends and model stability

---

## 💻 Frontend Integration

You can consume `docs/prediction.json` with:
- 🌐 GitHub Pages static frontend
- 📊 Streamlit Dashboard
- 🧩 Any React or JavaScript app

---

## 🧪 Installation

Install dependencies:

```bash
pip install -r requirements.txt
