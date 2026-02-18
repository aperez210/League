motd = "#gamer#"
output = ""

import utils as ut
loop = True
games = []
def stop():
    return ["stopping..."]

def game_get(s:str):
    print(f"gettin games for user {s}")
    x = ut.get_games_by_name(s)
    y = ut.analyze_matches(x)
    z = ut.curated_to_list(y)
    fileName = input("filename: ")
    ut.write_strings_to_file(z,fileName)
    return z

while loop:
    command = input(f"{motd}:")
    commands = command.split(" ")
    
    response = []
    n = []
    string = ""
    match commands[0]:
        case "stop":
            n = stop()
            response.append(n[0])
            loop = False
        case "getGameList":
            o = commands[1:]
            if o:
                response.append(game_get(" ".join(o)))
            else:
                print(f"something")
    print(f"{response}\n")