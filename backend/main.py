import os

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware # Import this
from dotenv import load_dotenv
import utils as ut
from telemetry import collect_riot_telemetry

load_dotenv()

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


@app.get("/telemetry/{riotID}")
async def get_telemetry(
    riotID: str,
    maxMatches: int = Query(default=500, ge=1, le=1000),
):
    api_key = os.getenv("ARENA_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="Missing ARENA_KEY environment variable")

    try:
        payload = collect_riot_telemetry(
            riot_id=riotID,
            api_key=api_key,
            max_matches=maxMatches,
            augments_path="augments.json",
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Telemetry collection failed: {exc}") from exc

    return payload


@app.get("/telemetry/{riotID}/summary")
async def get_telemetry_summary(
    riotID: str,
    maxMatches: int = Query(default=500, ge=1, le=1000),
):
    full = await get_telemetry(riotID=riotID, maxMatches=maxMatches)
    return full["summary"]

# myGames = ut.get_games_by_name("Crackpipe Perez#NA1")
# curatedMatches = ut.analyze_matches(myGames)
# ut.write_strings_to_file(curatedMatches,"gamesInfo")
# t = ut.curated_to_list(curatedMatches)
# ut.write_strings_to_file(t,"augmentHistory")
