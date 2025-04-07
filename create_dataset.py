import pandas as pd

# Load the dataset
df = pd.read_csv("datasets/crime.csv", encoding="ISO-8859-1")

# Filter for records from 2018
df_2018 = df[df["YEAR"] == 2018]

# Save to a new CSV file
df_2018.to_csv("filtered_2018_dataset.csv", index=False)

print("New dataset saved as 'filtered_2018_dataset.csv'.")

