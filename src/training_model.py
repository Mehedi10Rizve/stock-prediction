import sqlite3
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.metrics import accuracy_score, classification_report, roc_auc_score
import joblib
import xgboost as xgb
from imblearn.over_sampling import SMOTE
from scipy.stats import uniform, randint
import os

def load_data_from_db():
    """Load data from the SQLite database"""
    print("📦 Loading data from database...")
    conn = sqlite3.connect('data/database/stock_data.db')
    query = "SELECT * FROM stock_data"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def preprocess_data(df):
    """Preprocess the data for model training"""
    print("⚙️ Preprocessing data for training...")

    # Drop non-feature columns and handle missing values
    df = df.drop(columns=['date', 'symbol'])
    df.fillna(method='ffill', inplace=True)

    # Feature scaling
    scaler = MinMaxScaler()
    features = df.drop(columns=['next_day_movement'])
    scaled_features = scaler.fit_transform(features)

    # Add target column to the scaled features
    df_scaled = pd.DataFrame(scaled_features, columns=features.columns)
    df_scaled['next_day_movement'] = df['next_day_movement']

    # Split data into features (X) and target (y)
    X = df_scaled.drop(columns=['next_day_movement'])
    y = df_scaled['next_day_movement']

    return X, y, scaler

def tune_hyperparameters(X_train, y_train):
    """Perform RandomizedSearchCV to tune hyperparameters of the model"""
    model = xgb.XGBClassifier(random_state=42, objective='binary:logistic', eval_metric='logloss')

    # Define the parameter grid for RandomizedSearchCV
    param_dist = {
        'n_estimators': randint(50, 200),
        'max_depth': randint(3, 10),
        'learning_rate': uniform(0.01, 0.1),
        'subsample': uniform(0.7, 0.3),
        'colsample_bytree': uniform(0.7, 0.3),
        'scale_pos_weight': [1, 2, 3]  # Address class imbalance
    }

    # Randomized search with 3-fold cross-validation
    random_search = RandomizedSearchCV(estimator=model, param_distributions=param_dist,
                                       n_iter=100, cv=3, verbose=2, random_state=42, n_jobs=-1)

    random_search.fit(X_train, y_train)

    print("Best hyperparameters found: ", random_search.best_params_)

    return random_search.best_estimator_

def evaluate_model(model, X_test, y_test):
    """Evaluate the model on the test data"""
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {accuracy}")
    print("Classification Report:")
    print(classification_report(y_test, y_pred))
    
    # ROC-AUC score
    roc_auc = roc_auc_score(y_test, model.predict_proba(X_test)[:, 1])
    print(f"ROC-AUC: {roc_auc}")

def save_model_and_scaler(model, scaler):
    """Save the trained model and scaler to disk"""
    os.makedirs('models', exist_ok=True)
    joblib.dump(model, 'models/stock_price_predictor.pkl')
    joblib.dump(scaler, 'models/scaler.pkl')

def main():
    """Main function to load data, train model, and save"""
    # Load data
    df = load_data_from_db()

    # Preprocess data
    X, y, scaler = preprocess_data(df)

    # Split data into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Apply SMOTE for oversampling minority class
    smote = SMOTE(random_state=42)
    X_train_res, y_train_res = smote.fit_resample(X_train, y_train)
    print(f"Resampled data: {X_train_res.shape[0]} samples")

    # Perform hyperparameter tuning using RandomizedSearchCV
    model = tune_hyperparameters(X_train_res, y_train_res)

    # Evaluate the model
    evaluate_model(model, X_test, y_test)

    # Save the model and scaler
    save_model_and_scaler(model, scaler)

if __name__ == "__main__":
    main()
