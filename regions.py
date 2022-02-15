from ctypes.wintypes import INT
from email import header
from multiprocessing.sharedctypes import Value
from optparse import Values
from queue import Empty
#from tkinter.tix import AUTO
from turtle import clear
from xml.sax.xmlreader import Locator
import numpy as np
#from numpy import NaN
import requests
import json
import pandas as pd
from pathlib import Path
from pandas import json_normalize

# pip install cryptography --> needed
import pymysql
from pymysql import NULL
import mysql.connector
import sqlalchemy as db
#from sqlalchemy import VARCHAR, BigInteger, create_engine



from sqlalchemy import VARCHAR, create_engine, Column, Integer, String, Sequence, Float,PrimaryKeyConstraint, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.sql import *


from Objects import Location, Region, Station


#from sqlalchemy.orm import declarative_base
#from sqlalchemy import Column, Integer, String, text, Text, INTEGER, MetaData

# Tutorial
# https://docs.sqlalchemy.org/en/14/tutorial/dbapi_transactions.html
#https://medium.com/dataexplorations/sqlalchemy-orm-a-more-pythonic-way-of-interacting-with-your-database-935b57fd2d4d


#host= "dev.muenzer.at"  #"192.168.10.34" 
#user="spritpreise" #@192.168.10.21
#password ="]4e6H[tZCQc.YoY,S6jK"
#database="spritpreise"



mydb = mysql.connector.connect(
        host="dev.muenzer.at",
        user="spritpreise",
        password ="]4e6H[tZCQc.YoY,S6jK",
        database="spritpreise"
    )

# Engine -  to provide a unit of connectivity to the database called the Connection.
#engine = create_engine("mysql+pymysql://{user}:{pw}@{host}/{db}".format(user=user, pw = password,host=host,db=database))


#engine = create_engine("mysql://{user}:{pw}@{host}/{db}".format(user=user, pw = password,host=host,db=database))




regions_url = 'https://api.e-control.at/sprit/1.0/regions'

request_region_headers = {'Accept': 'application/json'}
Cities = 1


def func_dump(obj):
    for attr in dir(obj):
        print("obj.%s = %r" % (attr, getattr(obj, attr)))



#includecities = input("Include Cities? Y/N ")
#if includecities == ("Y") : 
#    regions_url = 'https://api.e-control.at/sprit/1.0/regions?includeCities=true'
#elif includecities == ("N") : 
#    regions_url = 'https://api.e-control.at/sprit/1.0/regions?includeCities=false'




units_url = "https://api.e-control.at/sprit/1.0/regions/units"
units_response=requests.get(units_url, headers=request_region_headers).json()
units=json.dumps(units_response)

#df_regions_sprit = pd.DataFrame(columns=("code","type","name"))

units_complete_dataset=json_normalize(units_response)

#print(units_complete_dataset)

list_units_sprit = ("PLZ","Location")
df_units_sprit = pd.DataFrame(columns=list_units_sprit)


get_location_info = units_complete_dataset["b"]

for i in range(len(get_location_info)):

    get_location_single = get_location_info[i]

    for j in range(len(get_location_single)):
        
        get_location_single_elements = get_location_single[j]
        get_location_single_elements_g = get_location_single_elements["g"]
        #print(get_location_single_elements_g)


        for k in range( len(get_location_single_elements_g)):

            
            get_location_single_elements_g_length_element = get_location_single_elements_g[k]
            
            get_location_single_first_g_length_n = get_location_single_elements_g_length_element["n"]
            get_location_single_first_g_length_p = get_location_single_elements_g_length_element["p"]

            df_new_entry_units = pd.DataFrame(data=[[get_location_single_first_g_length_p,get_location_single_first_g_length_n]],columns=list_units_sprit)
            
            #print(df_new_entry_units)
            frames=[df_units_sprit,df_new_entry_units]
            df_units_sprit=pd.concat(frames)

#df_units_sprit.reset_index(inplace=True,drop=True)
df_units_sprit.reset_index(inplace=True)
#print(df_units_sprit)

for i in range(len(df_units_sprit)):
    #print(i)
    df_units_sprit_Single = df_units_sprit.iloc[i,:]

    #print(df_units_sprit_Single)

    df_units_sprit_Single_PLZ = df_units_sprit_Single["PLZ"]
    df_units_sprit_Single_Location = df_units_sprit_Single["Location"]

    #print(df_units_sprit_Single_PLZ, df_units_sprit_Single_Location )
    obj_Location = Location(postCode=df_units_sprit_Single_PLZ, location=df_units_sprit_Single_Location)

    count_object_loc = obj_Location.AskCountOperator(mydb)

    if(count_object_loc[0][0] < 1):
        obj_Location.InsertSQLOperator(mydb)
    
    del obj_Location

print(" Finished first PLZ/Location Update")



############################################################################################################
########                    URL for the Regions                     ###############
############################################################################################################

regions_url = 'https://api.e-control.at/sprit/1.0/regions?includeCities=true'
request_region_headers = {'Accept': 'application/json'}
regions_response=requests.get(regions_url, headers=request_region_headers).json()
regions=json.dumps(regions_response)

#df_regions_sprit = pd.DataFrame(columns=("code","type","name"))

complete_dataset=json_normalize(regions_response)

#print(complete_dataset)

list_useful_regions = ["code","type","name","postalCodes","cities"]

df_regions_complete_read = pd.DataFrame(columns=list_useful_regions)
#df_Street_complete_Frame = pd.DataFrame(columns=list_useful_regions_CoordStreet)
#print(df_regions_complete_read)


for j in range(len(complete_dataset)):

    df_Bundesland = complete_dataset.loc[j]
    df_Bundesland_subregion =df_Bundesland["subRegions"]

    #print(df_Bundesland)
    
    for i in range(len(df_Bundesland_subregion)):
        regions = df_Bundesland_subregion[i]

        #print(regions)

        regions_code = regions[list_useful_regions[0]]
        regions_type = regions[list_useful_regions[1]]
        regions_name = regions[list_useful_regions[2]]

        
        ##### This isn't necassery, but just to show, that we cannot easily build a table_street because there
        ##### is no unique connection with the Station and the PostalCode/Cities and Name
        
        if(list_useful_regions[3] in regions.keys()):
            regions_Coordpostcode = regions[list_useful_regions[3]]
            regions_CoordCities = regions[list_useful_regions[4]]
        else:
            regions_Coordpostcode is None
            regions_CoordCities is None


        #print()
        
        lstr=[[regions_code,regions_type,regions_name,regions_Coordpostcode,regions_CoordCities]]
        df_new_entry=pd.DataFrame(lstr,columns=list_useful_regions)
        frames=[df_regions_complete_read,df_new_entry]
        df_regions_complete_read=pd.concat(frames)

    
df_regions_complete_read.reset_index(inplace=True,drop=True)
df_regions_complete_Type = df_regions_complete_read[[list_useful_regions[0],list_useful_regions[1],list_useful_regions[2]]]
#print(df_regions_complete_Type)
df_regions_complete_CitiesStreet = df_regions_complete_read[[list_useful_regions[3],list_useful_regions[4]]]
#print(df_regions_complete_CitiesStreet)




# This is an additional way for taking new PLZ in the SQL-Database
df_new_PostCityList_whole = pd.DataFrame(columns=df_regions_complete_CitiesStreet.columns)
#print(df_new_PostList)
for z in range(df_regions_complete_CitiesStreet.shape[0]):

    get_location = df_regions_complete_CitiesStreet.iloc[z,:]
    length_items = len(get_location[1])

    get_loc_post = get_location[df_regions_complete_CitiesStreet.columns[0]]
    get_loc_city = get_location[df_regions_complete_CitiesStreet.columns[1]]

    #print(get_loc_post)
    #print(get_loc_city)
    #print(z)
    #print("--")
    for y in range(length_items):

        #if(z == 35):
        #    print(y)
        #    print(get_loc_post)
        #    print(get_loc_city)
        NaNvalues = [None] * len(df_regions_complete_CitiesStreet.columns)
        df_new_PostCity_forUpdate = pd.DataFrame(data=[NaNvalues],columns=(df_regions_complete_CitiesStreet.columns)) 

        get_loc_post_single = get_loc_post[y]
        get_loc_city_single = get_loc_city[y]

        df_loc_post_update = pd.DataFrame(data=[get_loc_post_single],columns=[df_regions_complete_CitiesStreet.columns[0]],index=[0])
        df_loc_city_update = pd.DataFrame(data=[get_loc_city_single],columns=[df_regions_complete_CitiesStreet.columns[1]],index=[0])

        #print(df_loc_post_update)
        #print(df_loc_city_update)
        #print('------------------------')
        #print(df_new_PostCity_forUpdate)

        df_new_PostCity_forUpdate.update(df_loc_post_update)
        df_new_PostCity_forUpdate.update(df_loc_city_update)

        frames = [df_new_PostCityList_whole, df_new_PostCity_forUpdate]
        df_new_PostCityList_whole = pd.concat(frames)


#print(df_new_PostCityList_whole)



#An additional to the additional above
for i in range(len(df_new_PostCityList_whole)):
    #print(i)
    df_units_sprit_Single = df_new_PostCityList_whole.iloc[i,:]

    #print(df_units_sprit_Single)

    df_units_sprit_Single_PLZ = df_units_sprit_Single[df_new_PostCityList_whole.columns[0]]
    df_units_sprit_Single_Location = df_units_sprit_Single[df_new_PostCityList_whole.columns[1]]

    #print(df_units_sprit_Single_PLZ, df_units_sprit_Single_Location )
    obj_Location = Location(postCode=df_units_sprit_Single_PLZ, location=df_units_sprit_Single_Location)

    count_object_loc = obj_Location.AskCountOperator(mydb)

    if(count_object_loc[0][0] < 1):
        obj_Location.InsertSQLOperator(mydb)
    
    del obj_Location


print(" Finished with filling the Table PLZ ")









for i in range(len(df_regions_complete_Type)):
    #print(i)
    df_regions_sprit_Single = df_regions_complete_Type.iloc[i,:]

    #print(df_units_sprit_Single)

    df_regions_sprit_Single_code = df_regions_sprit_Single["code"]
    df_regions_sprit_Single_type = df_regions_sprit_Single["type"]
    df_regions_sprit_Single_name = df_regions_sprit_Single["name"]

    #print(df_units_sprit_Single_PLZ, df_units_sprit_Single_Location )
    obj_Region = Region(code=df_regions_sprit_Single_code, type=df_regions_sprit_Single_type, name=df_regions_sprit_Single_name)

    count_object_reg = obj_Region.AskCountOperator(mydb)

    if(count_object_reg[0][0] < 1):
        obj_Region.InsertSQLOperator(mydb)
    else:
        obj_Region.UpdateSQLOperator(mydb)
    
    del obj_Region

print("Finished Code Search, now we search for Stations")

###############################################################################################################

# And now the big SQL






##### Insert the Stations of the different Regions


#print(df_regions_complete_Type)


#Test if Abfrage have two resulst

import time
time.sleep(30)

for iq in range(2):
    print(iq)



    header_all_sprit = ["id","name","location.address","location.postalCode","location.city","location.latitude","location.longitude","contact.telephone","contact.mail","contact.website","offerInformation.service","offerInformation.selfService","open", "fuelType","amount","label","Type","code"] 
    header_all_sprit_withoutpreis = ["id","name","location.address","location.postalCode","location.city","location.latitude","location.longitude","contact.telephone","contact.mail","contact.website","offerInformation.service","offerInformation.selfService","open", "prices"] 
    df_whole_sprit = pd.DataFrame(columns=(header_all_sprit))

    get_header_for_all_regions = list(df_regions_complete_Type.columns)
    get_code_for_regions = list(df_regions_complete_Type[get_header_for_all_regions[0]])
    #print(get_code_for_regions)
        
    #gasstation_url = "https://api.e-control.at/sprit/1.0/search/gas-stations/by-region?code={gcode}&type={type_pb}&fuelType={fueltype}&includeClosed=true".format(gcode=str(101),type_pb="PB",fueltype="GAS")
    #gasstation_url = 'https://api.e-control.at/sprit/1.0/regions?includeCities=true'
    #request_gas_headers = {'Accept': 'application/json'}
    #gas_response=requests.get(gasstation_url, headers=request_gas_headers).json()
    #gas=json.dumps(gas_response)
    #complete_dataset_gas=json_normalize(gas_response)

    #print(complete_dataset_gas.keys())


    #print(df_whole_sprit)
    #########################




    mycursor = mydb.cursor()
    sql = "SELECT fueltype FROM tbl_fueltype"
    mycursor.execute(sql)
    myresultFuel_count = mycursor.fetchall()
    mydb.commit()


    lst_Type = ["PB","BL"]



    for k in get_code_for_regions:

        for Insert_type in lst_Type:

            for fut in myresultFuel_count:
                
                ft = fut[0]

                gasstation_url = "https://api.e-control.at/sprit/1.0/search/gas-stations/by-region?code={gcode}&type={type_pb}&fuelType={fueltype}&includeClosed=true".format(gcode=str(k),type_pb=Insert_type,fueltype=ft)
                #gasstation_url = 'https://api.e-control.at/sprit/1.0/regions?includeCities=true'
                request_gas_headers = {'Accept': 'application/json'}
                gas_response=requests.get(gasstation_url, headers=request_gas_headers).json()
                gas=json.dumps(gas_response)
                complete_dataset_gas=json_normalize(gas_response)

                lst_adding = []
                #list_var_select_header = ["id","name","location.address","location.postalCode","location.city","location.latitude","location.longitude","contact.telephone","contact.mail","contact.website","offerInformation.service","offerInformation.selfService","open","prices.fuelType","prices.amount","prices.label"]

                #NaNvalues = [np.nan] * len(header_all_sprit)
                NaNvalues = [None] * len(header_all_sprit)
                df_new_test = pd.DataFrame([NaNvalues],columns=(header_all_sprit))
                #print(df_new_test)

            
                #print(complete_dataset_gas)
                if not complete_dataset_gas.empty:
                    #print("YEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEESSSSSSSSSSSSSSSSSSSSS")
                
                    #print(k)
                    #print(complete_dataset_gas)
                    
                    #Now we have to look how many rows there are

                    length_dataSet_Fuel = complete_dataset_gas.shape[0]
                    #print(complete_dataset_gas)
                    #print(length_dataSet_Fuel)
                    #print("---------------------------------------")
                    for r in range(length_dataSet_Fuel):
                        #print(r)
                        #print("---------------              STAGE 1             --------------------------")
                        df_single_dataset_gas_g = complete_dataset_gas.iloc[r,:]
                        df_single_dataset_gas = df_single_dataset_gas_g
                        #print(type(df_single_dataset_gas))
                        #print(df_single_dataset_gas)
                        #print('---')
                        #print(df_single_dataset_gas.columns.values)
                        #print(df_single_dataset_gas.columns)
                        #print(df_single_dataset_gas)
                        #print("--")
                        #print(df_single_dataset_gas["prices"])
                        #print("-----------------------------------------")
                        for i in range(len(header_all_sprit_withoutpreis)):
                        
                            reiter_name = header_all_sprit_withoutpreis[i]
                            #print(reiter_name)
                            #print(reiter_name)
                            #print("---------------              STAGE 2             --------------------------")
                            # Look if the column even exists in the dataframe
                            if reiter_name in complete_dataset_gas.columns:

                                #print("---------------              STAGE 3             --------------------------")
                                #print(df_single_dataset_gas[reiter_name])
                                var = df_single_dataset_gas[reiter_name]
                                #print(var)
                                if(type(var) is np.bool_):
                                    var = str(var)
                                else:
                                    pass

                                #print("reiter:   {a},   Value :    {b}    ".format(a = reiter_name, b = var))
                                #print("---------------------------------------------------------------")
                                if(reiter_name == header_all_sprit_withoutpreis[-1]):

                                    #print("---------------              STAGE 4             --------------------------")
                                    #print(reiter_name)
                                    #prices = var[0][0]
                                    #print(k)

                                    var = df_single_dataset_gas[str(reiter_name)]
                                    #print(var)
                                    var_intro_keys = var[0]
                                    
                                    #print(var_intro_keys)
                                    var_prices_with_keys = var_intro_keys
                                    list_of_keys = list(var_prices_with_keys.keys())
                                    for j in list_of_keys:

                                        prices_key_value = var_prices_with_keys[j]
                                        df_new_test_single = pd.DataFrame(data=[prices_key_value],columns=[j],index=[0])
                                        df_new_test.update(df_new_test_single)
                                        #print(df_new_test)
                                    
                                else:

                                    #print("---------------              STAGE 5             --------------------------")
                                    #pass
                                    #print("---------------------------------------------------------------")
                                    #print(df_new_test)
                                    df_new_test_single = pd.DataFrame(data=[var],columns=[reiter_name],index=[0])
                                    df_new_test.update(df_new_test_single)
                                    #print(df_new_test)
                                    ### Here now we have to include the Type from the API request --> PB or BP


                                
                                df_new_test_Type = pd.DataFrame(data=[Insert_type],columns=["Type"],index=[0])
                                df_new_test.update(df_new_test_Type)
                                #print(df_new_test)
                                df_new_test_code = pd.DataFrame(data=[str(k)],columns=["code"],index=[0])
                                df_new_test.update(df_new_test_code)
                                #print(df_new_test)
                                #print('-----------------------------------------------------')
                                #print(df_new_test)

                            else:
                                pass
                            

                        frames = [df_whole_sprit, df_new_test]
                        df_whole_sprit = pd.concat(frames)

            
                #DataFrame is empty
                else:
                    pass

    print(df_whole_sprit)




    # The next additional way to bring new PLZ into the SQL table because the API-request is just SHIT 

    df_whole_sprit_PLZ_range = df_whole_sprit[[header_all_sprit[3],header_all_sprit[4]]]
    #print(df_whole_sprit_PLZ_range)

    for i in range(len(df_whole_sprit_PLZ_range)):
        #print(i)
        df_units_sprit_Single = df_whole_sprit_PLZ_range.iloc[i,:]

        #print(df_units_sprit_Single)

        df_units_sprit_Single_PLZ = df_units_sprit_Single[df_whole_sprit_PLZ_range.columns[0]]
        df_units_sprit_Single_Location = df_units_sprit_Single[df_whole_sprit_PLZ_range.columns[1]]

        #print(df_units_sprit_Single_PLZ, df_units_sprit_Single_Location )
        obj_Location = Location(postCode=df_units_sprit_Single_PLZ, location=df_units_sprit_Single_Location)

        count_object_loc = obj_Location.AskCountOperator(mydb)

        if(count_object_loc[0][0] < 1):
            obj_Location.InsertSQLOperator(mydb)
        
        del obj_Location




    # Now create Object and fill the sql
    #print("-#------#--###--#--#--####----##---#-##-----#-##--#----#-#---###-------#-#-#--#--##----#----#----#--#-----###---#------#-#-###---")
    #

    counter_Update=0
    counter_Insert=0

    for i in range(len(df_whole_sprit)):
        #print(i)
        df_Station_Single = df_whole_sprit.iloc[i,:]

        #print(df_Station_Single)

        df_regions_sprit_Single_id = df_Station_Single[header_all_sprit[0]]
        df_regions_sprit_Single_name = df_Station_Single[header_all_sprit[1]]
        df_regions_sprit_Single_adress = df_Station_Single[header_all_sprit[2]]
        df_regions_sprit_Single_postalCode = df_Station_Single[header_all_sprit[3]]
        df_regions_sprit_Single_city = df_Station_Single[header_all_sprit[4]]
        df_regions_sprit_Single_latitude = df_Station_Single[header_all_sprit[5]]
        df_regions_sprit_Single_longitude = df_Station_Single[header_all_sprit[6]]
        df_regions_sprit_Single_telephone = df_Station_Single[header_all_sprit[7]]
        df_regions_sprit_Single_mail = df_Station_Single[header_all_sprit[8]]
        df_regions_sprit_Single_website = df_Station_Single[header_all_sprit[9]]
        df_regions_sprit_Single_service = df_Station_Single[header_all_sprit[10]]
        df_regions_sprit_Single_selfService = df_Station_Single[header_all_sprit[11]]
        df_regions_sprit_Single_open = df_Station_Single[header_all_sprit[12]]
        df_regions_sprit_Single_fuelType = df_Station_Single[header_all_sprit[13]]
        df_regions_sprit_Single_amount = df_Station_Single[header_all_sprit[14]]
        df_regions_sprit_Single_label = df_Station_Single[header_all_sprit[15]]
        df_regions_sprit_Single_Type = df_Station_Single[header_all_sprit[16]]
        df_regions_sprit_Single_Code = df_Station_Single[header_all_sprit[17]]

        #print(df_regions_sprit_Single_Code)
        #print(df_units_sprit_Single_PLZ, df_units_sprit_Single_Location )
        obj_Station = Station(code=df_regions_sprit_Single_Code,
        id=df_regions_sprit_Single_id,
        name=df_regions_sprit_Single_name,
        type=df_regions_sprit_Single_Type,
        address=df_regions_sprit_Single_adress,
        postalCode=df_regions_sprit_Single_postalCode,
        city=df_regions_sprit_Single_city,
        latitude=df_regions_sprit_Single_latitude,longitude=
        df_regions_sprit_Single_longitude,
        telephone=df_regions_sprit_Single_telephone,
        mail=df_regions_sprit_Single_mail,
        website=df_regions_sprit_Single_website,
        service=df_regions_sprit_Single_service,
        selfService=df_regions_sprit_Single_selfService,
        open=df_regions_sprit_Single_open, 
        fuelType=df_regions_sprit_Single_fuelType,
        amount=df_regions_sprit_Single_amount,
        label=df_regions_sprit_Single_label)


        obj_Station.FuelId = obj_Station.GetFuelTypeID(mydb)[0][0]
        obj_Station.PLZId = obj_Station.GetPlzID(mydb)[0][0]
        obj_Station.RegionId = obj_Station.GetRegionID(mydb)[0][0]  


        count_object_station = obj_Station.AskCountStation(mydb)

        if(count_object_station[0][0] < 1):
            counter_Insert = counter_Insert + 1
            #func_dump(obj_Station)
            obj_Station.InsertSQLOperator(mydb)
            #print('---------------------------------------------')
        else:
            counter_Update = counter_Update + 1
            obj_Station.UpdateSQLOperator(mydb)
        
        del obj_Station

    #print(" Insert ")
    #print(counter_Insert)
    #print("Update")
    #print(counter_Update)

    if(iq == 0):
        df_testa = df_whole_sprit
    else:
        df_testb = df_whole_sprit

print("'''''''''''''''''''         TEST                  '''''''''''''''''''''''''''''''")
## Test where df-A is different as df-B
df1_str_tuples = df_testa.astype(str).apply(tuple, 1)
df2_str_tuples = df_testb.astype(str).apply(tuple, 1)
df1_values_in_df2_filter = df1_str_tuples.isin(df2_str_tuples)
df2_values_in_df1_filter = df2_str_tuples.isin(df1_str_tuples)
df1_values_not_in_df2 = df_testa[~df1_values_in_df2_filter]
df2_values_not_in_df1 = df_testb[~df2_values_in_df1_filter]
print(df1_values_not_in_df2)
print("########################################")
print(df2_values_not_in_df1)

























































# SicherheitsSave

"""
############################################################################################################
########                    URL for the Regions                     ###############
############################################################################################################

regions_url = 'https://api.e-control.at/sprit/1.0/regions?includeCities=true'
request_region_headers = {'Accept': 'application/json'}
regions_response=requests.get(regions_url, headers=request_region_headers).json()
regions=json.dumps(regions_response)

#df_regions_sprit = pd.DataFrame(columns=("code","type","name"))

complete_dataset=json_normalize(regions_response)

#print(complete_dataset)

list_useful_regions = ["code","type","name"]
list_useful_regions_CoordStreet = ["name","postalCodes","cities"]
df_regions_complete_read = pd.DataFrame(columns=list_useful_regions)
df_Street_complete_Frame = pd.DataFrame(columns=list_useful_regions_CoordStreet)
#print(df_regions_complete_read)


for j in range(len(complete_dataset)):

    df_Bundesland = complete_dataset.loc[j]
    df_Bundesland_subregion =df_Bundesland["subRegions"]

    #print(df_Bundesland)
    
    for i in range(len(df_Bundesland_subregion)):
        regions = df_Bundesland_subregion[i]

        #print(regions)

        regions_code = regions[list_useful_regions[0]]
        regions_type = regions[list_useful_regions[1]]
        regions_name = regions[list_useful_regions[2]]

        print("--------------------------")
        #print(regions)
        #print(regions.keys())
        if(list_useful_regions_CoordStreet[1] in regions.keys()):
            region_CoordName = regions[list_useful_regions_CoordStreet[0]]
            regions_Coordpostcode = regions[list_useful_regions_CoordStreet[1]]
            regions_Coordcities = regions[list_useful_regions_CoordStreet[2]]
        else:
            region_CoordName = regions[list_useful_regions_CoordStreet[0]]
            regions_Coordpostcode is None
            regions_Coordcities is None


        #print()
        
        lstr=[[regions_code,regions_type,regions_name]]
        df_new_entry=pd.DataFrame(lstr,columns=list_useful_regions)
        frames=[df_regions_complete_read,df_new_entry]
        df_regions_complete_read=pd.concat(frames)

    
df_regions_complete_read.reset_index(inplace=True,drop=True)
print(df_regions_complete_read)


"""



"""
SicherheitsSave






for k in get_code_for_regions:

    gasstation_url = "https://api.e-control.at/sprit/1.0/search/gas-stations/by-region?code={gcode}&type={type_pb}&fuelType={fueltype}&includeClosed=true".format(gcode=str(k),type_pb=Insert_type,fueltype="GAS")
    #gasstation_url = 'https://api.e-control.at/sprit/1.0/regions?includeCities=true'
    request_gas_headers = {'Accept': 'application/json'}
    gas_response=requests.get(gasstation_url, headers=request_gas_headers).json()
    gas=json.dumps(gas_response)
    complete_dataset_gas=json_normalize(gas_response)

    lst_adding = []
    #list_var_select_header = ["id","name","location.address","location.postalCode","location.city","location.latitude","location.longitude","contact.telephone","contact.mail","contact.website","offerInformation.service","offerInformation.selfService","open","prices.fuelType","prices.amount","prices.label"]

    #NaNvalues = [np.nan] * len(header_all_sprit)
    NaNvalues = [None] * len(header_all_sprit)
    df_new_test = pd.DataFrame([NaNvalues],columns=(header_all_sprit))
    #print(df_new_test)

   
    #print(type(complete_dataset_gas))
    if not complete_dataset_gas.empty:
        #print("YEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEESSSSSSSSSSSSSSSSSSSSS")
    
        #print(k)
        print(complete_dataset_gas)
        for i in range(len(header_all_sprit_withoutpreis)):

            reiter_name = header_all_sprit_withoutpreis[i]
            #print(reiter_name)

            # Look if the column even exists in the dataframe
            if reiter_name in complete_dataset_gas.columns:
                var = complete_dataset_gas[reiter_name][0]

                if(type(var) is np.bool_):
                    var = str(var)
                else:
                    pass

                #print("reiter:   {a},   Value :    {b}    ".format(a = reiter_name, b = var))
                #print("---------------------------------------------------------------")
                if(reiter_name == header_all_sprit_withoutpreis[-1]):
                    #print(reiter_name)
                    #prices = var[0][0]
                    print(k)

                    var = complete_dataset_gas[str(reiter_name)]
                    #print(var)
                    var_intro_keys = var[0]
                    

                    var_prices_with_keys = var_intro_keys[0]
                    list_of_keys = list(var_prices_with_keys.keys())
                    for j in list_of_keys:

                        prices_key_value = var_prices_with_keys[j]
                        df_new_test_single = pd.DataFrame(data=[prices_key_value],columns=[j],index=[0])
                        df_new_test.update(df_new_test_single)
                    
                else:
                    #pass
                    #print("---------------------------------------------------------------")
                    #print(df_new_test)
                    df_new_test_single = pd.DataFrame(data=[var],columns=[reiter_name],index=[0])
                    df_new_test.update(df_new_test_single)
                    ### Here now we have to include the Type from the API request --> PB or BP
                df_new_test_Type = pd.DataFrame(data=[Insert_type],columns=["Type"],index=[0])
                df_new_test.update(df_new_test_Type)
                df_new_test_code = pd.DataFrame(data=[str(k)],columns=["code"],index=[0])
                df_new_test.update(df_new_test_code)


    

                #print(df_new_test)
                #concat
                

            else:
                pass
            

        frames = [df_whole_sprit, df_new_test]
        df_whole_sprit = pd.concat(frames)

    
    #DataFrame is empty
    else:
        pass

print(df_whole_sprit)



# Now create Object and fill the sql
print("-#------#--###--#--#--####----##---#-##-----#-##--#----#-#---###-------#-#-#--#--##----#----#----#--#-----###---#------#-#-###---")
#
for i in range(len(df_new_test)):
    #print(i)
    df_Station_Single = df_new_test.iloc[i,:]

    #print(df_units_sprit_Single)

    df_regions_sprit_Single_id = df_Station_Single[header_all_sprit[0]]
    df_regions_sprit_Single_name = df_Station_Single[header_all_sprit[1]]
    df_regions_sprit_Single_adress = df_Station_Single[header_all_sprit[2]]
    df_regions_sprit_Single_postalCode = df_Station_Single[header_all_sprit[3]]
    df_regions_sprit_Single_city = df_Station_Single[header_all_sprit[4]]
    df_regions_sprit_Single_latitude = df_Station_Single[header_all_sprit[5]]
    df_regions_sprit_Single_longitude = df_Station_Single[header_all_sprit[6]]
    df_regions_sprit_Single_telephone = df_Station_Single[header_all_sprit[7]]
    df_regions_sprit_Single_mail = df_Station_Single[header_all_sprit[8]]
    df_regions_sprit_Single_website = df_Station_Single[header_all_sprit[9]]
    df_regions_sprit_Single_service = df_Station_Single[header_all_sprit[10]]
    df_regions_sprit_Single_selfService = df_Station_Single[header_all_sprit[11]]
    df_regions_sprit_Single_open = df_Station_Single[header_all_sprit[12]]
    df_regions_sprit_Single_fuelType = df_Station_Single[header_all_sprit[13]]
    df_regions_sprit_Single_amount = df_Station_Single[header_all_sprit[14]]
    df_regions_sprit_Single_label = df_Station_Single[header_all_sprit[15]]
    df_regions_sprit_Single_Type = df_Station_Single[header_all_sprit[16]]
    df_regions_sprit_Single_Code = df_Station_Single[header_all_sprit[17]]

    #print(df_regions_sprit_Single_Code)
    #print(df_units_sprit_Single_PLZ, df_units_sprit_Single_Location )
    obj_Station = Station(code=df_regions_sprit_Single_Code,
    id=df_regions_sprit_Single_id,
    name=df_regions_sprit_Single_name,
    type=df_regions_sprit_Single_Type,
    address=df_regions_sprit_Single_adress,
     postalCode=df_regions_sprit_Single_postalCode,
     city=df_regions_sprit_Single_city,
    latitude=df_regions_sprit_Single_latitude,longitude=
    df_regions_sprit_Single_longitude,
    telephone=df_regions_sprit_Single_telephone,
    mail=df_regions_sprit_Single_mail,
    website=df_regions_sprit_Single_website,
    service=df_regions_sprit_Single_service,
    selfService=df_regions_sprit_Single_selfService,
    open=df_regions_sprit_Single_open, 
    fuelType=df_regions_sprit_Single_fuelType,
    amount=df_regions_sprit_Single_amount,
    label=df_regions_sprit_Single_label)

    count_object_station = obj_Station.AskCountOperator(mydb)

    
    print("###############################################################")
    obj_Station.FuelId = obj_Station.GetFuelTypeID(mydb)[0][0]
    obj_Station.PLZId = obj_Station.GetPlzID(mydb)[0][0]
    obj_Station.RegionId = obj_Station.GetRegionID(mydb)[0][0]


  
    #func_dump(obj_Station)

    if(count_object_station[0][0] < 1):
        obj_Station.InsertSQLOperator(mydb)
    else:
        obj_Station.UpdateSQLOperator(mydb)
    
    del obj_Station





"""