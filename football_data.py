import numpy as np
import pandas as pd
import nfl_data_py as nfl  # Assuming you're using nfl_data_py

# Define the seasons to analyze
seasons = range(2016, 2022 + 1)

# Load NFL play-by-play data for selected seasons
pbp_py = nfl.import_pbp_data(seasons, cache=True)

# Save the filtered dataset as a pickle file
pbp_py.to_pickle("filtered_nfl_data.pkl")

# Load the dataset later
pbp_py_loaded = pd.read_pickle("filtered_nfl_data.pkl")

# Display the first few rows to verify
print(pbp_py_loaded.head())

