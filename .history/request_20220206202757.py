#docs https://api.e-control.at/sprit/1.0/doc/index.html?url=https://api.e-control.at/sprit/1.0/api-docs%3Fgroup%3Dpublic-api#/
from email import header
import json
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
includecities = input("Include Cities? Y/N")
Cities = 0
if includecities == ("Y") : 
    regions_url = 'https://api.e-control.at/sprit/1.0/regions?includeCities=true'
elif includecities == ("N") : 
    regions_url = 'https://api.e-control.at/sprit/1.0/regions?includeCities=false'
regions_response=requests.get(regions_url, headers=request_headers).content
print("Now calling the API via" + regions_url)
print(regions_response)
