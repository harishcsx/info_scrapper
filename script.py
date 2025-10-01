import requests
import csv
import json
import csv_retrival_system

API_KEY = "38397f5a75dcc2e24468f08066ac0ce7c91d5f1e"
url = "https://google.serper.dev/places"
headers = {
    'X-API-KEY': API_KEY,
    'Content-Type': 'application/json'
}


def fetch_data(SEARCH_QUERY: str):
    payload = json.dumps({
        "q": SEARCH_QUERY,
        "num": 60 # Number of results to fetch (can be up to 100)
    })

    print(f"Searching for: '{SEARCH_QUERY}'...")

    try:
        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)

        # Parse the JSON results
        search_results = response.json()
        places = search_results.get('places', [])

        if not places:
            print("No results found.")
        else:
            csv_file_name = "restaurants.csv"
            
            with open(csv_file_name, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                
                writer.writerow(['Name', 'Address', 'Website', 'PhoneNumber', 'Email'])
                
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


query = "restaurants in goa"
fetch_data(query)


analyzer = csv_retrival_system.Analyzer_csv("restaurants.csv")
analyzer.create_list()