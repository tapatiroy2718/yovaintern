import os
import pandas as pd
import numpy as np

# ============================================================
# WEEK 1: DATA ACQUISITION, CLEANING & PREPROCESSING
# Dataset: RBI Weekly Monetary & Banking Indicators
# Author: Tapati Roy
# ============================================================

RAW_PATH = "tapatir630_17866381335214086.csv"
CLEANED_PATH = "RBI_weekly_dataset_cleaned.csv"

# ------------------------------------------------------------
# 1. DATA ACQUISITION / LOADING
# ------------------------------------------------------------
if not os.path.exists(RAW_PATH):
    raise FileNotFoundError(
        f"Raw dataset not found: {RAW_PATH}. "
        "Place the CSV in the same folder as this script."
    )

df = pd.read_csv(RAW_PATH)
df_raw = df.copy()

print("=" * 70)
print("INITIAL DATASET EXPLORATION")
print("=" * 70)
print("Shape:", df.shape)
print("Columns:", len(df.columns))
print("\\nFirst five rows:")
print(df.head())
print("\\nData types:")
print(df.dtypes)
print("\\nDataset information:")
df.info()

# ------------------------------------------------------------
# 2. INITIAL DATA QUALITY CHECK
# ------------------------------------------------------------
print("\\n" + "=" * 70)
print("DATA QUALITY CHECK")
print("=" * 70)

missing_before = df.isna().sum()
print("\\nMissing values by column:")
print(missing_before[missing_before > 0])

print("\\nTotal missing cells:", int(df.isna().sum().sum()))
print("Duplicate rows:", int(df.duplicated().sum()))

# ------------------------------------------------------------
# 3. STANDARDIZE COLUMN NAMES AND TEXT
# ------------------------------------------------------------
df.columns = df.columns.str.strip().str.replace(r"\\s+", " ", regex=True)

for col in df.select_dtypes(include="object").columns:
    df[col] = df[col].astype("string").str.strip()

# ------------------------------------------------------------
# 4. REMOVE EXACT DUPLICATES
# ------------------------------------------------------------
duplicate_count = int(df.duplicated().sum())
if duplicate_count > 0:
    df = df.drop_duplicates().copy()

print("\\nExact duplicate rows removed:", duplicate_count)

# ------------------------------------------------------------
# 5. IDENTIFY COLUMN TYPES
# ------------------------------------------------------------
categorical_cols = [c for c in ["Country", "Year", "Month"] if c in df.columns]
date_cols = [c for c in ["Date"] if c in df.columns]
numeric_cols = [
    c for c in df.columns
    if c not in categorical_cols + date_cols
]

# ------------------------------------------------------------
# 6. CONVERT DATA TYPES
# ------------------------------------------------------------
if "Date" in df.columns:
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

print("\\nInvalid Date values:", int(df["Date"].isna().sum()))

# ------------------------------------------------------------
# 7. SORT CHRONOLOGICALLY
# ------------------------------------------------------------
if "Date" in df.columns:
    df = df.sort_values("Date").reset_index(drop=True)
    print("Date range:", df["Date"].min(), "to", df["Date"].max())

# ------------------------------------------------------------
# 8. HANDLE INFINITE VALUES
# ------------------------------------------------------------
df.replace([np.inf, -np.inf], np.nan, inplace=True)

# ------------------------------------------------------------
# 9. HANDLE NUMERIC MISSING VALUES
# ------------------------------------------------------------
missing_numeric_before = int(df[numeric_cols].isna().sum().sum())

df[numeric_cols] = (
    df[numeric_cols]
    .interpolate(method="linear", limit_direction="both")
)

missing_numeric_after = int(df[numeric_cols].isna().sum().sum())

print("\\nNumeric missing cells before interpolation:", missing_numeric_before)
print("Numeric missing cells after interpolation:", missing_numeric_after)

# ------------------------------------------------------------
# 10. TIME-BASED FEATURE ENGINEERING
# ------------------------------------------------------------
if "Date" in df.columns:
    df["observation_year"] = df["Date"].dt.year
    df["observation_month"] = df["Date"].dt.month
    df["observation_quarter"] = df["Date"].dt.quarter
    df["observation_week"] = df["Date"].dt.isocalendar().week.astype("Int64")
    df["observation_day"] = df["Date"].dt.day
    df["month_name"] = df["Date"].dt.month_name()

# ------------------------------------------------------------
# 11. PERCENTAGE CHANGE FOR SELECTED INDICATORS
# ------------------------------------------------------------
m3_col = next(
    (c for c in numeric_cols if c.lower().startswith("m3 (")),
    None
)

fx_col = next(
    (c for c in numeric_cols if "net foreign exchange assets" in c.lower()),
    None
)

if m3_col:
    df["m3_pct_change"] = df[m3_col].pct_change() * 100

if fx_col:
    df["net_fx_assets_pct_change"] = df[fx_col].pct_change() * 100

# ------------------------------------------------------------
# 12. IQR OUTLIER DETECTION
# ------------------------------------------------------------
print("\\n" + "=" * 70)
print("OUTLIER DETECTION — IQR METHOD")
print("=" * 70)

outlier_report = []

for col in numeric_cols:
    series = df[col].dropna()
    if series.empty:
        continue

    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)
    iqr = q3 - q1

    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    mask = (series < lower_bound) | (series > upper_bound)
    count = int(mask.sum())

    outlier_report.append({
        "column": col,
        "outlier_count": count,
        "lower_bound": lower_bound,
        "upper_bound": upper_bound
    })

outlier_report = pd.DataFrame(outlier_report)
print(outlier_report.sort_values("outlier_count", ascending=False).head(20))

# IMPORTANT:
# Outliers are not automatically deleted. Economic time-series extremes
# may be genuine observations or structural changes.

# ------------------------------------------------------------
# 13. NEGATIVE-VALUE VALIDATION
# ------------------------------------------------------------
negative_counts = (df[numeric_cols] < 0).sum()
negative_counts = negative_counts[negative_counts > 0].sort_values(ascending=False)

print("\\nNegative values by column:")
print(negative_counts)

# Negative values are not automatically errors because some economic
# variables are net positions and may legitimately take negative values.

# ------------------------------------------------------------
# 14. FINAL QUALITY VALIDATION
# ------------------------------------------------------------
print("\\n" + "=" * 70)
print("FINAL DATA QUALITY VALIDATION")
print("=" * 70)

final_missing = int(df.isna().sum().sum())
final_duplicates = int(df.duplicated().sum())
final_invalid_dates = int(df["Date"].isna().sum()) if "Date" in df.columns else 0
final_infinite = int(
    np.isinf(df.select_dtypes(include=np.number)).sum().sum()
)

print("Rows:", len(df))
print("Columns:", len(df.columns))
print("Remaining missing cells:", final_missing)
print("Remaining duplicate rows:", final_duplicates)
print("Invalid dates:", final_invalid_dates)
print("Infinite numeric values:", final_infinite)

# ------------------------------------------------------------
# 15. EXPORT CLEANED DATASET
# ------------------------------------------------------------
df.to_csv(CLEANED_PATH, index=False)

print("\\nCleaned dataset saved as:", CLEANED_PATH)
print("Final shape:", df.shape)
print("=" * 70)
print("WEEK 1 PREPROCESSING COMPLETED")
print("=" * 70)
