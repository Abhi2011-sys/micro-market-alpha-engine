import pandas as pd
from src.city_weights import get_city_weights

def generate_city_alpha(df):
    """
    Expands national EGS into city-level signals
    """
    cities = get_city_weights()
    all_city_frames = []

    for city, weight in cities.items():
        city_df = df.copy()
        city_df["city"] = city

        # City adjusted alpha
        city_df["city_EGS"] = city_df["EGS"] * weight

        # Simulate diffusion lag (weeks)
        lag = int((1 - weight) * 6)
        city_df["city_EGS"] = city_df["city_EGS"].shift(lag)

        all_city_frames.append(city_df)

    return pd.concat(all_city_frames, ignore_index=True)
