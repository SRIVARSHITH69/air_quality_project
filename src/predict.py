# src/predict.py
import pandas as pd
import joblib

def load_model(model_path='models/air_quality_model.pkl'):
    bundle = joblib.load(model_path)
    model = bundle["model"]
    features = bundle["features"]
    return model, features

def make_prediction(model, features, input_data):
    df = pd.DataFrame([input_data])
    df = df[features]  # Reorder columns
    return model.predict(df)[0]

if __name__ == "__main__":
    model, features = load_model()
    sample_input = {
        "CO": 0.5,
        "NH3": 10,
        "NO2": 30,
        "OZONE": 40,
        "PM10": 80,
        "SO2": 5
    }
    print("✅ Predicted PM2.5:", make_prediction(model, features, sample_input))
