from flask import Flask, render_template, redirect
import requests
import json

app = Flask(__name__)



#API request to transport API for bus times for these atco codes
#Pass to HTML flask template to display in HTML table

#Requir.: Please could it display the destination, the time to arrival and the line number.

atco_codes=["490008660N", "490008660S"]

postcode="NW5 1TL"

@app.route('/')
def main_page():
    bus_stops = []
    #atco_codes=getCoordinates(postcode)
    for code in atco_codes:
        try: 
            bus_stop = getBusDetails(code)
        except:
            return render_template('error.html', 404)
        bus_stops.append(bus_stop)
    return render_template('index.html', bus_stops=bus_stops)

    
def getBusDetails(atco):
    res = {}
    url='https://transportapi.com/v3/uk/bus/stop/'+atco+'/live.json?app_id=cf442150&app_key=cb9bae4e1ad5e833c64fdb1d3d4293db&group=route&nextbuses=yes&group=no'
    json_dict=getJson(url)
    
    res["stopName"] = json_dict["name"]
    res["buses"] = []
    for i in json_dict["departures"]["all"]:
        bus = {"line": i["line"], "arrival_time": i["expected"]["arrival"]["time"], "destination": i["direction"]}
        res["buses"].append(bus)
    
    return res


def getCoordinates(postcode):
    url = "http://api.postcodes.io/postcodes/"+postcode
    json_dict=getJson(url)
    lon=json_dict["result"]["longitude"]
    lat=json_dict["result"]["latitude"]
    atcoCodes=getAtcoCodes(lon, lat)
    return atcoCodes


def getAtcoCodes(lon, lat):
    #Function to pull out relevant atco codes based on postcode input
    res = []
    url = "http://transportapi.com/v3/uk/places.json?lat="+str(lat)+"&lon="+str(lon)+"&type=bus_stop&app_id=cf442150&app_key=cb9bae4e1ad5e833c64fdb1d3d4293db"
    json_dict=getJson(url)
    print (json_dict)
    for bus_stop in json_dict["member"]:
        res.append(bus_stop["atcocode"])
    return res


def getJson (url):
    r = requests.get(url) 
    r.raise_for_status()
    return r.json()


if __name__ == '__main__':
    app.run()
