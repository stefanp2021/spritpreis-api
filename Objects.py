
#from itertools import count
#from turtle import st


class Location:
    species = "Location name"
    def __init__(self, postCode, location):

        self.postCode = postCode
        self.location = location

    def AskCountOperator(self, connector):
        mycursor = connector.cursor()

        sql = "SELECT COUNT(*) FROM tbl_Location WHERE PLZ = %s AND Location = %s"
        val = (self.postCode ,self.location)
        mycursor.execute(sql,val)
        myresult_count = mycursor.fetchall()
        connector.commit()
        return(myresult_count)


    def InsertSQLOperator(self,connector):

        if(self.postCode is None and self.location is None):
            mycursor = connector.cursor()
            sql = "SELECT COUNT(*) FROM tbl_Location WHERE PLZ IS NULL AND Location IS NULL"
            mycursor.execute(sql)
            myresult_count = mycursor.fetchall()
            connector.commit()
            if (myresult_count[0][0] < 1):
                mycursor = connector.cursor()
                sql = "INSERT INTO tbl_Location (PLZ,Location) VALUES (%s, %s)"
                val = (self.postCode, self.location)
                mycursor.execute(sql,val)
                connector.commit()
            else:
                pass
            
        else:

            if(self.location is None):
                mycursor = connector.cursor()
                sql = "SELECT COUNT(*) FROM tbl_Location WHERE PLZ =%s AND Location IS NULL"
                val = (self.postCode,)
                mycursor.execute(sql,val)
                myresult_count = mycursor.fetchall()
                connector.commit()
                if (myresult_count[0][0] < 1):
                    mycursor = connector.cursor()
                    sql = "INSERT INTO tbl_Location (PLZ,Location) VALUES (%s, %s)"
                    val = (self.postCode, self.location)
                    mycursor.execute(sql,val)
                    connector.commit()
                else:
                    pass
            else:
                mycursor = connector.cursor()
                sql = "INSERT INTO tbl_Location (PLZ,Location) VALUES (%s, %s)"
                val = (self.postCode, self.location)
                mycursor.execute(sql,val)
                connector.commit()
 

    def __del__(self):
        pass




class Region:
    species = "Region name"
    def __init__(self, code, type, name):

        self.code = code
        self.type = type
        self.name = name

    def AskCountOperator(self, connector):
        mycursor = connector.cursor()

        sql = "SELECT COUNT(*) FROM tbl_spritregions WHERE region_Code = %s"
        val = (self.code,)
        mycursor.execute(sql,val)
        myresult_count = mycursor.fetchall()
        connector.commit()
        return(myresult_count)
    

    def InsertSQLOperator(self,connector):
        mycursor = connector.cursor()
        sql = "INSERT INTO tbl_spritregions (region_Code,region_Type,region_Name) VALUES (%s, %s,%s)"
        val = (self.code, self.type, self.name)
        mycursor.execute(sql,val)
        connector.commit()
 

    def UpdateSQLOperator(self,connector):
        mycursor = connector.cursor()
        sql = "UPDATE tbl_spritregions SET region_Type=%s,region_Name=%s WHERE region_Code=%s"
        val = (self.type, self.name, self.code)
        mycursor.execute(sql,val)
        connector.commit()


    def __del__(self):
        pass

class Station:

    species = "Station name"
    def __init__(self, code, id, name, type, address, postalCode, city, latitude,longitude, telephone, mail, website,service, selfService, open, fuelType,amount, label ):

        self.code = code
        self.id = id
        self.name = name
        self.type = type
        self.address = address
        self.postCode = postalCode
        self.city = city
        self.latitude = latitude
        self.longitude = longitude
        self.telephone = telephone
        self.mail = mail
        self.website = website
        self.service = service
        self.selfService = selfService
        self.open = open
        self.fuelType = fuelType
        self.amount = amount
        self.label = label
        self.FuelId=""
        self.PLZId = ""
        self.RegionId = ""

    def AskCountStation(self, connector):
        mycursor = connector.cursor()

        sql = "SELECT COUNT(*) FROM tbl_Station WHERE StationID = %s AND Type=%s AND fueltype_Id=%s"

        val = (self.id,self.type,self.FuelId)
        mycursor.execute(sql,val)
        myresult_count = mycursor.fetchall()
        connector.commit()
        return(myresult_count)
    

    def InsertSQLOperator(self,connector):
        mycursor = connector.cursor()
        sql = "INSERT INTO tbl_Station (StationID,station_name,station_adress,Plz_Id,latitiude,longitude,telephone,mail,website,service,selfService,open,fueltype_Id,amount,label,Region_Id, Type) VALUES (%s, %s,%s,%s, %s,%s,%s, %s,%s,%s, %s,%s,%s, %s,%s,%s,%s)"
        val = (self.id, self.name, self.address, self.PLZId, self.latitude, self.longitude, self.telephone, self.mail, self.website, self.service, self.selfService, self.open,
        self.FuelId, self.amount, self.label, self.RegionId, self.type)
        mycursor.execute(sql,val)
        connector.commit()
 

    def UpdateSQLOperator(self,connector):
        mycursor = connector.cursor()
        sql = "UPDATE tbl_Station SET station_name=%s, station_adress=%s, Plz_Id =%s ,latitiude=%s ,longitude =%s,telephone =%s,mail =%s,website=%s,service=%s,selfService=%s,open=%s,fueltype_Id=%s,amount=%s,label=%s,Region_Id=%s, Type=%s WHERE StationID=%s AND fueltype_Id=%s AND Type=%s"
        val = (self.name, self.address, self.PLZId, self.latitude, self.longitude, self.telephone, self.mail, self.website, self.service, self.selfService,
        self.open, self.FuelId, self.amount, self.label, self.RegionId,self.type, self.id, self.FuelId, self.type)
        mycursor.execute(sql,val)
        connector.commit()


    def GetPlzID(self, connector):

        mycursor = connector.cursor()

        plz_streetid = "SELECT Location_ID FROM tbl_Location WHERE PLZ=%s and Location=%s"
        var = (self.postCode, self.city)
        mycursor.execute(plz_streetid, var)
        myresult_plzID = mycursor.fetchall()
        connector.commit()
        return(myresult_plzID)

    def GetRegionID(self, connector):
        
        mycursor = connector.cursor()

        region_id = "SELECT region_ID FROM tbl_spritregions WHERE region_Code=%s and region_Type=%s"
        var = (self.code,self.type)
        mycursor.execute(region_id, var)
        myresult_regionID = mycursor.fetchall()
        connector.commit()
        return(myresult_regionID)

    def GetFuelTypeID(self, connector):
        
        mycursor = connector.cursor()

        fuelid = "SELECT Fueltype_ID FROM tbl_fueltype WHERE fueltype=%s"
        var = (self.fuelType,)
        mycursor.execute(fuelid, var)
        myresult_fuelID = mycursor.fetchall()
        connector.commit()
        return(myresult_fuelID)

    def __del__(self):
        pass
