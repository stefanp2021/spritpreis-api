import requests
from pandas import json_normalize
#admin-units
adminunitsurl = 'https://api.e-control.at/sprit/1.0/regions/units'
adminunits_requestheaders={'Accept': 'application/json'}
adminunits_response=requests.get(adminunitsurl, headers=adminunits_requestheaders).json()
#adminunits=json.dumps(adminunits_response)
#print(type(adminunits_response))
df_austria_sprit = json_normalize(adminunits_response)
df_bundesland_sprit= df_austria_sprit.iloc[0:]
#print(df_bundesland_sprit)
b_length=(len(df_bundesland_sprit))
b_shape=df_bundesland_sprit.shape
b_info=df_bundesland_sprit.info
b_describe=df_bundesland_sprit.describe
#print(b_length)
#print(b_shape)
print(b_describe)