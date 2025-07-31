# 🌍 Air Quality Prediction & Monitoring Dashboard

---

📌 Project Objective

This project aims to develop a robust **Air Quality Monitoring System** that can:

- ✅ Predict **PM2.5** concentration based on key pollutant levels (Regression task).
- ✅ Calculate the **Air Quality Index (AQI)** dynamically.
- ✅ Visualize air quality stations across India on an **interactive map** similar to [CPCB AQI India](https://airquality.cpcb.gov.in/AQI_India/).

The goal is to empower citizens, researchers, and authorities with real-time, interpretable air quality data.

---

🧠 Models Built

**Regression Model**

- **Goal:** Predict PM2.5 levels using inputs like CO, NO2, SO2, NH3, OZONE, PM10.
- **Algorithm:** Random Forest Regressor with hyperparameter tuning.
- **Performance (example):**
  - RMSE: 18.45
  - MAE: 12.32
  - R² Score: 0.87

---

🗂️ Dataset Description

The dataset combines **CPCB**, **OpenAQ**, and fallback mock station data for Indian cities.  
Features include:

- Pollutants: **CO**, **NO2**, **SO2**, **NH3**, **OZONE**, **PM10**
- Target: **PM2.5**
- Geolocation: **Latitude**, **Longitude**, **City**
- Timestamps: **last_update**

---

📊 Methodology

**Data Preprocessing**

- Null value handling
- Pivot table to get wide format
- Feature engineering & standardization

**Exploratory Data Analysis (EDA)**

- Correlation heatmaps
- Distributions of pollutant levels
- Time trends of PM2.5

**Model Training**

- Train-Test split (80-20)
- Random Forest with `GridSearchCV` or `RandomizedSearchCV`
- Evaluation using RMSE, MAE, R²

---

🚀 Live Deployment

The full dashboard is built with **Streamlit** and can be deployed on **Render** or **Streamlit Cloud**.

Features:
- 📈 Predict PM2.5 for custom inputs
- 🎨 Color-coded AQI output block
- 🗺️ Interactive Folium map with **marker clustering**, **search bar**, **legend**

---

🛠️ Tech Stack

- **Python**
- **Pandas, NumPy**
- **Scikit-learn**
- **Streamlit**
- **Folium**, **Streamlit-Folium**
- **Matplotlib**, **Seaborn**
- **Render** (for deployment)

---

📁 Project Structure

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
