import requests
from objecthandler import FileHandler, WeatherFetcher, WeatherService
from flask import Flask, jsonify, request

app = Flask(__name__)

Api_key = "a0fd3e6ef327fb3716f7d453937ac104"
file_handler = FileHandler()
fetcher = WeatherFetcher(Api_key)
service = WeatherService(Api_key)

@app.route("/weather", methods=["GET"])
def get_weather():
    city = request.args.get("city")

    if not city:
        return jsonify({"error": "City parameter is required"}), 400

    # weatherinfo = fetcher.fetch_weather(city)

    # if not weatherinfo:
    #     return jsonify({"error": "Failed to fetch weather data"}), 500

    # file_handler.save_to_json(weatherinfo)
    # file_handler.save_to_csv([weatherinfo])
    # return jsonify(weatherinfo), 200
    
    result, status = service.get_weather(city)

    return jsonify(result), status
    
if __name__ == "__main__":
    app.run(debug=True)