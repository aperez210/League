from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware # Import this
import utils as ut

app = FastAPI()

# Add this block to allow your React app to speak to FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, replace "*" with ["http://localhost:5173"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/games/{riotID}")
async def getGames(riotID: str):
    # Note: If the ID comes in as "Name%23Tag", FastAPI usually decodes it automatically.
    # If you run into issues, print(riotID) here to check.
    games = ut.get_games_by_name(riotID)
    curatedMatches = ut.analyze_matches(games)
    return ut.curated_to_list(curatedMatches)

# myGames = ut.get_games_by_name("Crackpipe Perez#NA1")
# curatedMatches = ut.analyze_matches(myGames)
# ut.write_strings_to_file(curatedMatches,"gamesInfo")
# t = ut.curated_to_list(curatedMatches)
# ut.write_strings_to_file(t,"augmentHistory")
