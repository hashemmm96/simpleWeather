import json
import gzip
from urllib.request import Request, urlopen
import urllib.error
import tempfile
from io import BytesIO

dataUrl = "http://bulk.openweathermap.org/sample/city.list.json.gz"
apiEndpoint = "api.openweathermap.org/data/2.5/forecast?"

print("What country are you in?")
country = input("> ")
print("And what city are you in?")
city = input ("> ")

# fetch list of cities and their IDs
try: 
    with urllib.request.urlopen(dataUrl) as response:
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
    cityList = json.loads(f.read())
