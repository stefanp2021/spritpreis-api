from multiprocessing.sharedctypes import Value
import requests
import json
import pandas as pd
from pathlib import Path
from pandas import json_normalize
regions_url = 'https://api.e-control.at/sprit/1.0/regions'
#includecities = input("Include Cities? Y/N ")
request_region_headers = {'Accept': 'application/json'}
Cities = 1
''' if includecities == ("Y") : 
    regions_url = 'https://api.e-control.at/sprit/1.0/regions?includeCities=true'
elif includecities == ("N") : 
    regions_url = 'https://api.e-control.at/sprit/1.0/regions?includeCities=false'
    '''
    
    
regions_url = 'https://api.e-control.at/sprit/1.0/regions?includeCities=true'
regions_response=requests.get(regions_url, headers=request_region_headers).json()
#filename=Path("regions.json")
#print("Now calling the API via " + regions_url)
#print(regions_response)
regions=json.dumps(regions_response)
#print(type(regions))
df_regions_sprit = pd.DataFrame(columns=("code","type"))

complete_dataset=json_normalize(regions_response)

print(complete_dataset)

for j in range(len(complete_dataset)):

    df_Bundesland = complete_dataset.loc[j]
    df_Bundesland_subregion =df_Bundesland["subRegions"]

    print(df_Bundesland_subregion)

    #for k in range(len(df_Bundesland_subregion)):
    #df_Bezirke_Gesamt = df_Bundesland_subregion[k]
    #print("----")
    #print(df_Bezirke_Gesamt['code'])
    
    
    for i in range(len(df_Bundesland_subregion)):
        regions = df_Bundesland_subregion[i]
        #print(regions['type'])
        #print('-----')
        regions_code=regions['code']
        regions_type=regions['type']
        lstr=[[regions_code,regions_type]]
        df_new_entry=pd.DataFrame(lstr,columns=("code","type"))
        #print(df_new_entry)
        frames=[df_regions_sprit,df_new_entry]
        df_regions_sprit=pd.concat(frames)
    
df_regions_sprit.reset_index(inplace=True,drop=True)
print(df_regions_sprit)
   