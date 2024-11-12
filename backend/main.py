from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import fastf1
import pandas as pd
from typing import List
from pydantic import BaseModel
import os
from fastf1.ergast import Ergast

app = FastAPI()

# CORS middleware setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cache setup
CACHE_DIR = os.path.join(os.path.dirname(__file__), 'cache')
os.makedirs(CACHE_DIR, exist_ok=True)
fastf1.Cache.enable_cache(CACHE_DIR)

class Driver(BaseModel):
    position: int
    driver_number: str
    full_name: str
    points: float

class Constructor(BaseModel):
    position: int
    name: str
    points: float

@app.get("/api/standings", response_model=List[Driver])
async def get_driver_standings():
    try:
        ergast = Ergast()
        races = ergast.get_race_schedule(2022)  # Races in year 2022
        results = []

        for rnd, race in race['raceName'].items():
            temp =ergast.get_race_schedule(2024, rnd = rnd+1) #get results. We use rnd+1 because rnd is 1-indexed
            temp = temp.content[0]

            #get sprint results
            sprint = ergast.get_sprint_results(2024, rnd = rnd+1)
            if sprint.content and sprint.description['round'][0] == rnd+1:
                temp = pd.merge(temp, sprint.content[0], on = 'DriverNumber', how = 'left')

        #https://docs.fastf1.dev/gen_modules/examples_gallery/plot_results_tracker.html

        """
        session = fastf1.get_session(2024, 1, 'R')
        session.load()
        
        # Get driver results
        results = []
        for idx, driver in enumerate(session.results.itertuples(), 1):
            results.append(Driver(
                position=idx,
                driver_number=str(driver.DriverNumber),
                full_name=f"{driver.FirstName} {driver.LastName}",
                points=float(driver.Points)
            ))
        
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    """

@app.get("/api/standings/constructors", response_model=List[Constructor])
async def get_constructor_standings():
    try:
        session = fastf1.get_session(2024, 1, 'R')
        session.load()
        
        # Process constructor standings
        teams_data = {}
        for _, row in session.results.iterrows():
            team_name = row['TeamName']
            points = float(row['Points'])
            if team_name in teams_data:
                teams_data[team_name] += points
            else:
                teams_data[team_name] = points
        
        # Sort teams by points
        sorted_teams = sorted(teams_data.items(), key=lambda x: x[1], reverse=True)
        
        # Create response
        results = [
            Constructor(
                position=idx + 1,
                name=team_name,
                points=points
            )
            for idx, (team_name, points) in enumerate(sorted_teams)
        ]
        
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))