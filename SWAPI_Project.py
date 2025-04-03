import requests
import json
import os

def get_swapi_resource(resource_type, resource_id=None, search_query=None):
    """
    Function to get data from SWAPI
    resource_type: people, planets, starships, etc.
    resource_id: optional specific ID to retrieve
    search_query: optional search parameter
    """
    base_url = "https://swapi.dev/api"
    
    if resource_id:
        url = f"{base_url}/{resource_type}/{resource_id}/"
    elif search_query:
        url = f"{base_url}/{resource_type}/?search={search_query}"
    else:
        url = f"{base_url}/{resource_type}/"
        
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None

def save_request(response, filename):
    os.makedirs("requests_data", exist_ok=True)
    with open(f"request_data/{filename}.json", "w") as file:
        json.dump(response, file,indent=4)

def search_by_character(name):
    data = get_swapi_resource("people", None, name)
    if data and data["count"] > 0:
        top_result = data["results"][0]
        print(f"Name: {top_result["name"]}")
        print(f"Height: {top_result["height"]}")
        print(f"Mass: {top_result["mass"]}")
        print(f"Birth Year: {top_result["birth_year"]}")
    else:
        print("No Results Found")

def compare(search_1, search_2, search_type):
    data_1 = get_swapi_resource(search_type, None, search_1)
    data_2 = get_swapi_resource(search_type, None, search_2)
    if data_1 and data_2 and data_1["count"] > 0 and data_2["count"] > 0:
        top_result_1 = data_1["results"][0]
        top_result_2 = data_2["results"][0]
        print("\nComparison:")
        count = 0
        for (k,v), (k2,v2) in zip(top_result_1.items(),top_result_2.items()):
            print(f"{k}: {v} vs {v2}")
            count += 1
            if count == 5:
                break
    else:
        print("No Results Found")


compare("millennium falcon", "death star", "starships")