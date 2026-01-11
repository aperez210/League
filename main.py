import utils as ut
myGames = ut.get_games_by_name("Crackpipe Perez","NA1")
curatedMatches = ut.analyze_matches(myGames)
ut.write_strings_to_file(curatedMatches,"gamesInfo")
t = ut.curated_to_list(curatedMatches)
ut.write_strings_to_file(t,"augmentHistory")
