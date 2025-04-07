import cloudscraper
from bs4 import BeautifulSoup

def get_all_table_containers(url):
    # Create a CloudScraper instance to bypass Cloudflare protection
    scraper = cloudscraper.create_scraper()
    response = scraper.get(url)
    
    # Check if the request was successful
    if response.status_code != 200:
        raise Exception(f"Failed to retrieve page. Status code: {response.status_code}")
    
    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find all divs containing tables
    table_containers = soup.find_all('div', {'id': True})  # Find all divs with an 'id' attribute

    if not table_containers:
        raise Exception("No table containers found")
    
    # Print out the IDs of all table containers
    print("Found table containers with the following IDs:")
    for div in table_containers:
        if div.find('table'):  # Ensure the div actually contains a table
            print(div['id'])
    
    return [div['id'] for div in table_containers if div.find('table')]

if __name__ == "__main__":
    url = "https://fbref.com/en/comps/9/2021-2022/shooting/2021-2022-Premier-League-Stats"
    
    try:
        table_ids = get_all_table_containers(url)
        print("\nTable container IDs found:", table_ids)
        
    except Exception as e:
        print(f"Error: {str(e)}")

