import asyncio
import aiohttp
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
            "Condition":data["weather"][0]["main"],
            "Time":data["dt"]
        }
        with open("weather.json","a") as f:
            json.dump(weatherinfo,f)
        with     open("weather.csv","a",newline="") as f:
            writer=csv.DictWriter(f,fieldnames=weatherinfo.keys())
            writer.writeheader()
            writer.writerow(weatherinfo)
            return jsonify(weatherinfo)
    
    else:
        return jsonify({"error":"Failed to fetch weather data"}),500  
@app.route("/weather",methods=["POST"])
def add():
    data=request.json
    cities=[]
    for i in cities:
        response=requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={i}&appid={Api_key}")
        if response.status_code==200:
            data=response.json()
            weatherinfo={
                "city":data["name"],
                "temperature":data["main"]["temp"],
                "description":data["weather"][0]["description"],
                "humidity":data["main"]["humidity"]
            }
            cities.append(weatherinfo)

    return jsonify(cities)
async def fetch_weather(session, city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={Api_key}"
    async with session.get(url) as res:
        if res.status == 200:
            data = await res.json()
            return {
                "city": data["name"],
                "temperature": data["main"]["temp"],
                "description": data["weather"][0]["description"],
                "humidity": data["main"]["humidity"]
            }
        
        
        else:
            return {"error": f"Failed to fetch weather data for {city}"}
async def get_multiple_weather(cities):
    async with aiohttp.ClientSession() as session:
        work=[fetch_weather(session, city) for city in cities]
        return await asyncio.gather(*work)
@app.route("/weather/many",methods=["POST"])
def adding():
    data=request.json
    cities=data.get("cities",[])
    ans=asyncio.run(get_multiple_weather(cities))
    with open("weather.json","w") as f:
            json.dump(ans,f)
    with open("weather.csv","w",newline="") as f:
            writer=csv.DictWriter(f,fieldnames=ans[0].keys())
            writer.writeheader()
            for row in ans:
                writer.writerow(row)
    return jsonify(ans)



if __name__=="__main__":
    app.run(debug=True)