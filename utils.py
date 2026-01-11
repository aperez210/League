import os
import Ritool as rt
import json as js

logging = True


class acc:
    puuid = ""
    gameName = ""
    tagLine = ""
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
        log(f"{self.puuid}")
        return rt.games_by_puuid(self.puuid)

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

def text_parse(text:str):
    j = js.dumps(text,sort_keys=True)
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

def get_acc_by_name(name:str):
    log("getting account by name")
    nameTag = name[:name.index("#")],name[name.index("#")+1:]
    #log(f"[*]{nameTag}")
    return acc(rt.acc_by_rid(nameTag[0],nameTag[1]))
        
def get_games_by_name(name:str):
    log("getting games by name")
    x = get_acc_by_name(name)
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

import os

def write_strings_to_file(strings, fn: str):
    os.makedirs("data", exist_ok=True)
    path = os.path.join("data", f"{fn}.txt")

    with open(path, "w", encoding="utf-8") as f:
        for s in strings:
            if len(s[0]) == 1:
                f.write(f"{s}\n")
         
q = []                    
def analyze_matches(matches:list):
    game_info_list = []
    
    for match in matches:
        out = []
        match_info = js.loads(rt.match_info(match))['info']
        participants_info = match_info["participants"]
        
        for x in range(0,len(participants_info)):
            players_list = []
            players_augments = []
            player_x = participants_info[x]
            players_list.append(player_x[f"riotIdGameName"])
            #players_list(player_x["riotIdTagline"])
            players_list.append(player_x["championName"])
            
            for y in range(1,7):
                m = player_x[f"playerAugment{y}"]
                players_augments.append(m)
                
            players_list.append(players_augments)
            q.append(players_augments)
            out.append(players_list)
        game_info_list.append(out)
    """for x in range(len(game_info_list)):
        log(f"{game_info_list[x][0:1]}")
    """
    return game_info_list

def make_keypath_file(gameList:list):
    log("making keypath file...")
    j = js.loads(rt.match_info(listDispChoose(gameList)))
    out = []
    for x in key_value_paths(j):
        out.append(x)
    write_strings_to_file(out,"keypaths")

def get_augments_by_id(id_list, json_path="augments.json"):
    if len(id_list) != 6:
        raise ValueError("id_list must contain exactly 6 integers")
    class TheBoys:
        Alex = id_list[0]
        ToastedPigeon38 = id_list[1]
        Jalse = id_list[2]
        FlameFreeze = id_list[3]
        Andrew2831 = id_list[4]
        Isaac2000 = id_list[5]
    my_tummy = [[],[],[],[],[],[]]
    with open(json_path, "r", encoding="utf-8") as f:
        bag_of_candy = js.load(f).items()
        for twix,snickers in bag_of_candy:
            for peanut in snickers:
                best_nut = peanut["id"]
                yummy = [
                        peanut["name"],
                        best_nut,
                        peanut["rarity"]
                        ]
                match best_nut:
                    case TheBoys.Alex:
                        my_tummy[0] = yummy
                    case TheBoys.ToastedPigeon38:
                        my_tummy[1] = yummy
                    case TheBoys.Jalse:
                        my_tummy[2] = yummy
                    case TheBoys.FlameFreeze:
                        my_tummy[3] = yummy
                    case TheBoys.Andrew2831:
                        my_tummy[4] = yummy
                    case TheBoys.Isaac2000:
                        my_tummy[5] = yummy
    return my_tummy

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
            
def curated_to_list(curatedMatches):
    t = []
    for x in curatedMatches:
        t.append(x)
        for y in x:
            if isinstance(y,list):
                t.append(f"{y[:2]} {get_augments_by_id(y[2])}")
    return t
    

