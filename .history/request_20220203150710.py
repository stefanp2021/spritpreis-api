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

url_ping = 'https://api.e-control.at/sprit/1.0/ping'

print(url_ping)
headers = {'Accept': 'text/plain'}
response=requests.get(url_ping, headers=headers).content
result=json_normalize(response)
