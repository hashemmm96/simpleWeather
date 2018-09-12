import json
import gzip
from urllib.request import Request, urlopen
import urllib.error
import tempfile
from io import BytesIO
import requests

dataURL = "http://bulk.openweathermap.org/sample/city.list.json.gz"
apiURL = "http://api.openweathermap.org/data/2.5/weather"
apiKey = "d4b2007c1194620471443eb3c6fe4c68"

print("What city would you like to see the weather for?")
city = input ("> ")
city = city.casefold() # for case insensitive matching

# fetch list of cities and their IDs
try: 
    with urllib.request.urlopen(dataURL) as response:
        with tempfile.TemporaryFile() as tmp:
            tmp = response.read()

# error handling
except URLError as e:
    if hasattr(e, 'reason'):
        print('Failed to reach server.')
        print('Reason: ', e.reason)
    elif hasattr(e, 'code'):
        print('The server couldn\'t fulfill the request.')
        print('Error code: ', e.code)

# json file is zipped so need to unzip
with gzip.open(BytesIO(tmp)) as f:
    locations = json.loads(f.read())

# Check locations for city that was given by user
cityID = 0
for entry in locations:
    if entry['name'].casefold() == city:
        cityID = entry['id']

if cityID == 0:
    print ("Your city was not found. Program exited")
    exit()

# API call to get weather, using necessary parameters
apiCallParams = {'id': cityID, 'APPID': apiKey}
req = requests.get(apiURL, params=apiCallParams)
req.raise_for_status() # raise potential errors
weatherData = req.json()

# Extract relevant information
temp = round(weatherData['main']['temp']-273.15, 1)
weather = weatherData['weather'][0]['main'].lower()

# Print weather status
print("Weather in " + weatherData['name'] + " is " + weather)
print("Temperature in degrees celsius:", temp)
