import pandas as pd

# List of seasons to scrape
seasons = ["1516", "1617", "1718", "1819", "1920", "2021", "2122", "2223", "2324"]

# Empty list to store DataFrames
dataframes = []

# Loop through and scrape data for each season
for season in seasons:
    url = f"https://www.football-data.co.uk/mmz4281/{season}/E0.csv"
    df = pd.read_csv(url)

    # Add a 'season' column to track the season
    df["season"] = season  

    # Append to list
    dataframes.append(df)
    
    print(f"Season {season}: {df.shape[0]} matches scraped")

# Concatenate all DataFrames into one
epl_data = pd.concat(dataframes, ignore_index=True)

# Save as a pickle file
pickle_filename = "epl_data.pkl"
pd.to_pickle(epl_data, pickle_filename)

print(f"Data saved as {pickle_filename}")

# Load saved data
epl_data = pd.read_pickle("epl_data.pkl")

# Filter for a specific season (e.g., 2023-24)
epl_2324 = epl_data[epl_data["season"] == "2324"]

print(epl_2324.head())  # Show first few rows


# Define criteria to filter for home wins and home team scoring more than 2 goals
filter_criteria = 'FTR == "H" & FTHG > 2'

# Apply the filter to the DataFrame
epl_filtered = epl_data.query(filter_criteria)

# Display the filtered data
print(epl_filtered.head())

