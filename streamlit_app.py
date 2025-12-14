import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import sys
import os

# 🔑 FIX: always resolve project root
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(PROJECT_ROOT)

from src.features import compute_trend_features, compute_early_growth_score
from src.city_alpha import generate_city_alpha

st.set_page_config(page_title="Micro-Market Alpha Engine", layout="wide")

st.title("📈 Micro-Market Alpha Engine")
st.subheader("Early Demand Detection & City-Level Intelligence")

# Load data
df = pd.read_csv(os.path.join(PROJECT_ROOT, "data/processed/national_trends.csv"))


keyword = st.selectbox(
    "Select Product Keyword",
    sorted(df["keyword"].unique())
)

kw_df = df[df["keyword"] == keyword]

kw_df = compute_trend_features(kw_df)
kw_df = compute_early_growth_score(kw_df)

city_df = generate_city_alpha(kw_df)

# City selector
city = st.selectbox(
    "Select City",
    sorted(city_df["city"].unique())
)

city_data = city_df[city_df["city"] == city]

latest_score = city_data["city_EGS"].iloc[-1]

# Decision logic
if latest_score >= 70:
    decision = "🟢 ACT"
elif latest_score >= 40:
    decision = "🟡 WAIT"
else:
    decision = "🔴 IGNORE"

# KPI cards
col1, col2, col3 = st.columns(3)

col1.metric("City", city)
col2.metric("Early Growth Score", f"{latest_score:.1f}")
col3.metric("Recommendation", decision)

# Plot
fig, ax = plt.subplots(figsize=(10,4))
ax.plot(city_data["date"], city_data["city_EGS"], label="City EGS")
ax.axhline(70, linestyle="--", color="green", label="ACT Threshold")
ax.axhline(40, linestyle="--", color="orange", label="WAIT Threshold")
ax.legend()
ax.set_title(f"City-Level Alpha Trend – {keyword.title()} ({city})")

st.pyplot(fig)

st.markdown("---")
st.markdown(
"""
### 🧠 How to Interpret
- **ACT** → Launch ads / stock inventory / partnerships
- **WAIT** → Monitor closely
- **IGNORE** → No near-term opportunity

This system detects **emerging demand weeks before peak interest**.
"""
)
