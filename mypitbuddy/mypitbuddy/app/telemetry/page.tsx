'use client';
import React, { useState } from 'react';

const GearShiftsPlot = () => {
    const [year, setYear] = useState(2024);
    const [location, setLocation] = useState('Australia');
    const [eventType, setEventType] = useState('R');
    const [imageSrc, setImageSrc] = useState('');

    const fetchPlot = () => {
        fetch(`/api/gear-shifts?year=${year}&location=${location}&event_type=${eventType}`)
            .then(response => response.blob())
            .then(blob => {
                const url = URL.createObjectURL(blob);
                setImageSrc(url);
            })
            .catch(error => console.error('Error fetching gear shifts plot:', error));
    };

    return (
        <div>
            <h1>Gear Shifts Plot</h1>
            <div>
                <label>
                    Year:
                    <select value={year} onChange={e => setYear(parseInt(e.target.value))}>
                        <option value="2024">2024</option>
                        <option value="2023">2023</option>
                        <option value="2022">2022</option>
                        <option value="2021">2021</option>
                        <option value="2020">2020</option>
                        <option value="2019">2019</option>
                        <option value="2018">2018</option>
                    </select>
                </label>
                <label>
                    Location:
                    <select value={location} onChange={e => setLocation(e.target.value)}>
                        <option value="Australia">Australia</option>
                        <option value="Bahrain">Bahrain</option>
                        {/* Add more locations as needed */}
                    </select>
                </label>
                <label>
                    Event Type:
                    <select value={eventType} onChange={e => setEventType(e.target.value)}>
                        <option value="R">Race</option>
                        <option value="Q">Qualifying</option>
                        <option value="FP1">FP1</option>
                        <option value="FP2">FP2</option>
                        <option value="FP3">FP3</option>
                    </select>
                </label>
                <button onClick={fetchPlot}>Fetch Plot</button>
            </div>
            {imageSrc ? <img src={imageSrc} alt="Gear Shifts Plot" /> : <p>Select options and click 'Fetch Plot'</p>}
        </div>
    );
};

export default GearShiftsPlot;
