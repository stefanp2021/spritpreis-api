import requests
import json
from pathlib import Path
from pandas import json_normalize
regions_url = 'https://api.e-control.at/sprit/1.0/regions'
includecities = input("Include Cities? Y/N ")
request_region_headers = {'Accept': 'application/json'}
Cities = 0
if includecities == ("Y") : 
    regions_url = 'https://api.e-control.at/sprit/1.0/regions?includeCities=true'
elif includecities == ("N") : 
    regions_url = 'https://api.e-control.at/sprit/1.0/regions?includeCities=false'
regions_response=requests.get(regions_url, headers=request_region_headers).json()
#filename=Path("regions.json")
#print("Now calling the API via " + regions_url)
#print(regions_response)
regions=json.dumps(regions_response)
print(type(regions))

a=json_normalize(regions_response)
b=a.loc[2]
c=b["subRegions"]
d=json.dumps(c)
print(d)

