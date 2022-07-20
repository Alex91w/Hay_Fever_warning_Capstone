import requests
import boto3
from datetime import datetime
import os

WEATHER_API_URL = 'https://api.brightsky.dev/weather?lat=53.55&lon=9.99&date=2022-07-18'
weather_table_name = os.environ["WEATHER_DATA"]

dynamodb_resource = boto3.resource("dynamodb")
weather_table = dynamodb_resource.Table(weather_table_name)


def load_weather_data():
    print("start loading weather data")
    response = requests.get(WEATHER_API_URL)
    return response.json()["data"]

def map_weather_data(weather_api_data):
    result = []
    today = datetime.now()
    for weather_item in weather_api_data:
        result.append({
            "id": weather_item["source_id"],
            "timestamp": weather_item["timestamp"],
            "windspeed": weather_item["wind_speed"],
            "windgust": weather_item["wind_gust_speed"],
            "date": today.strftime("%Y-%m-%d %H:%M:%S")
        })
    return result

def save_weather_data(weatherdata):
    for weather in weatherdata:
        weather_table.put_item(Item = weather)

def handle(event, context):
    weather_api_data = load_weather_data()
    mapped_data = map_weather_data(weather_api_data)
    save_weather_data(mapped_data)

if __name__ == "__main__":
    handle({},{})