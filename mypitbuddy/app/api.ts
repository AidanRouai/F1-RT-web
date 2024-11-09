const BASE_URL = "https://api.openf1.org/v1";

export interface Race {
    season: number;
    round: number;
    url: string;
    raceName: string;
    circuitId: string;
    circuitName: string;
}

export interface Driver {
    broadcast_name: number;
    driver_name: string;
    team_name: string;
    position: number;
    meeting_key: number;
    country_code: string;
    name_acronym: string;
    team_color: string;
}

export interface LiveTiming {
    date: string;
    driver_number: number;
    meeting_key: number;
    session_key: number;
    speed_i1: number;
    speed_i2: number;
    speed_fl: number;
    speed_st: number;
    sector_1_time: number;
    sector_2_time: number;
    sector_3_time: number;
    lap_time: number;
    car_status: string;
}

export interface Weather {
    air_temperature: number;
    date: string;
    humidity: number;
    track_temperature: number;
    meeting_key: number;
    rainfall: number;
}


export const f1Api = {
    async getDrivers(session_id?: number): Promise<Driver[]> {
        const url = session_id ? `${BASE_URL}/session/${session_id}/drivers` : `${BASE_URL}/drivers`;
        const response = await fetch(url);
        return response.json();
    },

    async getLiveTiming(session_id: number): Promise<LiveTiming[]> {
        const url = `${BASE_URL}/session/${session_id}/live/timing`;
        const response = await fetch(url);
        return response.json();
    },

    async getWeather(session_id: number): Promise<Weather> {
        const url = `${BASE_URL}/session/${session_id}/weather`;
        const response = await fetch(url);
        return response.json();
    },

    async getRaceSchedule(): Promise<Race[]> {
        const url = `${BASE_URL}/race-schedule`;
        const response = await fetch(url);
        return response.json();
    }

}