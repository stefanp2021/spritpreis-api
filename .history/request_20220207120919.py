#docs https://api.e-control.at/sprit/1.0/doc/index.html?url=https://api.e-control.at/sprit/1.0/api-docs%3Fgroup%3Dpublic-api#/
from email import header
import json
from operator import index
import pathlib
import re
from unittest import result
from urllib import request, response
from wsgiref.util import request_uri
from xml.etree.ElementInclude import include
from requests.auth import HTTPBasicAuth
import requests
import pandas as pd
from pandas import json_normalize
from pathlib import Path

ping_url = 'https://api.e-control.at/sprit/1.0/ping'

request_headers = {'Accept': 'text/plain'}
ping_response=requests.get(ping_url, headers=request_headers).content
#print("Now pinging the API via" + ping_url)
#print(ping_response)

#Regions
regions_url = 'https://api.e-control.at/sprit/1.0/regions'
#includecities = input("Include Cities? Y/N ")
request_region_headers = {'Accept': 'application/json'}
Cities = 0
''' if includecities == ("Y") : 
    regions_url = 'https://api.e-control.at/sprit/1.0/regions?includeCities=true'
elif includecities == ("N") : 
    regions_url = 'https://api.e-control.at/sprit/1.0/regions?includeCities=false'
regions_response=requests.get(regions_url, headers=request_region_headers).json()
filename=Path("regions.json")
print("Now calling the API via " + regions_url)
 '''#print(regions_response)
#regions=json.dumps(regions_response)
#regions

#admin-units
adminunitsurl = 'https://api.e-control.at/sprit/1.0/regions/units'
adminunits_requestheaders={'Accept': 'application/json'}
adminunits_response=requests.get(adminunitsurl, headers=adminunits_requestheaders).json()
#adminunits=json.dumps(adminunits_response)
print(type(adminunits_response))
df_austria_sprit = json_normalize(adminunits_response)
df_bundesland_sprit= df_austria_sprit.iloc[0,:]
#print(df_json)
b=df_bundesland_sprit[2][0]
''' res = list(b.keys())
res_v = list(b.values()[0])
 '''
#print(df_bundesland_sprit)
print(b)

#print(list(a))
#print(type(adminunits_response))
#json_adminunits=json.loads(adminunits_response)
#adminunits_string=json.dumps(adminunits_response)
#print(adminunits_string)
#print(adminunits_string[0])
#a=json.loads(adminunits_string)
#print(type(a))
#print(len(a))
#print(len(a[0]["c"]))
#print(type(json_adminunits))
#print(json_adminunits)