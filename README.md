## STAR WARS API (SWAPI)
A Python program that interacts with the Star Wars API (SWAP) to explore and analyze data from the star wars universe. 

# How it works

- ```class SWAPI``` makes requests to SWAPI endpoints (films, people, planets, species, starships, vehicles)
- Saves json response to file in requests_data directory
- Queries people endpoint by character name
- Compares data between two queries, and displays info for both sided by side
- Find similarities between two characters and displays them

# How to run it
- install dependecies ```requests```, ```json```, and ```requests```
- run script ```SWAPI_Project.py```
- script will create ```requests_data``` directory and files if they do not already exist
- requests data is stored on ```JSON``` source files by API endpoint (films, people, planets, species, starships, vehicles)