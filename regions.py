from ctypes.wintypes import INT
from email import header
from multiprocessing.sharedctypes import Value
from optparse import Values
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


from Objects import Location, Region


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

print('-------------------------------------------')
#print(engine)


print('----')


#query = db.select([table_Location]) 
#ResultProxy = connection.execute(query)
#ResultSet = ResultProxy.fetchall()
#print(ResultSet)


#Convert to dataframe
#df_test = pd.DataFrame(ResultSet)
#df_test.columns = ResultSet[0].keys()


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



"""

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
print(df_units_sprit)






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


############################################################################################################


regions_url = 'https://api.e-control.at/sprit/1.0/regions?includeCities=true'
request_region_headers = {'Accept': 'application/json'}
regions_response=requests.get(regions_url, headers=request_region_headers).json()
regions=json.dumps(regions_response)

#df_regions_sprit = pd.DataFrame(columns=("code","type","name"))

complete_dataset=json_normalize(regions_response)

#print(complete_dataset)

list_useful_regions = ["code","type","name"]
df_regions_complete_read = pd.DataFrame(columns=list_useful_regions)
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

        lstr=[[regions_code,regions_type,regions_name]]
        df_new_entry=pd.DataFrame(lstr,columns=list_useful_regions)
        frames=[df_regions_complete_read,df_new_entry]
        df_regions_complete_read=pd.concat(frames)

    
df_regions_complete_read.reset_index(inplace=True,drop=True)
#print(df_regions_complete_read)



for i in range(len(df_regions_complete_read)):
    #print(i)
    df_regions_sprit_Single = df_regions_complete_read.iloc[i,:]

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



###############################################################################################################

# And now the big SQL

"""



gasstation_url = "https://api.e-control.at/sprit/1.0/search/gas-stations/by-region?code={gcode}&type={type_pb}&fuelType={fueltype}&includeClosed=true".format(gcode=str(101),type_pb="PB",fueltype="GAS")
#gasstation_url = 'https://api.e-control.at/sprit/1.0/regions?includeCities=true'
request_gas_headers = {'Accept': 'application/json'}
gas_response=requests.get(gasstation_url, headers=request_gas_headers).json()
gas=json.dumps(gas_response)
complete_dataset_gas=json_normalize(gas_response)

print(complete_dataset_gas.keys())
header_all_sprit = ["id","name","location.address","location.postalCode","location.city","location.latitude","location.longitude","contact.telephone","contact.mail","contact.website","offerInformation.service","offerInformation.selfService","open", "fuelType","amount","label"] 
header_all_sprit_withoutpreis = ["id","name","location.address","location.postalCode","location.city","location.latitude","location.longitude","contact.telephone","contact.mail","contact.website","offerInformation.service","offerInformation.selfService","open", "prices"] 


df_whole_sprit = pd.DataFrame(columns=(header_all_sprit))

#print(df_whole_sprit)
#########################

gasstation_url = "https://api.e-control.at/sprit/1.0/search/gas-stations/by-region?code={gcode}&type={type_pb}&fuelType={fueltype}&includeClosed=true".format(gcode=str(101),type_pb="PB",fueltype="GAS")
#gasstation_url = 'https://api.e-control.at/sprit/1.0/regions?includeCities=true'
request_gas_headers = {'Accept': 'application/json'}
gas_response=requests.get(gasstation_url, headers=request_gas_headers).json()
gas=json.dumps(gas_response)
complete_dataset_gas=json_normalize(gas_response)

lst_adding = []
#list_var_select_header = ["id","name","location.address","location.postalCode","location.city","location.latitude","location.longitude","contact.telephone","contact.mail","contact.website","offerInformation.service","offerInformation.selfService","open","prices.fuelType","prices.amount","prices.label"]

NaNvalues = [np.nan] * len(header_all_sprit)
df_new_test = pd.DataFrame([NaNvalues],columns=(header_all_sprit))
#print(df_new_test)

for i in range(len(header_all_sprit_withoutpreis)):

    reiter_name = header_all_sprit_withoutpreis[i]
    var = complete_dataset_gas[reiter_name][0]

    #print("reiter:   {a},   Value :    {b}    ".format(a = reiter_name, b = var))
    #print("---------------------------------------------------------------")
    if(reiter_name == header_all_sprit_withoutpreis[-1]):
        #print(reiter_name)
        #prices = var[0][0]
        var = complete_dataset_gas[str(reiter_name)]
        var_intro_keys = var[0]
        var_prices_with_keys = var_intro_keys[0]
        list_of_keys = list(var_prices_with_keys.keys())
        #print('--')
        #print(var)
        #print('--')
        #print(var)
        #b = var[0]
        #c= b[0]
        #prices_key = list(var.keys())
        #print('-----')
        #print(c.keys())
        #print(var_intro_keys.keys())
        #print(list(var_intro_keys.keys()))
        #print(var_prices_with_keys["fuelType"])
        for j in list_of_keys:
        #    print(j)
            prices_key_value = var_prices_with_keys[j]

         #   print("reiter:   {a},   Value :    {b}    ".format(a = j, b = prices_key_value))

            df_new_test_single = pd.DataFrame(data=[prices_key_value],columns=[j],index=[0])
            print(df_new_test_single)
            df_new_test.update(df_new_test_single)
        
    else:
        #pass
        df_new_test_single = pd.DataFrame(data=[var],columns=[reiter_name],index=[0])
        df_new_test.update(df_new_test_single)

print(df_new_test)
print(df_new_test.columns)






































































"""




############################################################################################################################################################

from sqlalchemy import create_engine, Column, Integer, String, Sequence, Float,PrimaryKeyConstraint, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.sql import *
import os

def connect_db():
    db1 = create_engine("mysql+pymysql://{user}:{pw}@{host}/{db}".format(user=user, pw = password,host=host,db=database))
    return db1
Base = declarative_base()

class PointsOfInterest(Base):
    __tablename__ = "points_of_interest"
    poi_id = Column(Integer, Sequence('poi_id_seq'), primary_key=True)
    name = Column(String)
    build_year = Column(String)
    demolished_year = Column(String)
    address = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    external_url = Column(String)
    image_url = Column(String)
    heritage_status = Column(String)
    current_use = Column(String)
    poi_type = Column(String)
    source = Column(String)
    details = Column(String)
    #Defining One to Many relationships with the relationship function on the Parent Table
    styles = relationship('ArchitecturalStyles', backref = 'points_of_interest',lazy=True,cascade="all, delete-orphan")
    architects = relationship('Architects', backref = 'points_of_interest', lazy=True,cascade="all, delete-orphan")
    categories = relationship('POICategories', backref = 'points_of_interest', lazy=True,cascade="all, delete-orphan")
class ArchitecturalStyles(Base):
    __tablename__="architectural_styles"
    __table_args__ = (
        PrimaryKeyConstraint('poi_id', 'style'),
    )
    poi_id =Column(Integer,ForeignKey('points_of_interest.poi_id'))
    #Defining the Foreign Key on the Child Table
    style = Column(String)
class Architects(Base):
    __tablename__="architects"
    __table_args__ = (
        PrimaryKeyConstraint('poi_id', 'architect_name'),
    )
    poi_id= Column(Integer,ForeignKey('points_of_interest.poi_id'))
    architect_name = Column(String)
class POICategories(Base):
    __tablename__="poi_categories"
    __table_args__ = (
        PrimaryKeyConstraint('poi_id', 'category'),
    )
    poi_id =Column(Integer,ForeignKey('points_of_interest.poi_id'))
    category = Column(String)
engine = connect_db()
PointsOfInterest.__table__.create(bind=engine, checkfirst=True)
ArchitecturalStyles.__table__.create(bind=engine, checkfirst=True)
Architects.__table__.create(bind=engine, checkfirst=True)
POICategories.__table__.create(bind=engine, checkfirst=True)
"""
####################################################################################################################
"""

engine = db.create_engine("mysql+pymysql://{user}:{pw}@{host}/{db}".format(user=user, pw = password,host=host,db=database))

connection = engine.connect()
metadata = db.MetaData()
table_Location = db.Table('tbl_Location', metadata, autoload=True, autoload_with=engine)
table_keys = repr(metadata.tables['tbl_Location'])

# Print the column names
#print(table_Location.columns.keys())
# Print full table metadata
#print()

query = db.update(table_Location)


df_units_sprit.to_sql(
    'tbl_Location',
    con=engine,
    if_exists='replace',
    index=False,
    Location_ID =db.column()

    #keys="Location_ID",
    #chunksize=500,
    #dtype={
    #    "Location_ID": INTEGER,
    #    "Location": VARCHAR(200),
    #    "PLZ": Integer
    #},
    #PRIMARY KEY ("Location_ID")
)

ResultProxy = connection.execute(query,df_units_sprit)

#############################################################################################################################################



"""


################################################################################################################################



    
