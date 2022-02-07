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