import config
import requests
import pandas as pd
from io import BytesIO
import shapely
import geopandas as gpd
import streamlit as st

import ee
import geemap
ee.Initialize()

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

    print(f'requested: {url}')
    response = requests.api.get(url, api_params)
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

@st.cache()
def gee_dl_features(lat, lon, area, yr):
    region = ee.Feature(ee.Geometry.Point([lon, lat]))

    mean_reducer = ee.Reducer.mean()

    bdod_mean = ee.Image("projects/soilgrids-isric/bdod_mean")
    cec_mean = ee.Image("projects/soilgrids-isric/cec_mean")
    cfvo_mean = ee.Image("projects/soilgrids-isric/cfvo_mean")
    clay_mean = ee.Image("projects/soilgrids-isric/clay_mean")
    nitrogen_mean = ee.Image("projects/soilgrids-isric/nitrogen_mean")
    ocd_mean = ee.Image("projects/soilgrids-isric/ocd_mean")
    ocs_mean = ee.Image("projects/soilgrids-isric/ocs_mean")
    phh2o_mean = ee.Image("projects/soilgrids-isric/phh2o_mean")
    sand_mean = ee.Image("projects/soilgrids-isric/sand_mean")
    silt_mean = ee.Image("projects/soilgrids-isric/silt_mean")
    soc_mean = ee.Image("projects/soilgrids-isric/soc_mean")

    era5_monthly = ee.ImageCollection("ECMWF/ERA5_LAND/MONTHLY") 

    soil_feats = {'bulk density': bdod_mean,
                'cation exchange capacity': cec_mean,
                'coarse fragments': cfvo_mean,
                'clay': clay_mean,
                'total nitrogen': nitrogen_mean,
                'organic carbon density': ocd_mean,
                'organic carbon stock': ocs_mean,
                'pH in H2O': phh2o_mean,
                'sand': sand_mean,
                'silt': silt_mean,
                'soil organic carbon': soc_mean}

    soil_dfs = []
    for feat in soil_feats:
        image = soil_feats[feat]
        # Use the combined reducer to get the mean and SD of the image.
        soil_stats = image.reduceRegion(**{
        'reducer': mean_reducer,
        'geometry': region.geometry(),
        'scale':30
        })

        soil_stats_df = pd.DataFrame(soil_stats.getInfo(), index=[0])
        if soil_stats_df.isnull().values.any():
            return 0
        soil_dfs.append(soil_stats_df)

    era5_dfs = []

    for m in range(1,13):
        #print(y, m)

        era5_monthly_sel = era5_monthly \
                .filter(ee.Filter.calendarRange(yr,yr,'year')) \
                .filter(ee.Filter.calendarRange(1,1,'month')).first()


        # Use the combined reducer to get the mean and SD of the image.
        era5_stats = era5_monthly_sel.reduceRegion(**{
        'reducer': mean_reducer,
        'geometry': region.geometry(),
        'scale': 100
        })

        era5_stats_df = pd.DataFrame(era5_stats.getInfo(), index=[0])
        if era5_stats_df.isnull().values.any():
            return 1

        era5_stats_df.columns += f'_{m}'

        era5_dfs.append(era5_stats_df)

    soil_data_df = pd.concat(soil_dfs, axis=1)
    era5_data_df = pd.concat(era5_dfs, axis=1)

    in_df = pd.DataFrame({'Area (HA)':area}, index=[0])
    joined = pd.concat([in_df, soil_data_df, era5_data_df], axis=1)[['Area (HA)'] + config.SOIL_FEATS + config.ERA5_FEATS]

    return joined