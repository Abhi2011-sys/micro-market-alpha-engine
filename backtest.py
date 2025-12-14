import pandas as pd
import numpy as np

def backtest_early_vs_late(df, egs_threshold=70):
    df = df.copy().reset_index(drop=True)

    # Ensure date is datetime
    df["date"] = pd.to_datetime(df["date"])

    # Early signal: first time EGS crosses threshold
    early_idx = df[df["EGS"] >= egs_threshold].index.min()

    # Late signal: peak trend
    late_idx = df["trend"].idxmax()

    results = {}

    if not pd.isna(early_idx):
        results["early_date"] = df.loc[early_idx, "date"]
        results["early_trend"] = df.loc[early_idx, "trend"]
    else:
        results["early_date"] = None
        results["early_trend"] = None

    results["late_date"] = df.loc[late_idx, "date"]
    results["late_trend"] = df.loc[late_idx, "trend"]

    if results["early_date"] is not None:
        results["lead_time_weeks"] = (
            (results["late_date"] - results["early_date"]).days // 7
        )
    else:
        results["lead_time_weeks"] = 0

    # Simple ROI proxy
    results["early_roi"] = (
        results["late_trend"] - results["early_trend"]
        if results["early_trend"] is not None else 0
    )
    results["late_roi"] = results["late_trend"]

    return results
