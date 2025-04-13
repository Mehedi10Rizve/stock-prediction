import sqlite3
import joblib
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import os
import json
from datetime import datetime, timezone
import logging

DB_PATH = "data/database/stock_data.db"
MODEL_PATH = "models/stock_price_predictor.pkl"
SCALER_PATH = "models/scaler.pkl"

def load_data_from_db():
    """Load the latest available processed row from the SQLite database"""
    print("📦 Loading latest data from database...")
    conn = sqlite3.connect(DB_PATH)
    query = "SELECT * FROM stock_data WHERE date = (SELECT MAX(date) FROM stock_data)"
    df = pd.read_sql(query, conn)
    conn.close()

    if df.empty:
        print("❌ No data found in database.")
        return None

    print(f"✅ Data loaded for date: {df['date'].iloc[0]}")
    return df

def preprocess_data_for_prediction(df):
    """Prepare the data for model prediction"""
    print("⚙️ Preprocessing data for prediction...")

    # Drop non-feature columns
    df = df.drop(columns=['date', 'symbol'])

    # Load the pre-fitted scaler
    scaler = joblib.load(SCALER_PATH)

    # Feature scaling (assuming features are similar to the training file)
    features = df.drop(columns=['next_day_movement'])  # Drop the target column
    scaled_features = scaler.transform(features)

    # Convert to DataFrame
    df_scaled = pd.DataFrame(scaled_features, columns=features.columns)

    return df_scaled, scaler

def predict_movement(df_scaled, model):
    """Predict the next day's stock price movement (up or down)"""
    print("📈 Making prediction...")

    # Predict the next movement
    predicted_movement = model.predict(df_scaled)

    return predicted_movement

def main():
    df = load_data_from_db()
    if df is None:
        print("⚠️ Skipping prediction due to missing data.")
        return

    df_scaled, scaler = preprocess_data_for_prediction(df)

    # Load the trained model
    model = joblib.load(MODEL_PATH)

    # Predict the next day's movement (up/down)
    predicted_movement = predict_movement(df_scaled, model)

    # Output prediction result
    if predicted_movement[0] == 1:
        print("🔮 Predicted next day's stock movement: Up")
    else:
        print("🔮 Predicted next day's stock movement: Down")
    

    # 🔽 Add this section only: Export to JSON for GitHub Pages
    output = {
        "date": df['date'].iloc[0],
        "prediction": f"Apple Inc share is expected to go {'UP' if predicted_movement[0] == 1 else 'DOWN'}",
        "updated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    }

    os.makedirs("docs", exist_ok=True)
    with open("docs/prediction.json", "w") as f:
        json.dump(output, f)
    
    print("✅ Prediction saved to 'docs/prediction.json'")

    # 🧾 Log prediction result for monitoring
    os.makedirs("logs", exist_ok=True)
    logging.basicConfig(
        filename='logs/prediction.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    log_msg = f"Prediction for {output['date']}: {output['prediction']}"
    logging.info(log_msg)

if __name__ == "__main__":
    main()
