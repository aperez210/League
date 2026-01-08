import os
from dotenv import load_dotenv
import requests,json
from urllib.parse import quote
from datetime import datetime

logging = True

# Load API key from .env
load_dotenv()
API_KEY = os.getenv("ARENA_KEY")
CRACKPIPE = os.getenv("MY_PUUID")
RIOT = "https://americas.api.riotgames.com"

if not API_KEY:
    raise ValueError("Missing RIOT_API_KEY in .env file")

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
        return games_by_puuid(self.puuid)

def time_to_str(timestamp: int) -> str:
   # Auto-handle milliseconds
    if timestamp > 10**11:  # anything past year ~5138 in seconds
        timestamp //= 1000

    SECONDS_PER_MINUTE = 60
    SECONDS_PER_HOUR = 3600
    SECONDS_PER_DAY = 86400

    days = timestamp // SECONDS_PER_DAY
    seconds_remaining = timestamp % SECONDS_PER_DAY

    hour = seconds_remaining // SECONDS_PER_HOUR
    seconds_remaining %= SECONDS_PER_HOUR
    minute = seconds_remaining // SECONDS_PER_MINUTE
    second = seconds_remaining % SECONDS_PER_MINUTE

    year = 1970
    month = 1
    day = 1

    def is_leap(y):
        return y % 4 == 0 and (y % 100 != 0 or y % 400 == 0)

    days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    # Years
    while True:
        year_days = 366 if is_leap(year) else 365
        if days >= year_days:
            days -= year_days
            year += 1
        else:
            break

    # Months
    for i in range(12):
        dim = days_in_month[i]
        if i == 1 and is_leap(year):
            dim += 1
        if days >= dim:
            days -= dim
            month += 1
        else:
            break

    day += days
    z = f"{year:04d}-{month:02d}-{day:02d} {hour:02d}:{minute:02d}:{second:02d}"
    return z

def log(s:str):
    if logging:
        print(s)

def acc_by_rid(rid:str,tag:str):
    log("getting account by riot id")
    response = requests.get(f"{RIOT}/riot/account/v1/accounts/by-riot-id/{quote(rid)}/{tag}?api_key={API_KEY}")
    if response.status_code == 200:
        return(list(response.json().values()))
    else:
        return(f"Request failed with status code {response.status_code}")

def games_by_puuid(puuid:str):
    log("attempting to get games by puuid")
    s = f"{RIOT}/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count=20&api_key={API_KEY}"
    response = requests.get(s)
    if response.status_code == 200:
        log("success")
        return(response.json())
    else:
        log("failed")
        return(f"Request failed with status code {response.status_code}")

def text_parse(text:str):
    j = json.dumps(text,sort_keys=True)
    return
       
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
        log(f"Text successfully written to {filepath}")
    except Exception as e:
        log(f"An error occurred: {e}")

def  match_info(mid:str):
    log("attempting to get match info")
    response = requests.get(f"{RIOT}/lol/match/v5/matches/{mid}?api_key={API_KEY}")
    if response.status_code == 200:
        r = response.text
        log(f"success!")
        return r
    else:
        log("failure")
        return(f"Request failed with status code {response.status_code}")  

def listDispChoose(l:list):
    n = 1
    for choice in l:
        n+=1
        print(f"{n}:{choice}")
    try:
        selection = int(input("Select an option:"))
    except:
        selection = 0
    return(l[selection])

def get_acc_by_name(name:str,suffix:str):
    log("getting account by name")
    return acc(acc_by_rid(name,suffix))
        
def get_games_by_name(name:str,suffix:str):
    log("getting games by name")
    x = get_acc_by_name(name,suffix)
    return x.get_games()

def key_value_paths(data):
    results = []

    def walk(obj, path=""):
        if isinstance(obj, dict):
            for k, v in obj.items():
                new_path = f"{path}.{k}" if path else k
                if isinstance(v, (dict, list)):
                    walk(v, new_path)
                else:
                    results.append([new_path, v])
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                new_path = f"{path}[{i}]"
                if isinstance(item, (dict, list)):
                    walk(item, new_path)
                # primitives in lists have no keys → ignored

    walk(data)
    return results

def write_strings_to_file(strings,fn:str):
    with open(f"{fn}.txt", "w", encoding="utf-8") as f:
        for s in strings:
            f.write(f"{s}\n")
         
q = []                    
def analyze_matches(matches:list):
    out2 = []
    
    for match in matches:
        out = []
        
        j = json.loads(match_info(match))["info"]

        out.append(j["gameId"])
        out.append(j["gameMode"])
        out.append(time_to_str(j["gameCreation"]))
        jp = j["participants"]
        for x in range(0,len(jp)):
            out4 = []
            out5 = []
            #log(f"gathering player #{x} info")
            out3 = []
            p = jp[x]
            out4.append(p["riotIdGameName"])
            #out3.append(p["riotIdTagline"])
            out4.append(p["championName"])
            for y in range(1,7):
                #log(f"[^]{y}")
                m = p[f"playerAugment{y}"]
                out3.append(m)
                
            out4.append(out3)
            q.append(out3)
            out.append(out4)
        
        out2.append(out)
    return out2

def make_keypath_file(gameList:list):
    log("making keypath file...")
    j = json.loads(match_info(listDispChoose(gameList)))
    out = []
    for x in key_value_paths(j):
        out.append(x)
    write_strings_to_file(out,"keypaths")

def get_augments_by_id(id_list, json_path="augments.json"):
    if len(id_list) != 6:
        raise ValueError("id_list must contain exactly 6 integers")
    class TheID:
        a = id_list[0]
        b = id_list[1]
        c = id_list[2]
        d = id_list[3]
        e = id_list[4]
        f = id_list[5]
    out = [[],[],[],[],[],[]]
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        for x,y in data.items():
            for z in y:
                aug = [
                        z["name"],
                        z["id"],
                        z["rarity"]
                        ]
                match z["id"]:
                    case TheID.a:
                        out[0] = aug
                    case TheID.b:
                        out[1] = aug
                    case TheID.c:
                        out[2] = aug
                    case TheID.d:
                        out[3] = aug
                    case TheID.e:
                        out[4] = aug
                    case TheID.f:
                        out[5] = aug
    return out

def save_list_to_text(filename_str, data_list):
    # Remove extension if one exists
    base_name = os.path.splitext(filename_str)[0]
    file_name = f"{base_name}.txt"

    # Check if file already exists
    if os.path.exists(file_name):
        return  # Do nothing

    # Write list contents to file
    with open(file_name, "w", encoding="utf-8") as f:
        for item in data_list:
            f.write(f"{item}\n")
    
myGames = get_games_by_name("Crackpipe Perez","NA1")
curatedMatches = analyze_matches(myGames)
write_strings_to_file(curatedMatches,"gamesInfo")
#make_keypath_file(myGames)
t = []
for x in curatedMatches:
    t.append(x)
    for y in x:
        if isinstance(y,list):
            t.append(f"{y[:2]} {get_augments_by_id(y[2])}")
write_strings_to_file(t,"augmentHistory")
#log(get_augments_by_id(q[0]))


"""
for x in myGames:
    game = match_info(x)
    y = game
    saves+=1
    save_game(json.dumps(y,indent=3),saves)
    gameInfo.append(y)
"""