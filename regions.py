#Needed packages and Links

from ctypes.wintypes import INT
from email import header
from multiprocessing.sharedctypes import Value
from optparse import Values
from queue import Empty
from time import sleep, time
from turtle import clear
from weakref import WeakSet
from xml.sax.xmlreader import Locator
import numpy as np
import requests
import json
import pandas as pd
from pathlib import Path
from pandas import json_normalize
import datetime
from datetime import datetime
from datetime import timedelta
import time

import tqdm
from tqdm import tqdm

import mysql.connector



from Objects import Location, Region, Station, SType, StationUpdate

mydb = mysql.connector.connect(
        host="dev.muenzer.at",
        user="spritpreise",
        password ="]4e6H[tZCQc.YoY,S6jK",
        database="spritpreise"
    )


#regions_url = 'https://api.e-control.at/sprit/1.0/regions'
request_region_headers = {'Accept': 'application/json'}



# Engine -  to provide a unit of connectivity to the database called the Connection.
#engine = create_engine("mysql+pymysql://{user}:{pw}@{host}/{db}".format(user=user, pw = password,host=host,db=database))


#engine = create_engine("mysql://{user}:{pw}@{host}/{db}".format(user=user, pw = password,host=host,db=database))




def func_dump(obj):
    for attr in dir(obj):
        print("obj.%s = %r" % (attr, getattr(obj, attr)))



units_url = "https://api.e-control.at/sprit/1.0/regions/units"
units_response=requests.get(units_url, headers=request_region_headers).json()
units=json.dumps(units_response)

units_complete_dataset=json_normalize(units_response)

#print(units_complete_dataset)


#df_new_PostCity_forUpdate = pd.DataFrame(data=[NaNvalues],columns=(df_regions_complete_CitiesStreet.columns)) 



print("Starting with the API request for the regions")

get_Region_info = units_complete_dataset["b"]

for i in tqdm(range(get_Region_info.shape[0])):

    get_Region_single = get_Region_info[i]
    #print(get_Region_single)

    for j in range(len(get_Region_single)):
        
        get_Region_single_elements = get_Region_single[j]
        get_Region_single_elements_Regionc = get_Region_single_elements["c"]
        get_Region_single_elements_Regionn = get_Region_single_elements["n"]
        get_Region_single_elements_g = get_Region_single_elements["g"]

        obj_Region = Region(code=get_Region_single_elements_Regionc, name=get_Region_single_elements_Regionn)
        count_Region = obj_Region.AskCountRegion(mydb)
        if(count_Region[0][0] < 1):
            obj_Region.InsertSQLRegion(mydb)
        else:
            pass
        del obj_Region


        for k in range(len(get_Region_single_elements_g)):
                
            get_location_single_elements_g_length_element = get_Region_single_elements_g[k]

            #print(get_location_single_elements_g_length_element)            
            get_location_single_first_g_length_Locname = get_location_single_elements_g_length_element["n"]
            get_location_single_first_g_length_Locpost = get_location_single_elements_g_length_element["p"]

            obj_Location = Location(postCode=get_location_single_first_g_length_Locpost, location=get_location_single_first_g_length_Locname)
            count_Location = obj_Location.AskCountLocation(mydb)
            if(count_Location[0][0] < 1):
                obj_Location.InsertSQLLocation(mydb)
            else:
                pass
            del obj_Location



print("Regions are inserted in the SQL-Database")


#####################################        Insert the Stations of the different Regions       ########################
print("Now starting with the Stations")



mycursor = mydb.cursor()
sql_t = "SELECT Type FROM tbl_Type"
mycursor.execute(sql_t)
myresult_fetchTypes = mycursor.fetchall()
mydb.commit()
#print(myresult_fetchTypes)

mycursor = mydb.cursor()
sql_f = "SELECT fueltype FROM tbl_fueltype"
mycursor.execute(sql_f)
myresult_fetchFuelTypes = mycursor.fetchall()
mydb.commit()
#print(myresult_fetchFuelTypes)

mycursor = mydb.cursor()
sql_C = "SELECT region_Code FROM tbl_spritregions"
mycursor.execute(sql_C)
myresult_fetchRegions = mycursor.fetchall()
mydb.commit()
#print(myresult_fetchRegions)

mycursor = mydb.cursor()
sql_Status = "SELECT Status_ID FROM tbl_Status WHERE Status=%s"
val_status = ("Active",)
mycursor.execute(sql_Status,val_status)
myresult_fetchStatus = mycursor.fetchall()
mydb.commit()

header_all_sprit = ["id","name","location.address","location.postalCode","location.city","location.latitude","location.longitude","contact.telephone","contact.mail","contact.website","offerInformation.service","offerInformation.selfService","open", "fuelType","amount","label","Type","regioncode","Status","UpdateDate"] 
header_all_sprit_withoutpreis = ["id","name","location.address","location.postalCode","location.city","location.latitude","location.longitude","contact.telephone","contact.mail","contact.website","offerInformation.service","offerInformation.selfService","open", "prices"] 
#df_whole_sprit = pd.DataFrame(columns=(header_all_sprit))


actual_dateTime = datetime.now().isoformat(sep=' ', timespec='milliseconds')
#print(actual_dateTime)


for i in tqdm(range(len(myresult_fetchRegions))):
    #print(i)
    value_region_code = str(myresult_fetchRegions[i][0])
    for j in range(len(myresult_fetchTypes)):
        value_type_code = myresult_fetchTypes[j][0]

        for k in range(len(myresult_fetchFuelTypes)):
            value_fueltype_code = myresult_fetchFuelTypes[k][0]


            #'Vorbereitung'
            Station_Url = "https://api.e-control.at/sprit/1.0/search/gas-stations/by-region?code={gcode}&type={type_pb}&fuelType={fueltype}&includeClosed=true".format(gcode=value_region_code,type_pb=value_type_code,fueltype=value_fueltype_code)
            #print(Station_Url)
            #Station_Url = "https://api.e-control.at/sprit/1.0/search/gas-stations/by-region?code={gcode}&type={type_pb}&fuelType={fueltype}&includeClosed=true".format(gcode=str(920),type_pb="PB",fueltype="GAS")
            request_Station_headers = {'Accept': 'application/json'}
            Station_response=requests.get(Station_Url, headers=request_Station_headers).json()
            #Stationsvalues=json.dumps(Station_response)
            complete_dataset_Station=json_normalize(Station_response)

            #lst_adding = []

            #print(df_new_test)

            if not complete_dataset_Station.empty:
                length_dataSet_Fuel = complete_dataset_Station.shape[0]
                for r in range(length_dataSet_Fuel):
                    #counter_full = counter_full + 1
                    df_single_dataset_Station = complete_dataset_Station.loc[r]
                    #print(df_single_dataset_Station)

                    #make a DataFrame to save in between values so it is much easier to handle in the end
                    NaNvalues = [None] * len(header_all_sprit)
                    df_new_Station = pd.DataFrame([NaNvalues],columns=(header_all_sprit))
                    for q in range(len(header_all_sprit_withoutpreis)):
                        reiter_name = header_all_sprit_withoutpreis[q]
                        # Look if the column even exists in the dataframe
                        if reiter_name in complete_dataset_Station.columns:
                            var = df_single_dataset_Station[reiter_name]
                            # Because a True would be a 1 in the SQL we want to right it as a Text
                            if(type(var) is np.bool_):
                                var = str(var)
                            else:
                                pass

                            #Reiter is price we have to go further in
                            if(reiter_name == header_all_sprit_withoutpreis[-1]):


                                var = df_single_dataset_Station[str(reiter_name)]
                                var_intro_keys = var[0]
                                #var_prices_with_keys = var_intro_keys
                                list_of_keys = list(var_intro_keys.keys())
                                for o in list_of_keys:

                                    prices_key_value = var_intro_keys[o]
                                    df_price_single = pd.DataFrame(data=[prices_key_value],columns=[o],index=[0])
                                    df_new_Station.update(df_price_single)

                            else:


                                df_new_values_single = pd.DataFrame(data=[var],columns=[reiter_name],index=[0])
                                df_new_Station.update(df_new_values_single)

                            #Update the new Station with the Type that is used
                            df_new_Type = pd.DataFrame(data=[value_type_code],columns=[header_all_sprit[-4]],index=[0])
                            df_new_Station.update(df_new_Type)
                            #Update the new Station with the RegionCode that is used
                            df_new_StCode = pd.DataFrame(data=[value_region_code],columns=[header_all_sprit[-3]],index=[0])
                            df_new_Station.update(df_new_StCode)
                            #Update the new Station with the Status that is used
                            df_new_StCode = pd.DataFrame(data=[myresult_fetchStatus[0]],columns=[header_all_sprit[-2]],index=[0])
                            df_new_Station.update(df_new_StCode)
                            #Update the new Station with the DateTime that is used
                            df_new_StCode = pd.DataFrame(data=[actual_dateTime],columns=[header_all_sprit[-1]],index=[0])
                            df_new_Station.update(df_new_StCode)


                        else:
                            pass
                    #print(df_new_Station)
                    ############################ Now we have a whole row of information in the DataFrame for a complete Station, so we can load it in the SQL
                    #first we look for the location

                    ## Values from DataFrame is a Series, therefore we need .values[0] to get the Info itself
                    df_ST_Single_id = df_new_Station[header_all_sprit[0]].values[0]
                    df_ST_Single_name = df_new_Station[header_all_sprit[1]].values[0]
                    df_ST_Single_adress = df_new_Station[header_all_sprit[2]].values[0]
                    df_ST_Single_postalCode = df_new_Station[header_all_sprit[3]].values[0]
                    df_ST_Single_city = df_new_Station[header_all_sprit[4]].values[0]
                    df_ST_Single_latitude = df_new_Station[header_all_sprit[5]].values[0]
                    df_ST_Single_longitude = df_new_Station[header_all_sprit[6]].values[0]
                    df_ST_Single_telephone = df_new_Station[header_all_sprit[7]].values[0]
                    df_ST_Single_mail = df_new_Station[header_all_sprit[8]].values[0]
                    df_ST_Single_website = df_new_Station[header_all_sprit[9]].values[0]
                    df_ST_Single_service = df_new_Station[header_all_sprit[10]].values[0]
                    df_ST_Single_selfService = df_new_Station[header_all_sprit[11]].values[0]
                    df_ST_Single_open = df_new_Station[header_all_sprit[12]].values[0]
                    df_ST_Single_fuelType = df_new_Station[header_all_sprit[13]].values[0]
                    df_ST_Single_amount = df_new_Station[header_all_sprit[14]].values[0]
                    df_ST_Single_label = df_new_Station[header_all_sprit[15]].values[0]
                    df_ST_Single_Type = df_new_Station[header_all_sprit[16]].values[0]
                    df_ST_Single_Code =   df_new_Station[header_all_sprit[17]].values[0]
                    df_ST_Single_Status = df_new_Station[header_all_sprit[18]].values[0]
                    df_ST_Single_DateTime = df_new_Station[header_all_sprit[19]].values[0]

                    ### First, add Location if new locations
                    #print("-----------------------------------------------------------")
                    #print(df_ST_Single_postalCode,df_ST_Single_city)
                    #print("--------")
                    obj_Location = Location(postCode=df_ST_Single_postalCode,location=df_ST_Single_city)
                    st_location_count = obj_Location.AskCountLocation(mydb)

                    if(st_location_count[0][0] < 1):
                        obj_Location.InsertSQLLocation(mydb)
                    else:
                        pass
                    del obj_Location
                    
                    ########
                    ### Second, add Type if new Types
                    #print(df_ST_Single_Type)
                    obj_Type = SType(type=df_ST_Single_Type)
                    st_type_count = obj_Type.AskCountType(mydb)

                    if(st_type_count[0][0] < 1):
                        obj_Type.InsertSQLLocation(mydb)
                    else:
                        pass
                    del obj_Type

                    ####
                    ### Third, add Stations if new Stations
                    obj_Station = Station(id=df_ST_Single_id, name=df_ST_Single_name, type=df_ST_Single_Type, address=df_ST_Single_adress, postalCode=df_ST_Single_postalCode,
                    city=df_ST_Single_city, latitude=df_ST_Single_latitude,longitude=df_ST_Single_longitude,telephone=df_ST_Single_telephone,mail=df_ST_Single_mail,
                    website=df_ST_Single_website, service=df_ST_Single_service, selfService=df_ST_Single_selfService, open=df_ST_Single_open, fuelType=df_ST_Single_fuelType,
                    amount=df_ST_Single_amount, label=df_ST_Single_label, regioncode=df_ST_Single_Code, statusID=df_ST_Single_Status,datetiming=df_ST_Single_DateTime)

                    obj_Station.PLZId = obj_Station.GetPlzID(mydb)[0][0]
                    obj_Station.FuelId = obj_Station.GetFuelTypeID(mydb)[0][0]
                    obj_Station.TypeID = obj_Station.GetTypeID(mydb)[0][0]
                    obj_Station.RegionId = obj_Station.GetRegionID(mydb)[0][0]

                    count_Station = obj_Station.AskCountStation(mydb)

                    if(count_Station[0][0] < 1):
                        obj_Station.InsertSQLStation(mydb)
                    else:
                        obj_Station.UpdateSQLStation(mydb)

                    del obj_Station



            else:
                pass


print(" API for Stations over all Fueltypes are finished and inserted/updated on the MySQL-Database")

############################################################################
#########                   Abfrage nach inaktiven Stationen

#################################################################################
print("Now starting with the control of inactive Stations (if no change over 4 days)")


mycursor = mydb.cursor()
sql_Status_inactive = "SELECT Status_ID FROM tbl_Status WHERE Status=%s"
val_status_inactive = ("Inactive",)
mycursor.execute(sql_Status_inactive,val_status_inactive)
myresult_fetchStatus_Inactive = mycursor.fetchall()
mycursor.close()
mydb.commit()
inactive_value_DB = myresult_fetchStatus_Inactive[0][0]
print(inactive_value_DB)

mycursor = mydb.cursor()
sql_update_inactive_status = "SELECT StationID,fueltype_Id,Type_Id,DateTime FROM tbl_Station WHERE Status_Id <> %s" #every station that is not inactive
val_update_inactive_status = (inactive_value_DB,)
mycursor.execute(sql_update_inactive_status,val_update_inactive_status)
myresult_UpdateInactiveStatus = mycursor.fetchall()
mycursor.close()
mydb.commit()

# Now we get the actual datetime, if a station isn't update for 4 days, the status will be inactive
actual_dateTime_for_difference = str(datetime.now().isoformat(sep=' '))
date_time_obj = datetime.strptime(actual_dateTime_for_difference, "%Y-%m-%d %H:%M:%S.%f")

for i in tqdm(range(len(myresult_UpdateInactiveStatus))):

    get_Infos_forInactive = myresult_UpdateInactiveStatus[0]
    UInact_SId = get_Infos_forInactive[0]
    UInact_FuelId = get_Infos_forInactive[1]
    UInact_TypeId = get_Infos_forInactive[2]
    UInact_Date = get_Infos_forInactive[3]

    obj_StationUpdate = StationUpdate(id=UInact_SId,type=UInact_TypeId,fuelType=UInact_FuelId,statusID=inactive_value_DB)

    diff_Date =  date_time_obj - UInact_Date

    if(diff_Date > timedelta(days=4)):
        obj_StationUpdate.UpdateSQLStationUpdate(mydb)
    else:
        pass
  
    del obj_StationUpdate


print("finished with the job")




