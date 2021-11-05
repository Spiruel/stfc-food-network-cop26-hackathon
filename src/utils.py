import config
import requests
import pandas as pd
from io import BytesIO
import shapely
import geopandas as gpd
import streamlit as st

india_gdf = gpd.read_file(config.INDIAN_DISTRICT_SHAPEFILE)

def get_weather_city(city):
    """
    Get the weather for a city
    """
    url = 'http://api.openweathermap.org/data/2.5/weather'
    params = {'APPID': config.OPENWEATHER_KEY, 'q': city, 'units': 'metric'}
    response = requests.get(url, params=params)
    weather = response.json()
    return weather

def get_weather_loc(lon, lat):
    """
    Get the weather for a location
    """
    url = 'http://api.openweathermap.org/data/2.5/weather'
    params = {'APPID': config.OPENWEATHER_KEY, 'lat': lat, 'lon': lon, 'units': 'metric', 'date': d}
    response = requests.get(url, params=params)
    weather = response.json()
    return weather

def get_weather_forecast(city, days=16):
    """
    Get the weather forecast for a city
    """
    url = 'http://api.openweathermap.org/data/2.5/forecast'
    params = {'APPID': config.OPENWEATHER_KEY, 'q': city, 'units': 'metric', 'cnt': days}
    response = requests.get(url, params=params)
    weather = response.json()
    return weather

def get_weather_forecast_loc(lon, lat, days=16):
    """
    Get the weather forecast for a location
    """
    url = 'http://api.openweathermap.org/data/2.5/forecast'
    params = {'APPID': config.OPENWEATHER_KEY, 'lat': lat, 'lon': lon, 'units': 'metric', 'cnt': days}
    response = requests.get(url, params=params)
    weather = response.json()
    return weather

@st.cache()
def data_gov_in_req(id):
    """
    Get data from data.gov.in
    """
    url = f'https://api.data.gov.in/resource/{id}'

    api_params = {
        'api-key': config.DATAGOV_IN_KEY,
        'format': 'csv', # The output format for the data (XML or CSV)
        'limit': 9999999 # The maximum number of rows to return
    }

    response = requests.api.get(url, api_params)
    print(response.content, url, api_params)
    df = pd.read_csv(BytesIO(response.content))

    return df

def get_district(lat, lon):
    """
    Checks a given coord and returns district if within India
    """
    point = shapely.geometry.Point(lon, lat)

    districts = india_gdf.distname.loc[india_gdf.geometry.contains(point)]
    if len(districts) > 0:
        return districts.iloc[0]
    else:
        return 'unknown'

def get_state(lat, lon):
    """
    Checks a given coord and returns state if within India
    """
    point = shapely.geometry.Point(lon, lat)

    districts = india_gdf.statename.loc[india_gdf.geometry.contains(point)]
    if len(districts) > 0:
        return districts.iloc[0]
    else:
        return 'unknown'

def get_markets(district):
    district_key = district.title().replace(" ","")
    if district_key in config.markets:
        return config.markets[district_key]
    else:
        return []