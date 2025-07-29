# src/app.py

# src/app.py

import folium
import streamlit as st
from predict import load_model, make_prediction
from aqi_calculator import calculate_aqi
from stations import get_station_data
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium



def create_aqi_map(df):
    # 🌍 Create base map
    m = folium.Map(
        location=[22.9734, 78.6569],  # Center of India
        zoom_start=5,
        tiles="CartoDB positron"
    )

    # Cluster for markers
    marker_cluster = MarkerCluster().add_to(m)

    # Color scale logic
    def get_color(aqi):
        if aqi <= 50:
            return "green"
        elif aqi <= 100:
            return "yellow"
        elif aqi <= 200:
            return "orange"
        elif aqi <= 300:
            return "red"
        elif aqi <= 400:
            return "purple"
        else:
            return "maroon"

    # Add all city markers
    for _, row in df.iterrows():
        popup = folium.Popup(
            html=f"""
            <div style='font-size: 14px;'>
                <b>City:</b> {row['City']}<br>
                <b>PM2.5:</b> {row['PM2.5']} µg/m³<br>
                <b>PM10:</b> {row['PM10']} µg/m³<br>
                <b>AQI:</b> {row['AQI']}
            </div>
            """,
            max_width=250
        )
        folium.CircleMarker(
            location=[row["Latitude"], row["Longitude"]],
            radius=8,
            popup=popup,
            color=get_color(row["AQI"]),
            fill=True,
            fill_color=get_color(row["AQI"]),
            fill_opacity=0.8
        ).add_to(marker_cluster)

    # ✅ Smaller, shifted AQI Legend — no search bar
    legend_html = """
     <div style="
         position: fixed;
         top: 100px;
         right: 20px;
         width: 180px;
         height: auto;
         border: 2px solid #ccc;
         z-index: 9999;
         font-size: 12px;
         background: black;
         color: white;
         padding: 10px;
         line-height: 1.4;
         border-radius: 8px;
     ">
         <b>AQI Legend</b><br>
         <i style="background:green; width:10px; height:10px; display:inline-block;"></i> Good (0–50)<br>
         <i style="background:yellow; width:10px; height:10px; display:inline-block;"></i> Satisfactory (51–100)<br>
         <i style="background:orange; width:10px; height:10px; display:inline-block;"></i> Moderate (101–200)<br>
         <i style="background:red; width:10px; height:10px; display:inline-block;"></i> Poor (201–300)<br>
         <i style="background:purple; width:10px; height:10px; display:inline-block;"></i> Very Poor (301–400)<br>
         <i style="background:maroon; width:10px; height:10px; display:inline-block;"></i> Severe (400+)
     </div>
    """
    m.get_root().html.add_child(folium.Element(legend_html))

    return m


def main():
    st.set_page_config(page_title="Air Quality Prediction Dashboard", layout="wide")

    st.title("🌍 Air Quality Prediction Dashboard")
    st.markdown("Predict PM2.5 concentration and calculate AQI based on your inputs.")

    # -------------------------------
    # 🔬 Prediction Section
    # -------------------------------
    st.subheader("🧪 Enter Pollutant Levels")

    col1, col2, col3 = st.columns(3)
    with col1:
        co = st.number_input("CO (mg/m3)", value=0.5)
        nh3 = st.number_input("NH3 (µg/m3)", value=10.0)
    with col2:
        no2 = st.number_input("NO2 (µg/m3)", value=30.0)
        ozone = st.number_input("OZONE (µg/m3)", value=40.0)
    with col3:
        pm10 = st.number_input("PM10 (µg/m3)", value=80.0)
        so2 = st.number_input("SO2 (µg/m3)", value=5.0)

    input_data = {
        "CO": co,
        "NH3": nh3,
        "NO2": no2,
        "OZONE": ozone,
        "PM10": pm10,
        "SO2": so2
    }

    # ✅ Load both model + features
    model, features = load_model()

    if st.button("🌟 Predict Now"):
        # ✅ Correct usage with 3 args
        predicted_pm25 = make_prediction(model, features, input_data)

        concentrations = {
            "PM2.5": predicted_pm25,
            "PM10": pm10
        }
        aqi = calculate_aqi(concentrations)

        if aqi <= 50:
            category = "Good"
            color = "#009865"
        elif aqi <= 100:
            category = "Satisfactory"
            color = "#A3C853"
        elif aqi <= 200:
            category = "Moderate"
            color = "#FFD834"
        elif aqi <= 300:
            category = "Poor"
            color = "#FF9834"
        elif aqi <= 400:
            category = "Very Poor"
            color = "#D64E33"
        else:
            category = "Severe"
            color = "#7E0023"

        st.markdown(
            f"""
            <div style="padding:30px; background-color:{color}; border-radius:10px; text-align:center;">
                <h2 style="color:white;">Predicted PM2.5: {predicted_pm25:.2f} µg/m3</h2>
                <h3 style="color:white;">AQI: {aqi} — {category}</h3>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("---")

    # -------------------------------
    # 📍 Stations Overview
    # -------------------------------
    st.subheader("📍 Current Stations Overview")
    df = get_station_data()
    st.dataframe(df, use_container_width=True)

    # -------------------------------
    # 🗺️ AQI Map — Clustered with Legend
    # -------------------------------
    st.subheader("🗺️ Air Quality Monitoring Stations")

    aqi_map = create_aqi_map(df)
    st_folium(aqi_map, width=1200, height=600)

    # Disclaimer below the map
    st.markdown("""
    <div style='font-size: 15px; color: gray; padding-top: 10px;'>
    ⚠️ This is our model and it can make mistakes. Please double-check or visit 
    <a href='https://airquality.cpcb.gov.in/AQI_India' target='_blank' style='color: lightblue;'>this official CPCB website</a> for accurate data.
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
