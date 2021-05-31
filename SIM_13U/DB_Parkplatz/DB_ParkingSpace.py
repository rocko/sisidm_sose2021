import requests
import json
from datetime import datetime

url:str = "https://api.deutschebahn.com/bahnpark/v1/spaces/100040/occupancies"

payload:dict={}
headers:dict = {'Authorization': 'Bearer 9aa873e0e58406dc3087344db59b1983'}
response:object = requests.request("GET", url, headers=headers, data=payload)
data:object = json.loads(response.text)

timestamp:object = datetime.strptime(data["allocation"]["timestamp"], '%Y-%m-%dT%H:%M:%S')
space_str:list = ["bis zu 10", "mehr als 10", "mehr als 30", "mehr als 50"]

print("Parkplatz Meldung für {0} vom {1} um {2}\n\t Parkplätze: {3} | aktuell {4} freie Parkplätze".format(
    data["space"]["nameDisplay"], 
    "{}.{}.{}".format(timestamp.day, timestamp.month, timestamp.year), 
    "{}:{} Uhr".format(timestamp.hour, timestamp.minute), 
    data["allocation"]["capacity"], 
    space_str[data["allocation"]["category"]-1]
))