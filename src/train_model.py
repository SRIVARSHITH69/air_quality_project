# src/train_model.py

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import joblib

from src.data_preprocessing import load_data, clean_data, save_clean_data

def train():
    # 1️⃣ Load raw CSV
    df = load_data('data/raw/AQI.csv')

    # 2️⃣ Clean & pivot
    cleaned_df = clean_data(df)

    # 3️⃣ Save cleaned version for reuse
    save_clean_data(cleaned_df, 'data/processed/cleaned_AQI.csv')
    print("✅ Cleaned data saved to data/processed/cleaned_AQI.csv")

    # 4️⃣ Prepare data
    FEATURES = ['CO', 'NH3', 'NO2', 'OZONE', 'PM10', 'SO2']
    TARGET = 'PM2.5'

    X = cleaned_df[FEATURES]
    y = cleaned_df[TARGET]

    # 5️⃣ Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # 6️⃣ Train model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # 7️⃣ Evaluate
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print(f"✅ Model Trained")
    print(f"📊 MSE: {mse:.2f}")
    print(f"📈 R2 Score: {r2:.2f}")

    # 8️⃣ Save model
    joblib.dump(model, 'models/air_quality_model.pkl')
    print("✅ Model saved to models/air_quality_model.pkl")

if __name__ == "__main__":
    train()
