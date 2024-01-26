import csv
import requests
import time
import subprocess

# Gets a list of appids from all of the owned games in the Steam users library
def get_owned_games(steam_api_key, steam_user_id):
    api = f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={steam_api_key}&steamid={steam_user_id}&format=json"

    try:
        response = requests.get(api)
        response.raise_for_status()

        data = response.json()

        if 'games' in data['response']:
            owned_games = data['response']['games']
            return owned_games
        else:
            print("No games found")
            return None
    
    except requests.exceptions.RequestException as e:
        print(f"Error making API request: {e}")
        return None

# Requests the game names from the store api, looking for names through appid
def get_game_name(appid, steam_api_key):
    store_api = f"http://store.steampowered.com/api/appdetails/?appids={appid}&key={steam_api_key}"

    try:
        response = requests.get(store_api)
        response.raise_for_status()

        data = response.json()

        if str(appid) in data and 'data' in data[str(appid)] and 'name' in data[str(appid)]['data']:
            return data[str(appid)]['data']['name']
        else:
            None
    except requests.exceptions.RequestException as e:
        print(f"Error making Store API request: {e}")
        return f"Error getting game name for app ID {appid}"

def save_to_csv(owned_games, steam_api_key, steam_username, csv_filename='owned_games_temp.csv'):
    if owned_games:
        try:
            with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
                # Creates the columns of User and GameName in the csv
                fieldnames = ['User', 'GameName']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                writer.writeheader()
                # Writes the username and game name in each row
                for game in owned_games:
                    appid = game['appid']
                    game_name = get_game_name(appid, steam_api_key)
                    writer.writerow({'User': steam_username, 'GameName': game_name})  
                    time.sleep(1)

            print(f"Data saved to {csv_filename}")
        except Exception as e:
            print(f"Error saving to CSV: {e}")
    else:
        print("No data to save.")

steam_api_key = # My Steam API key
steam_user_id = input("What is your Steam user ID? (Enter the numbers on your account details page) ")
steam_username = input("What is your username? (The name you go by on Steam) ")

# Call the get_owned_games function and store the result in owned_games
owned_games = get_owned_games(steam_api_key, steam_user_id)

if owned_games:
    save_to_csv(owned_games, steam_api_key, steam_username)
