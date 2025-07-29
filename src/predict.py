# src/predict.py

import pandas as pd
import joblib

def load_model(model_path='models/air_quality_model.pkl'):
    model = joblib.load(model_path)
    return model

def make_prediction(model, input_data: dict):
    """
    input_data: dict with keys: CO, NH3, NO2, OZONE, PM10, SO2
    Example:
      {
        "CO": 0.5,
        "NH3": 10,
        "NO2": 30,
        "OZONE": 40,
        "PM10": 80,
        "SO2": 5
      }
    """
    df = pd.DataFrame([input_data])
    prediction = model.predict(df)[0]
    return prediction

if __name__ == "__main__":
    # Example usage
    model = load_model()

    sample_input = {
        "CO": 0.5,
        "NH3": 10,
        "NO2": 30,
        "OZONE": 40,
        "PM10": 80,
        "SO2": 5
    }

    predicted_pm25 = make_prediction(model, sample_input)
    print(f"✅ Predicted PM2.5: {predicted_pm25:.2f}")
