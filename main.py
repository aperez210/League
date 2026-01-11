import utils as ut
t = []
myGames = ut.get_games_by_name("Crackpipe Perez","NA1")
curatedMatches = ut.analyze_matches(myGames)
for m in curatedMatches:
    print(f"[$]{m}")
ut.write_strings_to_file(curatedMatches,"gamesInfo")
for x in curatedMatches:
    t.append(x)
    for y in x:
        if isinstance(y,list):
            t.append(f"{y[:2]} {ut.get_augments_by_id(y[2])}")
ut.write_strings_to_file(t,"augmentHistory")
