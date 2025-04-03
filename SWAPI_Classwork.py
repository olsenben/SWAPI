import requests
import json
import os
import datetime 

data_dir = "api_data"

if not os.path.exists(data_dir):
    os.makedirs(data_dir)

class StarWarsAPI:
    """Class for working with Star Wars API"""

    def __init__(self):
        self.base_url = "https://swapi.dev/api/"

    def get_resource(self, resource_type, resource_id=None, search=None):
        """get resource from API"""
        url = f"{self.base_url}/{resource_type}/"

        if resource_id:
            url += f"{resource_id}"
        elif search:
            url += f"?search={search}"
        
        response = requests.get(url)
        if response.status_code == 200:
           return response.json()
        
        else:
            print(f"Error: {response.status_code}")
            return None

class NotesManager:
    """class for managing notes about our star wars data"""
    def __init__(self, storage_dir='api_data'):
        self.storage_dir = storage_dir
        self.notes_file = os.path.join(storage_dir, "character_notes.json")
        self.notes = self._load_notes()

    def _load_notes(self):
        if os.path.exists(self.notes_file):
            with open(self.notes_file, "r") as file:
                return json.load(file)
        return {}
    
    def save_notes(self):
        with open(self.notes_file, "w") as file:
            json.dump(self.notes)

    def add_note(self, character_id, note_text):
        if character_id not in self.notes:
            self.notes[character_id] = []

        self.notes[character_id].append({
            "text" : note_text,
            "timestamp" : datetime.datetime.now()
        })

def main():
    sw_api = StarWarsAPI
    notes_manager = NotesManager()
    character = sw_api.get_resource("people", 1)

    while True:
        print("\nOptions:")
        print("1. Search for a character")
        print("2. View character details")
        print("3. Add a note about a character")
        print("4. View notes about a character")
        print("5. Save character data to file")
        print("6. Exit")

        choice = input("\nEnter a choice (1-6): ")

        if choice == '1'L
            search_term = input("Enter character name to search: ")
            results = sw_api.get_resource("people", search_term)

        if character:
            character_data = {
                "info": character,
                "notes": notes_manager.get_notes(person_id),
                "films": [],
                "starships": []

            }

#main()