import requests
import json
import csv
import asyncio
import aiohttp

class WeatherFetcher:
    def __init__(self, api_key):
        self.api_key = api_key

    def fetch_weather(self, city):
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.api_key}"
        response = requests.get(url)

        if response.status_code != 200:
            return None

        data = response.json()

        return {
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "condition": data["weather"][0]["main"]
        }


class FileHandler:
    def save_to_json(self, data, filename="weather.json"):
        with open(filename, "w") as f:
            json.dump(data, f, indent=2)

    def save_to_csv(self, data, filename="weather.csv"):
        if not data:
            return
        with open(filename, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)


class WeatherService:
    def __init__(self, api_key):
        self.fetcher = WeatherFetcher(api_key)
        self.file_handler = FileHandler()
        self.api_key = api_key

    def get_weather(self, city):
        data = self.fetcher.fetch_weather(city)

        if not data:
            return {"error": "Failed to fetch weather data"}, 500

        self.file_handler.save_to_json(data)
        self.file_handler.save_to_csv([data])

        return data, 200

    async def fetch_weather_async(self, session, city):
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.api_key}"
        async with session.get(url) as res:
            if res.status == 200:
                data = await res.json()
                return {
                    "city": data["name"],
                    "temperature": data["main"]["temp"],
                    "humidity": data["main"]["humidity"],
                    "condition": data["weather"][0]["main"]
                }
            else:
                return {"error": f"Failed for {city}"}

    async def get_multiple_weather(self, cities):
        async with aiohttp.ClientSession() as session:
            tasks = [self.fetch_weather_async(session, city) for city in cities]
            results = await asyncio.gather(*tasks)

            self.file_handler.save_to_json(results)
            self.file_handler.save_to_csv(results)

            return results