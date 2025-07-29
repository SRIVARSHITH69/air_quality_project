<<<<<<< HEAD
# Air Quality Prediction System

This project predicts AQI for Indian cities using machine learning and visualizes it on an interactive dashboard similar to [CPCB AQI India](https://airquality.cpcb.gov.in/AQI_India/).

## 📂 Project Structure

- **data/**: Raw, processed, and external datasets
- **notebooks/**: Jupyter notebooks for EDA, modeling, evaluation
- **src/**: Python modules for data prep, model training, AQI calculation, dashboard app
- **models/**: Trained ML models
- **static/** and **templates/**: For web app styling (if using Flask)
- **run.py**: Entrypoint to run the app

## 🚀 How to Run

```bash
pip install -r requirements.txt

python src/train_model.py
python run.py



---


Open `air_quality_project\src\data_preprocessing.py` and paste:

```python
import pandas as pd

def load_data(filepath: str) -> pd.DataFrame:
    return pd.read_csv(filepath)

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df['last_update'] = pd.to_datetime(df['last_update'], dayfirst=True, errors='coerce')
    df = df.dropna(subset=['last_update'])
    pivot_df = df.pivot_table(
        index=['country', 'state', 'city', 'station', 'latitude', 'longitude', 'last_update'],
        columns='pollutant_id',
        values='pollutant_avg'
    ).reset_index()
    pivot_df = pivot_df.dropna()
    return pivot_df

def save_clean_data(df: pd.DataFrame, output_path: str):
    df.to_csv(output_path, index=False)


# 🌍 Air Quality Prediction Dashboard

**A Streamlit web app to predict PM2.5 levels, calculate AQI, and visualize real-time air quality across India.**

---

## 🚀 Features

- **📈 Predict PM2.5** based on user input for major pollutants.
- **🎨 Dynamic AQI calculation** with color-coded category display.
- **🗺️ Interactive map** with clustered air quality stations using Folium.
- **📍 Real-time & fallback data** for Indian cities.
- **🔍 Search & AQI legend** for easy exploration.

---

## 📂 Project Structure

```plaintext
air_quality_project/
├── data/
│   ├── raw/
│   ├── processed/
│   ├── external/
├── notebooks/
│   ├── 01_eda.ipynb
│   ├── 02_modeling.ipynb
│   ├── 03_evaluation.ipynb
├── src/
│   ├── app.py
│   ├── predict.py
│   ├── aqi_calculator.py
│   ├── stations.py
├── models/
│   ├── air_quality_model.pkl
├── requirements.txt
├── README.md
├── .gitignore
└── run.py
=======
# air_quality_project
AIR QUALITY PREDICTION
>>>>>>> fafa0bd4b1c6474f1840ad24462b21f048cc885b
