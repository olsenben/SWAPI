import requests
import json
import matplotlib as plt

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


def graph_most_common(search_type, key):

        """graph the most common of the queired type (species, starships) at the specified key"""
        data = self.get_swapi_resource(search_type)
        #not going to save this query to file since it will literally save every datapoint from the endpoint
        results = {}
        
        for data in data["results"]:
            results[data[key]] += 1

        names = [i for i in results.keys()]
        counts = [results[i] for i in results.items()]

        plt.bar(names, counts)
        plt.xlabel(f"{key}s")
        plt.ylabel("Count")
        plt.xticks(rotation=45)
        plt.title(f"Most Common {key}s")
        plt.show()        

graph_most_common("starships", "manufacturer")