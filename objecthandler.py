import requests
import json
import csv

class WeatherFetcher:
    def __init__(self, api_key):
        self.api_key = api_key

    def fetch_weather(self, city):
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.api_key}"
            response = requests.get(url)

            if response.status_code != 200:
                return None

            data = response.json()

            return {
                "city": data["name"],
                "temperature": data["main"]["temp"],
                "humidity": data["main"]["humidity"],
                "condition": data["weather"][0]["description"]
            }

        except Exception as e:
            print(f"Error fetching data for {city}: {e}")
            return None


class FileHandler:
    def save_to_csv(self, data, filename="weather.csv"):
        if not data:
            return

        with open(filename, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)

    def save_to_json(self, data, filename="weather.json"):
        try:
            with open(filename, "r") as f:
                existing_data = json.load(f)
        except:
            existing_data = []

        existing_data.append(data)

        with open(filename, "a") as f:
            json.dump(existing_data, f, indent=2)


class WeatherService:
    def __init__(self, api_key):
        self.fetcher = WeatherFetcher(api_key)
        self.file_handler = FileHandler()

    def get_weather(self, city):
        data = self.fetcher.fetch_weather(city)

        if not data:
            return {"error": "Failed to fetch weather data"}, 500

        self.file_handler.save_to_json(data)
        self.file_handler.save_to_csv([data])

        return data, 200