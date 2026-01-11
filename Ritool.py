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
    
def games_by_puuid(puuid:str):
   #log("attempting to get games by puuid")
    s = f"{RIOT}/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count=20&api_key={API_KEY}"
    response = requests.get(s)
    if response.status_code == 200:
        print("success")
        return(response.json())
    else:
        print("failed")
        
        return(f"Request failed with status code {response.status_code}")
    
def  match_info(mid:str):
    #log("attempting to get match info")
    response = requests.get(f"{RIOT}/lol/match/v5/matches/{mid}?api_key={API_KEY}")
    if response.status_code == 200:
        r = response.text
        #log(f"success!")
        return r
    else:
        #log("failure")
        return(f"Request failed with status code {response.status_code}")  

