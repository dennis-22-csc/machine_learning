# ----------------------
# Import Required Libraries
# ----------------------
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf
import numpy as np
import os.path
from sklearn.impute import KNNImputer
from sklearn.decomposition import PCA
from scipy.cluster.vq import vq, kmeans

# ----------------------
# Web Scraping Combine Data
# ----------------------
combine_py = pd.DataFrame()

for year in range(2000, 2023 + 1):
    url = f"https://www.pro-football-reference.com/draft/{year}-combine.htm"
    web_data = pd.read_html(url)[0]
    web_data["Season"] = year
    web_data = web_data.query('Ht != "Ht"')  # Remove header rows
    combine_py = pd.concat([combine_py, web_data])

combine_py.reset_index(drop=True, inplace=True)

# ----------------------
# Data Cleaning & Transformation
# ----------------------
# Convert height from feet-inches to total inches
combine_py[["Ht-ft", "Ht-in"]] = combine_py["Ht"].str.split("-", expand=True)
combine_py = combine_py.astype({
    "Ht-ft": float,
    "Ht-in": float,
    "Wt": float,
    "40yd": float,
    "Vertical": float,
    "Bench": float,
    "Broad Jump": float,
    "3Cone": float,
    "Shuttle": float
})

combine_py["Ht"] = combine_py["Ht-ft"] * 12 + combine_py["Ht-in"]
combine_py.drop(["Ht-ft", "Ht-in"], axis=1, inplace=True)

# ----------------------
# Handle Missing Values with KNN Imputation
# ----------------------
cols_to_impute = ["Ht", "Wt", "40yd", "Vertical", 
                 "Bench", "Broad Jump", "3Cone", "Shuttle"]

# Preserve non-numeric columns
combine_meta = combine_py.drop(cols_to_impute, axis=1)

# Perform KNN imputation
imputer = KNNImputer(n_neighbors=10)
imputed_data = imputer.fit_transform(combine_py[cols_to_impute])
combine_imputed = pd.DataFrame(imputed_data, columns=cols_to_impute)

# Recombine data
combine_clean = pd.concat([combine_meta, combine_imputed], axis=1)


# Save the filtered dataset as a pickle file
combine_clean.to_pickle("filtered_nfl_combine_ch8_plays.pkl")

# Load the dataset later
pbp_py_run_loaded = pd.read_pickle("filtered_nfl_combine_ch8_plays.pkl")

# Display the first few rows to verify
print(pbp_py_run_loaded.head())

