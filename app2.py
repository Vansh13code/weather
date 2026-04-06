from flask import Flask, jsonify, request
from objecthandler import WeatherService
import asyncio

app = Flask(__name__)

Api_key = "a0fd3e6ef327fb3716f7d453937ac104"

service = WeatherService(Api_key)


@app.route("/weather", methods=["GET"])
def get_weather():
    city = request.args.get("city")

    if not city:
        return jsonify({"error": "City parameter is required"}), 400

    result, status = service.get_weather(city)

    return jsonify(result), status

@app.route("/weather/many", methods=["POST"])
def get_many_weather():
    data = request.get_json()

    if not data or "cities" not in data:
        return jsonify({"error": "Cities list is required"}), 400

    cities = data["cities"]

    results = asyncio.run(service.get_multiple_weather(cities))

    return jsonify({
        "count": len(results),
        "data": results
    }), 200


if __name__ == "__main__":
    app.run(debug=True)