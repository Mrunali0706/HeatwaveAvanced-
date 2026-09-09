import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Heatwave Health Risk & Safety System",
    page_icon="🌡️",
    layout="wide"
)


# ============================================================
# LOCATION DATA
# ============================================================

location_data = {
    "Mumbai": {
        "temperature": 35.0,
        "humidity": 60.0,
        "wind": 2.0,
        "solar": 500.0,
    },
    "Delhi": {
        "temperature": 36.0,
        "humidity": 70.0,
        "wind": 2.0,
        "solar": 600.0,
    },
    "Chennai": {
        "temperature": 34.0,
        "humidity": 75.0,
        "wind": 2.5,
        "solar": 550.0,
    },
    "Bengaluru": {
        "temperature": 30.0,
        "humidity": 65.0,
        "wind": 2.5,
        "solar": 450.0,
    },
}


# ============================================================
# SIDEBAR - ENVIRONMENTAL CONDITIONS
# ============================================================

st.sidebar.header(" Environmental Conditions")

location = st.sidebar.selectbox(
    " Monitoring Location",
    list(location_data.keys())
)

default_values = location_data[location]

temperature = st.sidebar.number_input(
    "Air Temperature (°C)",
    min_value=0.0,
    max_value=60.0,
    value=default_values["temperature"],
    step=1.0
)

humidity = st.sidebar.number_input(
    "Relative Humidity (%)",
    min_value=0.0,
    max_value=100.0,
    value=default_values["humidity"],
    step=1.0
)

wind = st.sidebar.number_input(
    "Wind Speed (m/s)",
    min_value=0.0,
    max_value=30.0,
    value=default_values["wind"],
    step=0.5
)

solar = st.sidebar.number_input(
    "Solar Radiation (W/m²)",
    min_value=0.0,
    max_value=1200.0,
    value=default_values["solar"],
    step=50.0
)


# ============================================================
# HEATWAVE RISK CALCULATION
# ============================================================

def calculate_heat_score(temperature, humidity, wind, solar):
    """
    Calculate a heatwave risk score approximately between 0 and 100.

    Higher temperature and humidity increase risk.
    Higher wind reduces risk.
    Higher solar radiation increases risk.
    """

    # Temperature contribution
    temp_score = np.clip(
        (temperature - 25) / 15 * 45,
        0,
        45
    )

    # Humidity contribution
    humidity_score = np.clip(
        (humidity - 30) / 50 * 25,
        0,
        25
    )

    # Wind contribution
    wind_score = np.clip(
        (5 - wind) / 5 * 10,
        0,
        10
    )

    # Solar radiation contribution
    solar_score = np.clip(
        solar / 1000 * 20,
        0,
        20
    )

    score = (
        temp_score
        + humidity_score
        + wind_score
        + solar_score
    )

    return round(float(np.clip(score, 0, 100)), 1)


# ============================================================
# RISK LEVEL
# ============================================================

def get_risk_level(score):

    if score < 25:
        return "Low"
    elif score < 50:
        return "Moderate"
    elif score < 75:
        return "High"
    else:
        return "Extreme"


def get_risk_message(risk_level):

    messages = {
        "Low": "Low heat-related health risk.",
        "Moderate": "Moderate heat stress. Stay hydrated and limit prolonged exposure.",
        "High": "High risk of heat-related illness. Avoid unnecessary outdoor exposure.",
        "Extreme": "Extreme heat risk. Immediate protective measures are recommended."
    }

    return messages[risk_level]


# ============================================================
# MORTALITY RISK INDEX
# ============================================================

def calculate_mortality_risk(score, risk_level):

    multiplier = {
        "Low": 0.00,
        "Moderate": 0.15,
        "High": 0.30,
        "Extreme": 0.50
    }

    mortality_risk = min(
        100,
        round(
            score * (1.0 + multiplier[risk_level]),
            1
        )
    )

    return mortality_risk


# ============================================================
# CURRENT CONDITIONS
# ============================================================

heat_score = calculate_heat_score(
    temperature,
    humidity,
    wind,
    solar
)

risk_level = get_risk_level(heat_score)

risk_message = get_risk_message(risk_level)
# Emergency heat alert
if risk_level == "Extreme":
    st.error(
        " EXTREME HEAT ALERT: Immediate protective action is required. "
        "Avoid outdoor activity, stay hydrated, and move to a cool location."
    )

elif risk_level == "High":
    st.warning(
        " HIGH HEAT ALERT: Heat-related illness risk is high. "
        "Avoid prolonged outdoor exposure and stay hydrated."
    )

elif risk_level == "Moderate":
    st.info(
        " MODERATE HEAT ALERT: Take precautions, stay hydrated, "
        "and limit strenuous outdoor activity."
    )

else:
    st.success(
        " LOW HEAT RISK: Current conditions are relatively safe. "
        "Continue normal precautions."
    )

mortality_risk = calculate_mortality_risk(
    heat_score,
    risk_level
)


# ============================================================
# HEADER
# ============================================================

st.title(" Heatwave Health Risk & Safety System")

st.subheader("Advanced Heatwave Monitoring Dashboard")

st.write(
    "This system analyzes environmental conditions and provides "
    "a heat-risk level, thermal indicators, safety recommendations, "
    "5-day forecasts, graphs and an interactive monitoring view."
)


# ============================================================
# CURRENT CONDITIONS
# ============================================================

st.divider()

st.subheader(f" Current Conditions - {location}")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        " Temperature",
        f"{temperature:.1f} °C"
    )

with col2:
    st.metric(
        " Humidity",
        f"{humidity:.0f} %"
    )

with col3:
    st.metric(
        " Wind Speed",
        f"{wind:.1f} m/s"
    )

with col4:
    st.metric(
        " Solar Radiation",
        f"{solar:.0f} W/m²"
    )


# ============================================================
# CURRENT HEAT RISK
# ============================================================

st.subheader(" Current Heat Risk")

if risk_level == "Low":
    st.success(f" {risk_level} Risk")
elif risk_level == "Moderate":
    st.warning(f" {risk_level} Risk")
elif risk_level == "High":
    st.error(f" {risk_level} Risk")
else:
    st.error(f" {risk_level} Risk")

st.write(risk_message)

st.metric(
    "Heatwave Risk Score",
    f"{heat_score} / 100"
)


# ============================================================
# MORTALITY RISK INDEX
# ============================================================

st.subheader(" Mortality Risk Index")

st.metric(
    "Estimated Mortality Risk",
    f"{mortality_risk:.1f} / 100"
)


# ============================================================
# SAFETY ADVISORY
# ============================================================

st.subheader(" Recommended Safety Actions")

if risk_level == "Low":

    st.info(
        "Normal precautions. Stay hydrated and monitor heat conditions."
    )

elif risk_level == "Moderate":

    st.warning(
        "Increase water intake, reduce prolonged outdoor activity, "
        "and take regular breaks in shaded or cool areas."
    )

elif risk_level == "High":

    st.warning(
        "Avoid unnecessary outdoor exposure, especially during peak "
        "afternoon hours. Keep vulnerable people hydrated and cool."
    )

else:

    st.error(
        "Extreme heat conditions detected. Avoid outdoor activity, "
        "use cooling facilities, maintain hydration, and check on "
        "elderly people, children and outdoor workers."
    )


# ============================================================
# 5-DAY FORECAST
# ============================================================

st.divider()

st.subheader(" 5-Day Forecast Risk")


forecast_days = [
    "Day 1",
    "Day 2",
    "Day 3",
    "Day 4",
    "Day 5"
]


# ============================================================
# LOCATION-SPECIFIC FORECAST CHANGES
# ============================================================

location_changes = {

    "Mumbai": {
        "temperature": [0.0, 0.8, 1.5, 2.0, 1.2],
        "humidity": [0.0, 2.0, 4.0, 3.0, 1.0],
        "wind": [0.0, -0.2, -0.4, 0.1, -0.1],
        "solar": [0, 60, 120, 100, 70],
    },

    "Delhi": {
        "temperature": [0.0, 1.0, 2.0, 2.5, 2.0],
        "humidity": [0.0, -2.0, -4.0, -3.0, -1.0],
        "wind": [0.0, 0.3, -0.2, -0.4, 0.2],
        "solar": [0, 80, 150, 120, 90],
    },

    "Chennai": {
        "temperature": [0.0, 0.6, 1.2, 1.8, 1.0],
        "humidity": [0.0, 3.0, 5.0, 4.0, 2.0],
        "wind": [0.0, -0.3, -0.5, -0.2, 0.1],
        "solar": [0, 50, 100, 80, 60],
    },

    "Bengaluru": {
        "temperature": [0.0, 0.4, 0.8, 1.2, 0.7],
        "humidity": [0.0, 1.0, 2.0, 1.5, 1.0],
        "wind": [0.0, 0.2, 0.1, -0.2, 0.0],
        "solar": [0, 40, 80, 60, 50],
    }
}


# ============================================================
# CREATE FORECAST DATA
# ============================================================

forecast_data = []

changes = location_changes.get(
    location,
    {
        "temperature": [0.0, 0.5, 1.0, 1.5, 1.0],
        "humidity": [0.0, 2.0, 3.0, 2.0, 1.0],
        "wind": [0.0, -0.2, -0.3, -0.1, 0.0],
        "solar": [0, 50, 100, 80, 60],
    }
)


for i, day in enumerate(forecast_days):

    # Forecast environmental conditions
    forecast_temperature = (
        temperature
        + changes["temperature"][i]
    )

    forecast_humidity = max(
        0,
        min(
            100,
            humidity + changes["humidity"][i]
        )
    )

    forecast_wind = max(
        0.5,
        wind + changes["wind"][i]
    )

    forecast_solar = max(
        0,
        solar + changes["solar"][i]
    )


    # Calculate heat risk for THIS forecast day
    forecast_score = calculate_heat_score(
        forecast_temperature,
        forecast_humidity,
        forecast_wind,
        forecast_solar
    )

    forecast_risk = get_risk_level(
        forecast_score
    )

    forecast_mortality_risk = calculate_mortality_risk(
        forecast_score,
        forecast_risk
    )


    # Add complete forecast row
    forecast_data.append(
        {
            "Day": day,
            "Temperature (°C)": round(
                forecast_temperature,
                1
            ),
            "Humidity (%)": round(
                forecast_humidity,
                1
            ),
            "Wind Speed (m/s)": round(
                forecast_wind,
                1
            ),
            "Solar Radiation (W/m²)": round(
                forecast_solar,
                0
            ),
            "Heatwave Score": forecast_score,
            "Risk Level": forecast_risk,
            "Mortality Risk": forecast_mortality_risk
        }
    )


# ============================================================
# CREATE DATAFRAME
# ============================================================

forecast_df = pd.DataFrame(
    forecast_data
)
st.subheader(" 5-Day Heat Risk Forecast")

st.dataframe(
    forecast_df[
        [
            "Day",
            "Temperature (°C)",
            "Humidity (%)",
            "Wind Speed (m/s)",
            "Heatwave Score",
            "Risk Level",
            "Mortality Risk"
        ]
    ],
    use_container_width=True,
    hide_index=True
)
st.subheader(" Heat Risk Trend")

st.line_chart(
    forecast_df.set_index("Day")["Heatwave Score"]
)
st.subheader(" Mortality Risk Trend")

st.line_chart(
    forecast_df.set_index("Day")["Mortality Risk"]
)

# ============================================================
# FORECAST TABLE
# ============================================================

st.subheader(f"Forecast Data - {location}")

st.dataframe(
    forecast_df,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# FORECAST HEAT RISK GRAPH
# ============================================================

st.subheader(" Forecast Heat Risk")

fig_forecast = px.line(
    forecast_df,
    x="Day",
    y="Heatwave Score",
    markers=True,
    title=f"Forecast Heat Risk - {location}"
)

fig_forecast.update_yaxes(
    range=[0, 100],
    tickmode="array",
    tickvals=[0, 25, 50, 75, 100],
    ticktext=[
        "Low",
        "Moderate",
        "High",
        "Extreme",
        "Extreme"
    ],
    title="Heat Risk"
)

fig_forecast.update_xaxes(
    title="Forecast Day"
)

st.plotly_chart(
    fig_forecast,
    width="stretch"
)


# ============================================================
# 5-DAY TEMPERATURE FORECAST
# ============================================================

st.subheader(" 5-Day Temperature Forecast")

fig_temperature = px.line(
    forecast_df,
    x="Day",
    y="Temperature (°C)",
    markers=True,
    title=f"Temperature Forecast - {location}"
)

fig_temperature.update_xaxes(
    title="Forecast Day"
)

fig_temperature.update_yaxes(
    title="Temperature (°C)"
)

st.plotly_chart(
    fig_temperature,
    width="stretch"
)


# ============================================================
# 5-DAY HUMIDITY FORECAST
# ============================================================

st.subheader(" 5-Day Humidity Forecast")

fig_humidity = px.line(
    forecast_df,
    x="Day",
    y="Humidity (%)",
    markers=True,
    title=f"Humidity Forecast - {location}"
)

fig_humidity.update_xaxes(
    title="Forecast Day"
)

fig_humidity.update_yaxes(
    title="Humidity (%)"
)

st.plotly_chart(
    fig_humidity,
    width="stretch"
)


# ============================================================
# 5-DAY MORTALITY RISK FORECAST
# ============================================================

st.subheader(" 5-Day Mortality Risk Forecast")

fig_mortality = px.line(
    forecast_df,
    x="Day",
    y="Mortality Risk",
    markers=True,
    title=f"Mortality Risk Forecast - {location}"
)

fig_mortality.update_xaxes(
    title="Forecast Day"
)

fig_mortality.update_yaxes(
    range=[0, 100],
    title="Mortality Risk"
)

st.plotly_chart(
    fig_mortality,
    width="stretch"
)

# ============================================================
# RISK SUMMARY
# ============================================================

st.subheader(" Risk Summary")

highest_score = forecast_df["Heatwave Score"].max()
highest_day = forecast_df.loc[
    forecast_df["Heatwave Score"].idxmax(), "Day"
]

highest_mortality = forecast_df["Mortality Risk"].max()

st.write(
    f"• Highest predicted heatwave score: {highest_score} on {highest_day}"
)

st.write(
    f"• Highest predicted mortality risk: {highest_mortality:.1f}%"
)

st.write(
    "• Overall forecast indicates elevated heat-related risk. "
    "Preventive measures and monitoring are recommended."
)

# ============================================================
# EARLY WARNING ALERT
# ============================================================

st.subheader(" Early Warning Alert")

max_score = forecast_df["Heatwave Score"].max()
alert_day = forecast_df.loc[
    forecast_df["Heatwave Score"].idxmax(), "Day"
]

if max_score >= 75:
    st.error(
        f" EXTREME HEAT WARNING: Forecast heatwave score may reach "
        f"{max_score:.1f} on {alert_day}. Immediate preventive action is recommended."
    )
elif max_score >= 50:
    st.warning(
        f" HEAT WARNING: Elevated heat conditions are expected, "
        f"with the highest score of {max_score:.1f} on {alert_day}."
    )
else:
    st.info(
        f"ℹ️ Heat conditions are currently within a lower-risk range. "
        f"Continue monitoring the forecast."
    )


# ============================================================
# SAFETY RECOMMENDATIONS
# ============================================================

st.subheader(" Safety Recommendations")

risk = str(forecast_df.iloc[0]["Risk Level"]).lower()
temperature = forecast_df.iloc[0]["Temperature (°C)"]
humidity = forecast_df.iloc[0]["Humidity (%)"]

if risk == "high" or temperature >= 35:
    st.warning(
        " HIGH HEAT RISK: Heat-related illness risk is elevated. "
        "Avoid prolonged outdoor exposure and stay hydrated."
    )

    st.write("### Recommended Actions")
    st.write("• Drink water regularly, even if you do not feel thirsty.")
    st.write("• Avoid strenuous outdoor activities during peak afternoon hours.")
    st.write("• Stay in shaded, cool, or air-conditioned areas whenever possible.")
    st.write("• Check on elderly people, children, and other vulnerable individuals.")
    st.write("• Use lightweight and breathable clothing.")
else:
    st.info(
        "Heat conditions are currently manageable. Continue monitoring "
        "temperature and humidity."
    )


# ============================================================
# WARD / ZONE LEVEL HEAT RISK
# ============================================================

st.divider()

st.subheader(" Ward / Zone-Level Heat Risk")

# Demo ward-level data for localized monitoring
# These values can later be replaced with real ward sensor/API data
ward_data = pd.DataFrame({
    "Zone": [
        "South Mumbai",
        "Central Mumbai",
        "Western Suburbs",
        "Eastern Suburbs",
        "Harbour Area"
    ],
    "Heatwave Score": [74.9, 72.5, 69.8, 67.4, 71.2],
    "Temperature (°C)": [37.0, 36.8, 36.5, 36.2, 36.7],
    "Humidity (%)": [63, 64, 62, 61, 65]
})

# Automatically assign risk level
def get_zone_risk(score):
    if score >= 75:
        return "Extreme"
    elif score >= 60:
        return "High"
    elif score >= 40:
        return "Moderate"
    else:
        return "Low"

ward_data["Risk Level"] = ward_data["Heatwave Score"].apply(get_zone_risk)

st.dataframe(
    ward_data,
    width="stretch",
    hide_index=True
)

# Highest-risk zone
highest_zone = ward_data.loc[
    ward_data["Heatwave Score"].idxmax(), "Zone"
]

highest_zone_score = ward_data["Heatwave Score"].max()

st.warning(
    f" Highest-risk zone: {highest_zone} "
    f"(Heatwave Score: {highest_zone_score})"
)

# ============================================================
# HEATWAVE ALERT SYSTEM
# ============================================================

st.divider()

st.subheader(" Heatwave Alert System")

if highest_zone_score >= 75:
    alert_level = "EXTREME"
elif highest_zone_score >= 60:
    alert_level = "HIGH"
elif highest_zone_score >= 40:
    alert_level = "MODERATE"
else:
    alert_level = "LOW"

if alert_level == "EXTREME":
    st.error(
        f" EXTREME HEAT ALERT\n\n"
        f"{highest_zone} requires immediate attention. "
        f"Activate emergency heat-response measures."
    )

elif alert_level == "HIGH":
    st.warning(
        f" HIGH HEAT ALERT\n\n"
        f"{highest_zone} is currently at high heat risk. "
        f"Preventive measures should be activated."
    )

else:
    st.info(
        f"ℹ️ Current alert level: {alert_level}"
    )

st.write("**Recommended actions:**")

st.write("• Issue heat-health warning to the public")
st.write("• Activate cooling centres in high-risk areas")
st.write("• Monitor vulnerable populations")
st.write("• Increase hospital and emergency-service preparedness")
st.write("• Continue real-time heat-risk monitoring")


# ============================================================
# LOCALIZED MONITORING MAP
# ============================================================

st.divider()

st.subheader(" Localized Heat Risk Monitoring")

# Approximate city coordinates for dashboard demonstration
map_data = pd.DataFrame(
    {
        "Location": [
            "Mumbai",
            "Delhi",
            "Chennai",
            "Bengaluru"
        ],
        "Latitude": [
            19.0760,
            28.6139,
            13.0827,
            12.9716
        ],
        "Longitude": [
            72.8777,
            77.2090,
            80.2707,
            77.5946
        ],
        "Heat Risk Score": [
            calculate_heat_score(
                location_data["Mumbai"]["temperature"],
                location_data["Mumbai"]["humidity"],
                location_data["Mumbai"]["wind"],
                location_data["Mumbai"]["solar"]
            ),
            calculate_heat_score(
                location_data["Delhi"]["temperature"],
                location_data["Delhi"]["humidity"],
                location_data["Delhi"]["wind"],
                location_data["Delhi"]["solar"]
            ),
            calculate_heat_score(
                location_data["Chennai"]["temperature"],
                location_data["Chennai"]["humidity"],
                location_data["Chennai"]["wind"],
                location_data["Chennai"]["solar"]
            ),
            calculate_heat_score(
                location_data["Bengaluru"]["temperature"],
                location_data["Bengaluru"]["humidity"],
                location_data["Bengaluru"]["wind"],
                location_data["Bengaluru"]["solar"]
            )
        ]
    }
)

map_data["Risk Level"] = map_data["Heat Risk Score"].apply(
    get_risk_level
)

fig_map = px.scatter_map(
    map_data,
    lat="Latitude",
    lon="Longitude",
    hover_name="Location",
    hover_data=[
        "Heat Risk Score",
        "Risk Level"
    ],
    color="Risk Level",
    size="Heat Risk Score",
    zoom=3.5,
    height=500,
    title="City-Level Heat Risk Monitoring"
)

fig_map.update_layout(
    map_style="open-street-map",
    margin={
        "r": 0,
        "t": 50,
        "l": 0,
        "b": 0
    }
)

st.plotly_chart(
    fig_map,
    width="stretch"
)


# ============================================================
# ACTIONABLE HEAT ACTION PLAN
# ============================================================

st.subheader(" Recommended Heat Action Plan")

if risk_level in ["High", "Extreme"]:

    actions = [
        "Open or activate cooling centres.",
        "Issue localized heat-health warnings.",
        "Advise outdoor workers to shift working hours.",
        "Increase monitoring of elderly people and other vulnerable groups.",
        "Prepare hospitals and emergency services for increased heat-related cases.",
        "Ensure adequate drinking water availability."
    ]

else:

    actions = [
        "Continue monitoring environmental conditions.",
        "Maintain public hydration awareness.",
        "Monitor vulnerable populations.",
        "Prepare heat-health response measures if risk increases."
    ]

for action in actions:
    st.write(f"• {action}")

    # ============================================================
# EMERGENCY HEAT ALERT
# ============================================================

st.divider()

st.subheader(" Emergency Heat Alert")

if highest_score >= 75:
    st.error(
        f"EXTREME HEAT ALERT: {location} is expected to experience "
        f"very high heat risk. Immediate preventive action is recommended."
    )
elif highest_score >= 50:
    st.warning(
        f"HIGH HEAT ALERT: {location} is expected to experience "
        f"high heat risk. Preventive measures are recommended."
    )
else:
    st.success(
        f"Heat conditions in {location} are currently within a lower-risk range."
    )



# ============================================================
# SYSTEM STATUS
# ============================================================

st.divider()

st.caption(
    "Heatwave Health Risk & Safety System | "
    "Localized environmental risk monitoring and early warning dashboard"
)

# ============================================================
# VULNERABLE POPULATION MONITORING
# ============================================================

st.divider()

st.subheader(" Vulnerable Population Monitoring")

vulnerable_data = pd.DataFrame({
    "Group": [
        "Elderly people",
        "Children",
        "Outdoor workers",
        "People with chronic illness",
        "Homeless population"
    ],
    "Priority": [
        "High",
        "High",
        "High",
        "High",
        "Moderate"
    ],
    "Recommended Action": [
        "Increase monitoring and provide cooling support.",
        "Avoid prolonged outdoor exposure and ensure hydration.",
        "Shift working hours away from peak afternoon heat.",
        "Ensure medication, hydration and cooling support.",
        "Provide access to shade, water and cooling centres."
    ]
})

st.dataframe(
    vulnerable_data,
    width="stretch",
    hide_index=True
)