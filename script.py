import requests
import csv
import json
import csvrs 
from flask import Flask, request, jsonify
from flask_cors import CORS


app = Flask(__name__)
API_KEY = "38397f5a75dcc2e24468f08066ac0ce7c91d5f1e"
url = "https://google.serper.dev/places"
headers = {
    'X-API-KEY': API_KEY,
    'Content-Type': 'application/json'
}
origins = ["https://info-scrapper.vercel.app"]


CORS(app, resources={r"/*": {"origins":origins}})

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


    analyzer = csvrs.Analyzer_csv("restaurants.csv")
    analyzer.create_list()
    return analyzer.jsonify_it()


@app.route('/', methods=['POST'])
def home():
    content_type = request.headers.get("Content-Type")
    print("the type : ", content_type )

    if not (content_type and 'application/json' in content_type):
        return jsonify({"error":"request must be json and sent as POST"}), 400

    data = request.get_json()
    print(f"the parsed data : ", data )

    if not data:
        return jsonify({"error":"No data provided"}), 400
    
    query = data.get("query")
    print("query : ", query)
    if query:
        res = fetch_data(query)
    else:
        return jsonify({"error": "didn't revieve any data"})
    
    return jsonify({"data":res})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
