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
    """saves json response to file in requests_data directory"""
    
    os.makedirs("requests_data", exist_ok=True)
    with open(f"request_data/{filename}.json", "w") as file:
        json.dump(response, file,indent=4)

def search_by_character(name):
    """queries people endpoint by character name"""
    
    data = get_swapi_resource("people", None, name)
    
    #if results are found
    if data and data["count"] > 0:

        #iterate over results and print
        for k, v in data["results"][0].items(): 

            new_value = get_url_name_field(k,v)
                
            print(f"{k}: {new_value}")
    else:
        print("No Results Found")

def get_url_name_field(key, value):
    """
    takes a key and value from a json query and checks if that value is a list of urls, queries the urls and returns the first value of each one in a list
    
    Input: 
        key (str): dictionary key
        value (str): dictionary value associated with input key, possibly containing list of urls 

    Output:
        list: list of first value from query
        str: original input value if the value was not a list of urls
    
    """
    #check for url links
    urls_fields = ["homeworld", "films", "species", "vehicles", "starships", "characters","planets", "pilots", "people", "residents"]
    #if keys value holds url links
    if key in urls_fields:
        
        #for this to work, homeworld must be a list
        if key == "homeworld":
            value = [value]

        #store url names
        urls_name_list = []

        #iterate over each url, request and print first field (title or name)
        for url in value:
            url_data = requests.get(url).json()
            
            #append first entry (name or title) to urls_names
            if url_data:
                name = list(url_data.values())[0]
                urls_name_list.append(name)
        
        return urls_name_list
    
    #if its not in urls_fields just return original value  
    else:
        return value

def compare_info(search_1, search_2, search_type):
    """Compares data between two queries, prints info for both sided by side
    
    Input:
        search_1 (str): search term one
        search_2 (str): search term 2
        search_type (str): endpoint being queried: "films" "people" "planets" "species" "starships" "vehicles"
    """
    #query each search term according to search type
    data_1 = get_swapi_resource(search_type, None, search_1)
    data_2 = get_swapi_resource(search_type, None, search_2)

    #check if any results are returned
    if data_1 and data_2 and data_1["count"] > 0 and data_2["count"] > 0:
        
        #isolate top result for both and grab name fields for urls
        top_result_1 = data_1["results"][0]
        for k,v in top_result_1.items():
            top_result_1[k] = get_url_name_field(k,v)

        top_result_2 = data_2["results"][0]
        for k,v in top_result_2.items():
            top_result_2[k] = get_url_name_field(k,v)

        #print comparison between both dictionaries    
        print("\nComparison:")
        for (k,v), (k2,v2) in zip(top_result_1.items(),top_result_2.items()):
            print(f"{k}: {v} vs {v2}")
    
    else:
        print("No Results Found")


def find_character_connections(character_1, character_2):
    """Find similarities between two characters and prints them"""

    #query each search term
    data_1 = get_swapi_resource("people", None, character_1)
    data_2 = get_swapi_resource("people", None, character_2)

    #if results found
    if data_1 and data_2 and data_1["count"] > 0 and data_2["count"] > 0:
        
        #query endpoints in lists
        top_result_1 = data_1["results"][0]
        for k,v in top_result_1.items():
            top_result_1[k] = get_url_name_field(k,v)
        
        top_result_2 = data_2["results"][0]
        for k,v in top_result_2.items():
            top_result_2[k] = get_url_name_field(k,v)
        
        #store potential matches 
        matches = {}

        #check for matches between results
        for key in top_result_1:
            if key in top_result_2:
                value_1, value_2 = top_result_1[key], top_result_2[key]

                #check for overlap between values that are lists
                if isinstance(value_1, list) and isinstance(value_2, list):
                    shared_values = list(set(value_1) & set(value_2))        
                    if shared_values:
                        matches[key] = shared_values

                #if there are matches add them to dict matches
                elif value_1 == value_2:
                    matches[key] = value_1

        #print results            
        print(f"\nConnections found between {top_result_1["name"]} and {top_result_2["name"]}")
        for k, v in matches.items():
            print(f"{k}: {v}")
    
    #if one of the search terms returns no results, print no results found
    else:
        print("No Results found")




find_character_connections("chewbacca","han solo")