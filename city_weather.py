#!/usr/bin/env python
# coding: utf-8

# In[21]:


import pandas as pd
import json
import requests
import os 
import polars as pl

city_name = 'Warsaw'
units = 'metric' # C 'metrics',  F 'imperial', K 'standartd' default
lang = 'en' # Field 'description' wil be translated 'pl'
# date =2025-1-22 #Date for which summary is generated in the format YYYY-MM-DD
# weather_overview - AI generated weather overview for the requested date

API_KEY=os.environ["api_key"]
api_url = f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&APPID={API_KEY}&units={units}&lang={lang}'

try:
    response = requests.get(api_url)
    data = response.json()
    #print(data)
except (ConnectionError, Timeout, TooManyRedirects) as e:
    print(f'Error: {e}')

# response = requests.get(api_url)
# data = response.json()
city = pd.json_normalize(data)

list=['name',
      'cod',
      'coord.lon', 
      'coord.lat', 
      'main.temp', 
      'main.feels_like',
      'main.temp_min',
      'main.temp_max',
      'main.pressure',
      'main.humidity',
      'wind.speed',
      'timezone',
      'clouds.all',
      'visibility']

City_weather = city[list]
City_weather= City_weather.rename(columns={'name': 'City_Name', 
                      'cod': 'City_Cod', 
                      'coord.lon': 'Longitude', 
                      'coord.lat': 'Latitude', 
                      'main.temp': 'Temperature_Celsius', 
                      'main.feels_like':'Temperature_Feels_Like',
                      'main.temp_min': 'Temperature_Min', 
                      'main.temp_max': 'Temperature_Max', 
                      'main.pressure': 'Pressure', 
                      'main.humidity': 'Humidity',
                      'wind.speed': 'Wind_Speed', 
                      'timezone': 'Timezone', 
                      'clouds.all': 'Clouds',
                      'visibility': 'Visibility' })

# City_weather['Date'] = datetime.today()
City_weather['Timestamp'] = pd.to_datetime('now')

if not os.path.isfile(r'data/city_weather.csv'):
    City_weather.to_csv(r'data/city_weather.csv', header='column_names')
else:
    City_weather.to_csv(r'data/city_weather.csv'', mode='a', header=False)
