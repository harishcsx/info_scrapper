import requests
import csv
import json

# --- Configuration ---
# 1. Replace with your actual Serper API key
API_KEY = "247d599c4a425a8781a7abbf2f2aac143fe2f0e0"

# 2. Change this to your desired search query
SEARCH_QUERY = "restaurants in Bhubaneswar"
# --------------------

# API endpoint and headers
url = "https://google.serper.dev/places"
headers = {
    'X-API-KEY': API_KEY,
    'Content-Type': 'application/json'
}

# The data to send in the request
payload = json.dumps({
    "q": SEARCH_QUERY,
    "num": 20 # Number of results to fetch (can be up to 100)
})

print(f"Searching for: '{SEARCH_QUERY}'...")

# Make the API request
try:
    response = requests.post(url, headers=headers, data=payload)
    response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)

    # Parse the JSON results
    search_results = response.json()
    places = search_results.get('places', [])

    if not places:
        print("No results found.")
    else:
        # Define the name of the CSV file
        csv_file_name = "restaurants.csv"
        
        # Open the CSV file for writing
        with open(csv_file_name, mode='w', newline='', encoding='utf-8') as file:
            # Create a CSV writer object
            writer = csv.writer(file)
            
            # Write the header row
            writer.writerow(['Name', 'Address', 'Website', 'PhoneNumber', 'Email'])
            
            # Loop through each place and write its data to the CSV
            for place in places:
                name = place.get('title')
                address = place.get('address')
                website = place.get('website')
                phone = place.get('phoneNumber')
                
                # IMPORTANT: The Maps API does not provide emails.
                # This will always be None unless you scrape the website separately.
                email = None
                
                writer.writerow([name, address, website, phone, email])
        
        print(f"Successfully saved {len(places)} results to {csv_file_name}")

except requests.exceptions.HTTPError as errh:
    print(f"Http Error: {errh}")
except requests.exceptions.ConnectionError as errc:
    print(f"Error Connecting: {errc}")
except requests.exceptions.Timeout as errt:
    print(f"Timeout Error: {errt}")
except requests.exceptions.RequestException as err:
    print(f"Something went wrong: {err}")