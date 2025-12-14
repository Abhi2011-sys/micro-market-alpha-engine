import pandas as pd
import numpy as np

def compute_trend_features(df, window=4):
    """
    df: DataFrame with columns [date, trend, keyword]
    window: rolling window size (weeks)
    """

    df = df.sort_values("date").copy()

    # 1️⃣ Trend slope (1st derivative)
    df["trend_slope"] = df["trend"].diff()

    # 2️⃣ Trend acceleration (2nd derivative)
    df["trend_acceleration"] = df["trend_slope"].diff()

    # 3️⃣ Rolling mean & std for stability
    df["rolling_mean"] = df["trend"].rolling(window).mean()
    df["rolling_std"] = df["trend"].rolling(window).std()

    # Stability score (lower variance = higher stability)
    df["stability_score"] = 1 / (df["rolling_std"] + 1)

    # 4️⃣ Breakout detection
    df["breakout_score"] = (
        (df["trend"] - df["rolling_mean"]) /
        (df["rolling_std"] + 1)
    )

    return df


def compute_early_growth_score(df):
    """
    Final Alpha Metric (0–100)
    """

    df = df.copy()

    # Normalize components
    df["slope_norm"] = (df["trend_slope"] - df["trend_slope"].min()) / (
        df["trend_slope"].max() - df["trend_slope"].min()
    )

    df["acc_norm"] = (df["trend_acceleration"] - df["trend_acceleration"].min()) / (
        df["trend_acceleration"].max() - df["trend_acceleration"].min()
    )

    df["breakout_norm"] = (df["breakout_score"] - df["breakout_score"].min()) / (
        df["breakout_score"].max() - df["breakout_score"].min()
    )

    df["stability_norm"] = (df["stability_score"] - df["stability_score"].min()) / (
        df["stability_score"].max() - df["stability_score"].min()
    )

    # Weighted Alpha (you can justify these weights)
    df["EGS"] = (
        0.35 * df["slope_norm"] +
        0.30 * df["acc_norm"] +
        0.20 * df["breakout_norm"] +
        0.15 * df["stability_norm"]
    ) * 100

    return df
