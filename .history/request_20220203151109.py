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

print(ping_url)
ping_headers = {'Accept': 'text/plain'}
ping_response=requests.get(ping_url, headers=ping_headers).content
print(ping_response)


