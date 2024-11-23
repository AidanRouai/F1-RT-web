from fastapi import FastAPI, HTTPException, Query
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
import io
from fastapi.responses import StreamingResponse
import logging


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
        ergast = Ergast()
        races = ergast.get_race_schedule(2022)  # Races in year 2022
        results = []

        # For each race in the season
        for rnd, race in races['raceName'].items():
            # Get results. Note that we use the round no. + 1, because the round no.
            # starts from one (1) instead of zero (0)
            temp = ergast.get_race_results(season=2022, round=rnd + 1)
            temp = temp.content[0]

            # If there is a sprint, get the results as well
            sprint = ergast.get_sprint_results(season=2022, round=rnd + 1)
            if sprint.content and sprint.description['round'][0] == rnd + 1:
                temp = pd.merge(temp, sprint.content[0], on='driverCode', how='left')
                # Add sprint points and race points to get the total
                temp['points'] = temp['points_x'] + temp['points_y']
                temp.drop(columns=['points_x', 'points_y'], inplace=True)

            # Add round no. and grand prix name
            temp['round'] = rnd + 1
            temp['race'] = race.removesuffix(' Grand Prix')
            temp = temp[['round', 'race', 'driverCode', 'points']]  # Keep useful cols.
            results.append(temp)
    except Exception as e:
        logging.error(f"Error processing round {rnd + 1}: {e}")

        # Append all races into a single dataframe
        results = pd.concat(results)
        races = results['race'].drop_duplicates()

        # Create a list to store Driver objects
        driver_list = []

        for idx, driver in enumerate(results.itertuples(), 1):  
            driver_list.append(Driver(
                position=idx,
                driver_number=str(driver.driverCode),
                full_name=f"{driver.FirstName} {driver.LastName}",
                points=float(driver.Points)
            ))
        print(driver_list)
    try:
        return driver_list  # Return the list of Driver objects
    except Exception as e:
        logging.error(f"Error fetching driver standings: {e}")
        return []

    

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

@app.get("/api/race-schedule", response_model=List[Race])
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

@app.get("/api/gear-shifts")
async def get_gear_shifts(
    year: int = Query(..., description="Year of the event"),
    location: str = Query(..., description="Location of the event"),
    event_type: str = Query(..., description="Type of the event (R, Q, FP1, FP2, FP3)")
):
    # Get gear shifts on track 
    session = fastf1.get_session(year, location, event_type)
    session.load()

    lap = session.lap.pickfastest()
    tel = lap.get_telemetry()

    # Prepare the graph and values for plotting
    x = np.array(tel['X'].values)
    y = np.array(tel['Y'].values)

    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    gear = tel['nGear'].to_numpy().astype(float)

    # Create a line collection 
    cmap = colormaps['Paired']
    lc_comp = LineCollection(segments, norm=plt.Normalize(1, cmap.N+1), cmap=cmap)
    lc_comp.set_array(gear)
    lc_comp.set_linewidth(4)

    # Create the plot 
    plt.gca().add_collection(lc_comp)
    plt.axis('equal')
    plt.tick_params(labelleft=False, left=False, labelbottom=False, bottom=False)

    plt.suptitle(
        f"Fastest Lap Gear Shift Visualization\n"
        f"{lap['Driver']} - {session.event['EventName']} {session.event.year}"
    )

    cbar = plt.colorbar(mappable=lc_comp, label="Gear",
                        boundaries=np.arange(1, 10))
    cbar.set_ticks(np.arange(1.5, 9.5))
    cbar.set_ticklabels(np.arange(1, 9))

    # Save plot to a BytesIO object
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()

    return StreamingResponse(buf, media_type="image/png")

