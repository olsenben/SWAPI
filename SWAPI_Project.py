import requests
import json
import os
from collections import Counter
import matplotlib as plt



class SWAPI():

    """Class for working with Star Wars API"""


    def __init__(self, base_url):
        self.base_url = base_url

    def get_swapi_resource(self,resource_type, resource_id=None, search_query=None):
        """
        Function to get data from SWAPI
        resource_type: people, planets, starships, etc.
        resource_id: optional specific ID to retrieve
        search_query: optional search parameter
        """
        #base_url = "https://swapi.dev/api"
        
        if resource_id:
            url = f"{self.base_url}/{resource_type}/{resource_id}/"
        elif search_query:
            url = f"{self.base_url}/{resource_type}/?search={search_query}"
        else:
            url = f"{self.base_url}/{resource_type}/"
            
        response = requests.get(url)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code}")
            return None

    def save_request(self, query, dict, filename):
        """saves json response to file in requests_data directory"""
        query_dict = {}
        query_dict[query] = dict
        os.makedirs("requests_data", exist_ok=True)
        if os.path.exists(f"requests_data/{filename}.json"):
            with open(f"requests_data/{filename}.json", "r+") as file:
                data = json.load(file)
                data.update(query_dict)

                file.seek(0)

                json.dump(data, file, indent=4)

                file.truncate()

        else:
            with open(f"requests_data/{filename}.json", "w") as file:
                data = query_dict
                json.dump(data, file,indent=4)

    
    def search_by_character(self, name):
        """queries people endpoint by character name"""
        
        data = self.get_swapi_resource("people", None, name)
        
        #if results are found
        if data and data["count"] > 0:
            
            #save the data to file
            self.save_request(name, data["results"][0], "people")
            return data["results"][0]
           
        else:
            return "No Results Found"

    def get_url_name_field(self, key, value):
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

    def compare_info(self, search_1, search_2, search_type):
        """Compares data between two queries, prints info for both sided by side
        
        Input:
            search_1 (str): search term one
            search_2 (str): search term 2
            search_type (str): endpoint being queried: "films" "people" "planets" "species" "starships" "vehicles"
        """
        #query each search term according to search type
        data_1 = self.get_swapi_resource(search_type, None, search_1)
        data_2 = self.get_swapi_resource(search_type, None, search_2)

        #check if any results are returned
        if data_1 and data_2 and data_1["count"] > 0 and data_2["count"] > 0:
            
            #save results
            self.save_request(search_1, data_1["results"][0], search_type)
            self.save_request(search_2, data_2["results"][0], search_type)

            #isolate top result for both and grab name fields for urls
            top_result_1 = data_1["results"][0]
            for k,v in top_result_1.items():
                top_result_1[k] = self.get_url_name_field(k,v)

            top_result_2 = data_2["results"][0]
            for k,v in top_result_2.items():
                top_result_2[k] = self.get_url_name_field(k,v)

            
            return zip(top_result_1.items(),top_result_2.items())
        
        else:
            return "No Results Found"


    def find_character_connections(self,character_1, character_2):
        """Find similarities between two characters and prints them"""

        #query each search term
        data_1 = self.get_swapi_resource("people", None, character_1)
        data_2 = self.get_swapi_resource("people", None, character_2)

        #if results found
        if data_1 and data_2 and data_1["count"] > 0 and data_2["count"] > 0:
            
            #save to file
            self.save_request(character_1, data_1["results"][0], "people")
            self.save_request(character_2, data_2["results"][0], "people")
            
            #query endpoints in lists
            top_result_1 = data_1["results"][0]
            for k,v in top_result_1.items():
                top_result_1[k] = self.get_url_name_field(k,v)
            
            top_result_2 = data_2["results"][0]
            for k,v in top_result_2.items():
                top_result_2[k] = self.get_url_name_field(k,v)
            
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

            return matches
        
        #if one of the search terms returns no results, print no results found
        else:
            return "No Results found"
        
    def show_most_common(self,category):
        url = f"{self.base_url}/{category}"
        all_results = []

        while url:
            response = requests.get(url)
            if response.status_code != 200:
                print(f"Error: {response.status_code}")
                break
            
            data = response.json()
            all_results.extend(data["results"])
            url = data.get('next')

        if not all_results:
            return "No Results Found"

        name_counts = Counter(result["name"] for result in all_results)       

        return name_counts

def main():
    base_url = "https://swapi.dev/api"
    sw_api = SWAPI(base_url)

    while True:
        print("\nOptions:")
        print("1. Search by character")
        print("2. Compare Info")
        print("3. Find Character Connections")
        print("4. Show Most Common By Category")
        print("5. Exit")

        choice = input("Please make selection: ")

        if choice == "1":
            
            #query search term
            search_term = input("Please input character name: ")
            data = sw_api.search_by_character(search_term)
            
            #iterate over results and print
            if isinstance(data, dict):
                print("\nResults: ")
                for k, v in data.items():
                    new_value = sw_api.get_url_name_field(k,v)  
                    print(f"{k}: {new_value}")
            
            #if search returns no results, it will print "No results Found"
            else:
                print(data)
        
        elif choice == "2":
            
            search_types = ["films", "people", "planets", "species","starships", "vehicles"] 

            #query search terms 
            search_term_1 = input("Please input first search term to compare: ")
            search_term_2 = input("Please input second search term to compare: ")
            search_type = input(f"Please input search type: {search_types}")

            while search_type not in search_types: 
                search_type = input(f"Please input valid search type: {search_types}")

            data = sw_api.compare_info(search_term_1, search_term_2, search_type)

            if isinstance(data, zip): #might be an issure because its zipped so not sure if still a dict

                #print comparison between both dictionaries    
                print("\nComparison:")
                for (k,v), (k2,v2) in data:
                    print(f"{k}: {v} vs {v2}")
            
            else:
                print(data)

        elif choice == "3":
            search_term_1 = input("Please input first character: ")
            search_term_2 = input("Please input second character: ")

            #query search terms 
            data = sw_api.find_character_connections(search_term_1, search_term_2)

            if isinstance(data, dict):
                #print results            
                print(f"\nConnections found between {search_term_1} and {search_term_2}")
                for k, v in data.items():
                    print(f"{k}: {v}")
            else:
                print(data)

        elif choice == "4":
            search_types = ["species","starships","vehicles"] 

            #query search terms 
            search_type = input(f"Please input category: {search_types}")
        
            while search_type not in search_types: 
                search_type = input(f"Please input valid search type: {search_types}")

            data = sw_api.show_most_common(search_type)

            #plot if results are found
            if isinstance(dict, data):

                x_names = data.keys()
                y_counts = data.values()

                plt.plot(x_names, y_counts)
                plt.xlabel(f"{search_type}")
                plt.ylabel("Counts")
                plt.title(f"Most common {search_type}")
                plt.show()
            
            else:
                print("No Results Found")


        elif choice == "5": 
            print("Exiting program. May the Force be with you!")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 4.")


if __name__ == "__main__":
    main()
