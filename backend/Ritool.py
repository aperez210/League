import requests
import os
from dotenv import load_dotenv
from urllib.parse import quote
load_dotenv()

API_KEY = os.getenv("ARENA_KEY")
CRACKPIPE = os.getenv("MY_PUUID")
RIOT = os.getenv("RITO")

if not API_KEY:
    raise ValueError("Missing RIOT_API_KEY in .env file")

def acc_by_rid(rid:str,tag:str):
    response = requests.get(f"{RIOT}/riot/account/v1/accounts/by-riot-id/{quote(rid)}/{tag}?api_key={API_KEY}")
    if response.status_code == 200:
        return(list(response.json().values()))
    else:
        return(f"Request failed with status code {response.status_code}") 
    
def games_by_puuid(puuid:str, queue_id:int=None):
    # get 20 games from riot API using puuid, returns matches from all queues
   #log("attempting to get games by puuid")
    if queue_id is not None:
        s = f"{RIOT}/lol/match/v5/matches/by-puuid/{puuid}/ids?queue={queue_id}&start=0&count=20&api_key={API_KEY}"
    else:
        s = f"{RIOT}/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count=20&api_key={API_KEY}"
    response = requests.get(s)
    if response.status_code == 200:
        print("success")
        return(response.json())
    else:
        print("failed")
        
        return(f"Request failed with status code {response.status_code}")
    
def match_info(match_id:str):
    #log("attempting to get match info")
    response = requests.get(f"{RIOT}/lol/match/v5/matches/{match_id}?api_key={API_KEY}")
    if response.status_code == 200:
        #log(f"success!")
        return response.json()
    else:
        #log("failure")
        return(f"Request failed with status code {response.status_code}")  

