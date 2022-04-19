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

base_url='https://api.e-control.at/sprit/1.0'

ping_url = '{baURL}/ping'.format(baURL=base_url)


#regions
#build-url
region_url='{baURL}/regions.format(baURL=base_url)

#print(my_funct())
# print(ping_url)
ping_headers = {'Accept': 'text/plain'}
ping_response = requests.get(ping_url, headers=ping_headers).content
print("Now pinging the API via" + ping_url)
print(ping_response)
