# Week 1 — Data Acquisition, Cleaning & Preprocessing

## RBI Weekly Monetary & Banking Indicators

This project documents the Week 1 data analytics workflow for acquiring, exploring, cleaning, and preprocessing a public RBI-derived economic time-series dataset using Python.

### Student
- **Name:** Tapati Roy
- **Programme:** B.Tech Biotechnology with Artificial Intelligence
- **Institution:** Techno India University

## Project Objective

The objective is to prepare a reliable, analysis-ready dataset by:

- Acquiring a public dataset from a reliable source
- Exploring its structure and data quality
- Identifying missing values and duplicate records
- Validating and converting data types
- Cleaning text and date fields
- Detecting potential outliers using the IQR method
- Preserving economically meaningful extreme observations
- Creating useful time-based features
- Exporting the cleaned dataset for further analysis

## Dataset

The dataset contains weekly RBI economic indicators covering monetary aggregates, deposits, bank credit, government credit, foreign-exchange assets, and related banking-sector liabilities.

- **Raw observations:** 675
- **Original columns:** 26
- **Source:** Reserve Bank of India (RBI)
- **Source website:** https://www.rbi.org.in/

## Files in This Project

| File | Description |
|---|---|
| `week1_data_cleaning.py` | Complete Python preprocessing script |
| `RBI_weekly_dataset_cleaned.csv` | Cleaned and preprocessed dataset |
| `Week_1_Data_Acquisition_Cleaning_Preprocessing_Tapati_Roy.docx` | Detailed Week 1 report |
| `charts/` | Visualizations and screenshots generated during analysis |

## Cleaning Workflow

1. Load the raw CSV with Pandas.
2. Inspect shape, columns, data types, descriptive statistics, and sample records.
3. Standardize column names and strip unnecessary whitespace.
4. Check and remove exact duplicate rows.
5. Convert the `Date` column to Pandas datetime.
6. Convert economic indicator fields to numeric values.
7. Replace infinite values with missing values.
8. Sort observations chronologically.
9. Interpolate numeric missing values using linear interpolation where appropriate for the time series.
10. Create year, month, quarter, week, day, and month-name features.
11. Calculate percentage changes for selected indicators.
12. Detect potential outliers using the 1.5 × IQR rule.
13. Validate the final dataset.
14. Export the cleaned CSV.

## Outlier Policy

Potential outliers are **flagged rather than automatically deleted**. In economic time-series data, extreme values may represent genuine monetary, policy, market, or structural changes. Removing them solely because they are statistically unusual could introduce bias.

## Technologies

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn

## Reproducibility

Place the raw CSV in the same folder as `week1_data_cleaning.py` and run:

```bash
python week1_data_cleaning.py
```

The script generates `RBI_weekly_dataset_cleaned.csv` in the project directory.

## Key Learning

This project demonstrates that data preprocessing is not simply about deleting problematic records. Cleaning decisions must consider the structure and meaning of the dataset. For a weekly economic time series, chronology, continuity, and preservation of meaningful extreme observations are particularly important.

## Author

**Tapati Roy**