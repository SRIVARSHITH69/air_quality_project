# src/stations.py

import requests
import pandas as pd
import random

def get_station_data():
    try:
        # ✅ LIVE OpenAQ fetch
        api_key = "0df37a579aed758759705775df8879de9cad966339c4a4385a2e0e5992b53ac0"
        loc_url = "https://api.openaq.org/v3/locations"
        loc_params = {"country": "IN", "limit": 1000}
        headers = {"x-api-key": api_key}

        loc_resp = requests.get(loc_url, params=loc_params, headers=headers, timeout=10)
        loc_resp.raise_for_status()
        loc_data = loc_resp.json()

        cities, lats, lons, pm25_list, pm10_list, aqi_list = [], [], [], [], [], []

        for loc in loc_data.get("results", []):
            loc_id = loc["id"]
            city = loc.get("city") or loc.get("name") or loc.get("location") or "Unknown"
            coordinates = loc.get("coordinates", {})
            lat = coordinates.get("latitude")
            lon = coordinates.get("longitude")
            if not lat or not lon:
                continue

            available_params = [p["parameter"] for p in loc.get("parameters", [])]
            if not any(p in available_params for p in ["pm25", "pm10"]):
                continue

            meas_url = "https://api.openaq.org/v3/measurements"
            meas_params = {"location_id": loc_id, "parameter": ["pm25", "pm10"], "limit": 2}
            meas_resp = requests.get(meas_url, params=meas_params, headers=headers, timeout=10)

            if meas_resp.status_code == 404:
                continue

            meas_resp.raise_for_status()
            meas_data = meas_resp.json()

            pm25, pm10 = None, None
            for m in meas_data.get("results", []):
                param, value = m["parameter"], m["value"]
                if param == "pm25":
                    pm25 = value
                elif param == "pm10":
                    pm10 = value

            if pm25 is None and pm10 is None:
                continue

            pm25 = pm25 or 0
            pm10 = pm10 or 0
            aqi = max(pm25 * 2, pm10 * 1.5)

            cities.append(city)
            lats.append(lat)
            lons.append(lon)
            pm25_list.append(pm25)
            pm10_list.append(pm10)
            aqi_list.append(int(aqi))

        if not cities:
            raise Exception("No live stations found")

        df = pd.DataFrame({
            "City": cities,
            "Latitude": lats,
            "Longitude": lons,
            "PM2.5": pm25_list,
            "PM10": pm10_list,
            "AQI": aqi_list
        })
        return df

    except Exception as e:
        print(f"[INFO] Live fetch failed, using fallback. Reason: {e}")

        # 🟢 50 major cities + 10 Telangana fallback
        fallback = [
            ("Delhi", 28.6139, 77.2090), ("Mumbai", 19.0760, 72.8777),
            ("Kolkata", 22.5726, 88.3639), ("Chennai", 13.0827, 80.2707),
            ("Bengaluru", 12.9716, 77.5946), ("Hyderabad", 17.3850, 78.4867),
            ("Ahmedabad", 23.0225, 72.5714), ("Pune", 18.5204, 73.8567),
            ("Jaipur", 26.9124, 75.7873), ("Lucknow", 26.8467, 80.9462),
            ("Patna", 25.5941, 85.1376), ("Bhopal", 23.2599, 77.4126),
            ("Kanpur", 26.4499, 80.3319), ("Nagpur", 21.1458, 79.0882),
            ("Indore", 22.7196, 75.8577), ("Surat", 21.1702, 72.8311),
            ("Agra", 27.1767, 78.0081), ("Varanasi", 25.3176, 82.9739),
            ("Amritsar", 31.6340, 74.8723), ("Meerut", 28.9845, 77.7064),
            ("Rajkot", 22.3039, 70.8022), ("Srinagar", 34.0837, 74.7973),
            ("Ranchi", 23.3441, 85.3096), ("Coimbatore", 11.0168, 76.9558),
            ("Vijayawada", 16.5062, 80.6480), ("Madurai", 9.9252, 78.1198),
            ("Jodhpur", 26.2389, 73.0243), ("Raipur", 21.2514, 81.6296),
            ("Guwahati", 26.1445, 91.7362), ("Chandigarh", 30.7333, 76.7794),
            ("Mysuru", 12.2958, 76.6394), ("Dehradun", 30.3165, 78.0322),
            ("Noida", 28.5355, 77.3910), ("Gurugram", 28.4595, 77.0266),
            ("Faridabad", 28.4089, 77.3178), ("Ghaziabad", 28.6692, 77.4538),
            ("Ludhiana", 30.9000, 75.8573), ("Nashik", 19.9975, 73.7898),
            ("Thane", 19.2183, 72.9781), ("Aurangabad", 19.8762, 75.3433),
            ("Jabalpur", 23.1815, 79.9864), ("Gwalior", 26.2183, 78.1828),
            ("Vasai", 19.3919, 72.8397), ("Vellore", 12.9165, 79.1325),
            ("Thrissur", 10.5276, 76.2144), ("Warangal", 17.9784, 79.5941),
            ("Salem", 11.6643, 78.1460), ("Aligarh", 27.8974, 78.0880),
            ("Bareilly", 28.3670, 79.4304),
            # 10 Telangana fallback
            ("Karimnagar", 18.4386, 79.1288), ("Nizamabad", 18.6725, 78.0941),
            ("Khammam", 17.2473, 80.1514), ("Mahbubnagar", 16.7482, 77.9850),
            ("Adilabad", 19.6667, 78.5333), ("Siddipet", 18.1010, 78.8485),
            ("Nalgonda", 17.0544, 79.2671), ("Miryalaguda", 16.8722, 79.5625),
            ("Suryapet", 17.1400, 79.6190), ("Mancherial", 18.8743, 79.4444)
        ]

        data = []
        for city, lat, lon in fallback:
            data.append({
                "City": city,
                "Latitude": lat,
                "Longitude": lon,
                "PM2.5": random.randint(40, 250),
                "PM10": random.randint(50, 300),
                "AQI": random.randint(50, 400)
            })

        return pd.DataFrame(data)
