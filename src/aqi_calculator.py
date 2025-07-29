# src/aqi_calculator.py

def calculate_sub_index(pollutant, concentration):
    """
    Calculate sub-index for a given pollutant and its concentration.
    Using CPCB breakpoints (example for PM2.5).
    """

    breakpoints = {
        "PM2.5": [
            (0, 30, 0, 50),
            (31, 60, 51, 100),
            (61, 90, 101, 200),
            (91, 120, 201, 300),
            (121, 250, 301, 400),
            (251, 380, 401, 500),
        ],
        "PM10": [
            (0, 50, 0, 50),
            (51, 100, 51, 100),
            (101, 250, 101, 200),
            (251, 350, 201, 300),
            (351, 430, 301, 400),
            (431, 500, 401, 500),
        ],
        # Add more pollutants here
    }

    if pollutant not in breakpoints:
        raise ValueError(f"No breakpoints defined for {pollutant}")

    for (C_low, C_high, I_low, I_high) in breakpoints[pollutant]:
        if C_low <= concentration <= C_high:
            index = ((I_high - I_low) / (C_high - C_low)) * (concentration - C_low) + I_low
            return round(index)

    return None  # Out of range

def calculate_aqi(concentrations: dict):
    """
    Takes a dict like:
    {
        "PM2.5": 85,
        "PM10": 150,
        ...
    }
    Returns the highest sub-index (the AQI).
    """
    sub_indices = []
    for pollutant, value in concentrations.items():
        sub_index = calculate_sub_index(pollutant, value)
        if sub_index is not None:
            sub_indices.append(sub_index)
    if not sub_indices:
        return None
    return max(sub_indices)

if __name__ == "__main__":
    # Example usage
    inputs = {
        "PM2.5": 85,
        "PM10": 150
    }
    aqi = calculate_aqi(inputs)
    print(f"✅ Calculated AQI: {aqi}")
