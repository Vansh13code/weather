import asyncio
import json
import aiohttp
import requests


API_URL = "https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude={part}&appid={API_KEY}"
API_KEY = "a0fd3e6ef327fb3716f7d453937ac104"

async def fetch_weather_async(session, city):
    url = f"{API_URL}?q={city}&appid={API_KEY}"
    async with session.get(url) as response:
        return await response.json()
    
    try:
      async with session.get(url) as response:
        data = await response.json()
        return {
            "city": city,
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "condition": data["weather"][0]["description"]
        }
    except Exception as e:
        print(f"Error fetching data for {city}: {e}")
        return None
      
async def main_async(cities):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_weather_async(session, city) for city in cities]
        results = await asyncio.gather(*tasks)
        print(json.dumps(results, indent=2))
        
if __name__ == "__main__":
    cities = ["London", "Paris", "Tokyo"]
    asyncio.run(main_async(cities))
    aiohttp.request()
