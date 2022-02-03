from email import header
import json
import pathlib
import re
from urllib import request
from xml.etree.ElementInclude import include
from requests.auth import HTTPBasicAuth
import requests
import pandas as pd
from pandas import json_normalize
from pathlib import Path

url_ping = 'https://api.e-control.at/sprit/1.0/ping'

print(url_ping)
headers = {'Accept': 'text/plain'}
result=requests.get(url_ping, headers=headers).json
print(result)

