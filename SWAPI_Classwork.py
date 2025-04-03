import requests
import json 
import os
from datetime import datetime
import urllib.parse

data_dir = "api_data"
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

class StarWarsAPI:
    """Class for working with Star Wars API"""

    def __init__(self):
        self.base_url = "https://swapi.dev/api/"

    def get_resource(self, resource_type, resource_id=None, search=None):
        url = f"{self.base_url}{resource_type}/" 

        if resource_id:
            url += f"{resource_id}"
        elif search:
            url += f"?search={urllib.parse.quote(search)}"  

        response = requests.get(url)
        if response.status_code == 200:
            return response.json() 
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None
                
class NotesManager:
    """class for managing notes about our star wars data"""

    def __init__(self, storage_dir="api_data"):
        self.storage_dir = storage_dir   
        self.notes_file = os.path.join(storage_dir, "character_notes.json")
        self.notes = self._load_notes()

    def _load_notes(self):
        if os.path.exists(self.notes_file):
            try:
                with open(self.notes_file, 'r') as file:
                    return json.load(file)
            except json.JSONDecodeError:
                print(f"Error: Could not parse {self.notes_file}. Starting with empty notes.")
                return {}
        return {}   

    def save_notes(self):
        with open(self.notes_file, 'w') as file:
            json.dump(self.notes, file, indent=4)

    def add_note(self, character_id, note_text):
        # Ensure character_id is stored as a string
        character_id = str(character_id)
        
        if character_id not in self.notes:
            self.notes[character_id] = []

        self.notes[character_id].append({
            "text": note_text,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

        self.save_notes()

    def get_notes(self, character_id):
        return self.notes.get(str(character_id), [])


def main():
    sw_api = StarWarsAPI()
    notes_manager = NotesManager()

    while True:
        print("\nOptions:")
        print("1. Search for a character")
        print("2. View character details")
        print("3. Add a note about a character")
        print("4. View notes about a character")
        print("5. Save character data to file")
        print("6. Exit")

        choice = input("\nEnter a choice (1 - 6): ")
    
        if choice == '1':
            search_term = input("Enter character name to search: ")
            results = sw_api.get_resource("people", search=search_term)
            
            if results and 'count' in results and results['count'] > 0:
                print(f"\nFound {results['count']} characters:")
                for i, person in enumerate(results['results'], 1):
                    print(f"{i}. {person['name']}")
            else:
                print("No characters found")

        elif choice == '2':
            person_id = input("Enter character ID: ")
            character = sw_api.get_resource("people", person_id)

            if character:
                print(f"\nDetails for {character['name']}:")
                print(f"Height: {character['height']} cm")
                print(f"Mass: {character['mass']} kg")
                print(f"Birth year: {character['birth_year']}")
                print(f"Hair color: {character['hair_color']}")

                homeworld_url = character['homeworld']
                homeworld_id = homeworld_url.split('/')[-2]
                homeworld = sw_api.get_resource("planets", homeworld_id)

                if homeworld:
                    print(f"Homeworld: {homeworld['name']}")
            else:
                print(f"Character with ID {person_id} not found")
                
        elif choice == '3':
            person_id = input("Enter character ID to add a note: ")
            character = sw_api.get_resource("people", person_id)
            
            if character:
                print(f"Adding note for {character['name']}")
                note_text = input("Enter your note: ")
                notes_manager.add_note(person_id, note_text)
            else:
                print(f"Character with ID {person_id} not found")
            
        elif choice == '4':
            person_id = input("Enter character ID to view notes: ")
            character = sw_api.get_resource("people", person_id)
            
            if character:
                notes = notes_manager.get_notes(person_id)
                if notes:
                    print(f"\nNotes for {character['name']}:")
                    for i, note in enumerate(notes, 1):
                        print(f"{i}. [{note['timestamp']}] {note['text']}")
                else:
                    print(f"No notes found for {character['name']}")
            else:
                print(f"Character with ID {person_id} not found")      

        elif choice == '5':
            person_id = input("Enter character ID to save: ")
            character = sw_api.get_resource("people", person_id)

            if character:
                filename = os.path.join(data_dir, f"character_{person_id}_full.json")
                character_data = {
                    "info": character,
                    "notes": notes_manager.get_notes(person_id),
                    "films": [],
                    "starships": [],
                }

                for film_url in character['films']:
                    film_id = film_url.split('/')[-2]
                    film = sw_api.get_resource("films", film_id)
                    if film:
                        character_data["films"].append({
                            "title": film['title'],
                            "episode_id": film['episode_id'],
                            "release_date": film['release_date']
                        })

                for starship_url in character['starships']:
                    starship_id = starship_url.split('/')[-2]
                    starship = sw_api.get_resource("starships", starship_id)
                    if starship:
                        character_data["starships"].append({
                            "name": starship['name'],
                            "model": starship['model'],
                            "manufacturer": starship['manufacturer']
                        })
                
                # save our file!
                with open(filename, 'w') as file:
                    json.dump(character_data, file, indent=4)
                print(f"Character data saved to {filename}") 
            else:
                print(f"Character with ID {person_id} not found")

        elif choice == '6':
            print("Exiting program. May the Force be with you!")
            break
        
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")
    
if __name__ == "__main__":
    main()