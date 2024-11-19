from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import fastf1
import pandas as pd
from typing import List
from pydantic import BaseModel
import os
from fastf1.ergast import Ergast
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colormaps
from matplotlib.collections import LineCollection



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

class Race(BaseModel):
    round: int
    raceName: str
    circuitName: str
    date: str
    time: str
    country: str
    flagUrl: str

@app.get("/api/standings", response_model=List[Driver])
async def get_driver_standings():
    try:
        
        session = fastf1.get_session(2024, 'Australia', 'R')
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
    

@app.get("/api/standings/constructors", response_model=List[Constructor])
async def get_constructor_standings():
    try:
        session = fastf1.get_session(2024, 'Australia', 'R')
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

@app.get("/api/schedule", response_model=List[Race])
async def get_race_schedule():
    try:
        print("Fetching schedule...")  # Debug log
        schedule = fastf1.get_event_schedule(2024)
        schedule.load()
        races = []
        
        # Country code mapping
        country_codes = {
            'Bahrain': 'bh',
            'Saudi Arabia': 'sa',
            'Australia': 'au',
            'Japan': 'jp',
            'China': 'cn',
            'United States': 'us',
            'Italy': 'it',
            'Monaco': 'mc',
            'Canada': 'ca',
            'Spain': 'es',
            'Austria': 'at',
            'United Kingdom': 'gb',
            'Hungary': 'hu',
            'Belgium': 'be',
            'Netherlands': 'nl',
            'Singapore': 'sg',
            'Mexico': 'mx',
            'Brazil': 'br',
            'United Arab Emirates': 'ae',
            'Qatar': 'qa',
            'Las Vegas': 'us',
            'Miami': 'us',
        }
        
        for race in schedule:
            country = race['Country']['Location']['EventName']
            country_code = country_codes.get(country, '').lower()
            if not country_code:
                print(f"Warning: No country code found for {country}")
                country_code = 'unknown'
                
            races.append(Race(
                round=int(race['round']),
                raceName=race['raceName'],
                circuitName=race['Circuit']['circuitName'],
                date=race['date'],
                time=race['time'] if 'time' in race else "14:00:00",
                country=country,
                flagUrl=f"https://flagcdn.com/w80/{country_code}.png"
            ))
        
        print(f"Returning {len(races)} races")  # Debug log
        return races

    except Exception as e:
        print(f"Error in get_race_schedule: {str(e)}")
        print(f"Error type: {type(e)}")
        import traceback
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

async def get_gear_shifts():
    #Get gear shifts on track 

    session = fastf1.get_session(2024, 1, 'R')
    session.load()

    lap = session.lap.pickfastest()
    tel = lap.get_telemetry()


    #Prepare the graph and values for plotting
    x = np.array(tel['X'].values)
    y = np.array(tel['Y'].values)

    points = np.array([x,y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:1], points[1:]], axis =1)
    gear = tel['nGear'].to_numpy().astype(float)

    #Createa a line collection 

    cmap = colormaps['Paired']
    lc_comp = LineCollection(segments, norm = plt.Normalize(1, cmap.N+1), cmap=cmap)
    lc_comp.set_array(gear)
    lc_comp.set_linewidth(4)

    #Create the plot 

    plt.gca().add_collection(lc_comp)
    plt.axis('equal')
    plt.trick_params(labelleft = False, left = False, lablebottom = False, bottom = False)

    title = plt.suptitle(
        f"Fastest Lap Gear Shift Visualization"
        f{lap['Driver']} - {session.event['EventName']} {session.event.year}
    )

    #Add a collorbar to the plot. Shift the colorbar ticks by +0.5 so that they are centered for each color segment 
    
    cbar = plt.colorbar(mappable=lc_comp, label="Gear",
                        boundaries=np.arange(1, 10))
    cbar.set_ticks(np.arange(1.5, 9.5))
    cbar.set_ticklabels(np.arange(1, 9))

    plt.show()