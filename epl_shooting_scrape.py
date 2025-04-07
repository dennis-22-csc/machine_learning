import cloudscraper
from bs4 import BeautifulSoup, Comment
import pandas as pd

# List of seasons
seasons = [f"{year}-{year + 1}" for year in range(2015, 2025)]

# Initialize CloudScraper to bypass anti-bot measures
scraper = cloudscraper.create_scraper()

# Initialize an empty list to collect dataframes
dfs = []

# Loop through each season and scrape the data
for season in seasons:
    url = f"https://fbref.com/en/comps/9/{season}/shooting/{season}-Premier-League-Stats"

    # Send request to the URL
    response = scraper.get(url)

    # Parse HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the commented table containing the stats
    comments = soup.find_all(string=lambda text: isinstance(text, Comment))
    table_html = None
    for comment in comments:
        if 'div_stats_shooting' in comment:
            comment_soup = BeautifulSoup(comment, 'html.parser')
            table = comment_soup.find('table', id='stats_shooting')
            if table:
                table_html = str(table)
                break

    # Convert HTML table to DataFrame
    if table_html:
        df = pd.read_html(table_html, header=[0, 1])[0]  # Read with multi-index headers
        
        # Flatten the MultiIndex columns
        df.columns = ['_'.join(col).strip() if isinstance(col, tuple) else col for col in df.columns]

        # Clean up prefixes and suffixes
        df.columns = df.columns.str.replace('^Unnamed: \d+_level_0_', '', regex=True)  # Remove unwanted parts like 'Unnamed: 0_level_0_'
        df.columns = df.columns.str.replace('Standard_', '')  # Remove "Standard_" prefix

        # Add season column
        df['season'] = season

        # Append the dataframe to the list
        dfs.append(df)
    else:
        print(f"Table not found for season {season}")

# Concatenate all season dataframes
full_df = pd.concat(dfs, ignore_index=True)

# Align columns across all seasons and fill missing columns with NaN
full_df = full_df.reindex(columns=full_df.columns.union(full_df.columns, sort=False), fill_value=pd.NA)

# Save to CSV
full_df.to_csv('epl_shooting_all_seasons.csv', index=False)
print("Data saved successfully!")

