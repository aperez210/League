import os
from dotenv import load_dotenv
import requests,json
from urllib.parse import quote

# Load API key from .env
load_dotenv()
API_KEY = os.getenv("ARENA_KEY")
CRACKPIPE = os.getenv("MY_PUUID")
RIOT = "https://americas.api.riotgames.com"
if not API_KEY:
    raise ValueError("Missing RIOT_API_KEY in .env file")

def acc_by_rid(rid:str,tag:str):
    response = requests.get(f"{RIOT}/riot/account/v1/accounts/by-riot-id/{quote(rid)}/{tag}?api_key={API_KEY}")
    if response.status_code == 200:
        return(list(response.json().values()))
    else:
        return(f"Request failed with status code {response.status_code}")

def games_by_puuid(puuid:str):
    response = requests.get(f"{RIOT}/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count=20&api_key={API_KEY}")
    if response.status_code == 200:
        return(response.json())
    else:
        return(f"Request failed with status code {response.status_code}")

def save_game(text, saves:int, ext="json"):
    filename = "game"
    os.makedirs("games", exist_ok=True)
    if not filename.endswith(f".{ext}"):
        filename = f"game{saves}.{ext}"
    filepath = os.path.join("games", filename)
    try:
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(text)
        saves+=1
        print(f"Text successfully written to {filepath}")
    except Exception as e:
        print(f"An error occurred: {e}")

def  match_info(mid:str):
    response = requests.get(f"{RIOT}/lol/match/v5/matches/{mid}?api_key={API_KEY}")
    if response.status_code == 200:
        return(response.json())
    else:
        return(f"Request failed with status code {response.status_code}")
    
class acc:
    def __init__(self, values):
        if not isinstance(values, list):
            raise TypeError("values must be a list")
        if len(values) != 3:
            raise ValueError("list must have exactly 3 elements")
        self.puuid = values[0]
        self.gameName = values[1]
        self.tagLine = values[2]
    def __str__(self):
        return f"{self.puuid}, {self.gameName}#{self.tagLine}"
    def get_games(self):
        self.games = games_by_puuid(self.puuid)

def listDispChoose(l:list):
    n = 1
    for choice in l:
        print(f"{n}:{choice}")
    try:
        selection = int(input("Select an option:"))
    except:
        selection = 0

def get_acc_by_name(name:str,suffix:str):
    return acc(acc_by_rid(name,suffix))
        
def get_games_by_name(name:str,suffix:str):
    return games_by_puuid(get_acc_by_name(name,suffix))
#Crackpipe = get_acc_by_name("Crackpipe Perez","NA1")
#myGames =  games_by_puuid(Crackpipe.puuid)

myGames = get_acc_by_name("Crackpipe Perez","NA1")
gameInfo = []
saves = 0
for x in myGames:
    game = match_info(x)
    y = game
    saves+=1
    save_game(json.dumps(y,indent=3),saves)
    gameInfo.append(y)

