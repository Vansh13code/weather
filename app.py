import csv
import requests
from flask import Flask,jsonify,request
import json
app=Flask(__name__)
Api_key="a0fd3e6ef327fb3716f7d453937ac104"
@app.route("/weather",methods=["GET"])
def get_weather():
    city=request.args.get("city")
    if not city:
        return jsonify({"error":"City parameter is required"}),400
    url=f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={Api_key}"
    response=requests.get(url)
    if response.status_code==200:
        data=response.json()
        weatherinfo={
            "city":data["name"],
            "temperature":data["main"]["temp"],
            #"description":data["weather"][0]["description"],
            "humidity":data["main"]["humidity"],
            "Condition":data["weather"][0]["main"]
        }
        with open("weather.json","w") as f:
            json.dump(weatherinfo,f)
        with     open("weather.csv","w",newline="") as f:
            writer=csv.DictWriter(f,fieldnames=weatherinfo.keys())
            writer.writeheader()
            writer.writerow(weatherinfo)
            return jsonify(weatherinfo)
    
    else:
        return jsonify({"error":"Failed to fetch weather data"}),500  
#@app.route("/weather",methods=["POST"])
#def add():

if __name__=="__main__":
    app.run(debug=True)