
#from itertools import count
#from turtle import st


class Location:
    species = "Location name"
    def __init__(self, postCode, location):

        self.postCode = postCode
        self.location = location

    def AskCountLocation(self, connector):
        mycursor = connector.cursor()

        sql = "SELECT COUNT(*) FROM tbl_Location WHERE  (PLZ=%s OR PLZ IS NULL) AND (Location=%s OR Location IS NULL)"
        val = (self.postCode ,self.location)
        mycursor.execute(sql,val)
        myresult_count = mycursor.fetchall()
        connector.commit()
        mycursor.close()
        return(myresult_count)


    def InsertSQLLocation(self,connector):

        mycursor = connector.cursor()
        sql = "INSERT INTO tbl_Location (PLZ,Location) VALUES (%s, %s)"
        val = (self.postCode, self.location)
        mycursor.execute(sql,val)
        myresult_count = mycursor.fetchall()
        connector.commit()
        mycursor.close()

    def __del__(self):
        pass



class Region:
    species = "Region name"
    def __init__(self, code, name):

        self.code = code
        self.name = name

    def AskCountRegion(self, connector):
        mycursor = connector.cursor()

        sql = "SELECT COUNT(*) FROM tbl_spritregions WHERE region_Code = %s"
        val = (self.code,)
        mycursor.execute(sql,val)
        myresult_count = mycursor.fetchall()
        connector.commit()
        mycursor.close()
        return(myresult_count)
    

    def InsertSQLRegion(self,connector):
        mycursor = connector.cursor()
        sql = "INSERT INTO tbl_spritregions (region_Code,region_Name) VALUES (%s,%s)"
        val = (self.code, self.name)
        mycursor.execute(sql,val)
        connector.commit()
        mycursor.close()
 

    def UpdateSQLRegion(self,connector):
        mycursor = connector.cursor()
        sql = "UPDATE tbl_spritregions SET region_Name=%s WHERE region_Code=%s"
        val = (self.name, self.code)
        mycursor.execute(sql,val)
        connector.commit()

    def __del__(self):
        pass


class SType:
    species = "Type name"
    def __init__(self, type):

        self.type = type

    def AskCountType(self, connector):
        mycursor = connector.cursor()

        sql = "SELECT COUNT(*) FROM tbl_Type WHERE (Type=%s OR Type IS NULL)"
        val = (self.type,)
        mycursor.execute(sql,val)
        myresult_count = mycursor.fetchall()
        connector.commit()
        mycursor.close()
        return(myresult_count)


    def InsertSQLType(self,connector):

        mycursor = connector.cursor()
        sql = "INSERT INTO tbl_Type (Type) VALUES (%s)"
        val = (self.type,)
        mycursor.execute(sql,val)
        myresult_count = mycursor.fetchall()
        connector.commit()
        mycursor.close()

    def __del__(self):
        pass

class Station:

    species = "Station name"
    def __init__(self, id, name, type, address, postalCode, city, latitude,longitude, telephone, mail, website,service, selfService, open, fuelType,amount, label,
    regioncode, statusID,datetiming):

        self.regioncode = regioncode
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
        self.StatusID = statusID
        self.DateT = datetiming
        self.FuelId=""
        self.PLZId = ""
        self.RegionId = ""
        self.TypeID = ""

   

    def GetPlzID(self, connector):

        mycursor = connector.cursor()

        plz_streetid = "SELECT Location_ID FROM tbl_Location WHERE (PLZ=%s or PLZ IS NULL) and (Location=%s OR Location IS NULL)"
        var_id = (self.postCode, self.city)
        mycursor.execute(plz_streetid, var_id)
        myresult_plzID = mycursor.fetchall()
        connector.commit()
        mycursor.close()
        return(myresult_plzID)

    def GetRegionID(self, connector):
        
        mycursor = connector.cursor()

        region_id = "SELECT region_ID FROM tbl_spritregions WHERE region_Code=%s"
        var = (self.regioncode,)
        mycursor.execute(region_id, var)
        myresult_regionID = mycursor.fetchall()
        connector.commit()
        mycursor.close()
        return(myresult_regionID)

    def GetFuelTypeID(self, connector):
        
        mycursor = connector.cursor()

        fuelid = "SELECT Fueltype_ID FROM tbl_fueltype WHERE fueltype=%s"
        var = (self.fuelType,)
        mycursor.execute(fuelid, var)
        myresult_fuelID = mycursor.fetchall()
        connector.commit()
        mycursor.close()
        return(myresult_fuelID)

    def GetTypeID(self, connector):
        
        mycursor = connector.cursor()

        typeid = "SELECT Type_ID FROM tbl_Type WHERE Type=%s"
        var = (self.type,)
        mycursor.execute(typeid, var)
        myresult_typeID = mycursor.fetchall()
        connector.commit()
        mycursor.close()
        return(myresult_typeID)


    def AskCountStation(self, connector):
        mycursor = connector.cursor()

        sql = "SELECT COUNT(*) FROM tbl_Station WHERE StationID = %s AND Type_Id=%s AND fueltype_Id=%s"

        val = (self.id,self.TypeID,self.FuelId)
        mycursor.execute(sql,val)
        myresult_count = mycursor.fetchall()
        connector.commit()
        mycursor.close()
        return(myresult_count)

    #def GetStatusID(self, connector):
    #    
    #    mycursor = connector.cursor()

    #    fuelid = "SELECT Fueltype_ID FROM tbl_fueltype WHERE fueltype=%s"
    #    var = (self.fuelType,)
    #    mycursor.execute(fuelid, var)
    #    myresult_fuelID = mycursor.fetchall()
    #    connector.commit()
    #    return(myresult_fuelID)

    
    def InsertSQLStation(self,connector):
        mycursor = connector.cursor()
        sql = "INSERT INTO tbl_Station (StationID,station_name,station_adress,Plz_Id,latitiude,longitude,telephone,mail,website,service,selfService,open,fueltype_Id,price,label,Region_Id, Type_Id,Status_Id,DateTime) VALUES (%s, %s,%s,%s, %s,%s,%s, %s,%s,%s, %s,%s,%s, %s,%s,%s,%s,%s,%s)"
        val = (self.id, self.name, self.address, self.PLZId, self.latitude, self.longitude, self.telephone, self.mail, self.website, self.service, self.selfService, self.open,
        self.FuelId, self.amount, self.label, self.RegionId, self.TypeID,self.StatusID,self.DateT)
        mycursor.execute(sql,val)
        connector.commit()
        mycursor.close()
 
    def UpdateSQLStation(self,connector):
        mycursor = connector.cursor()
        sql = "UPDATE tbl_Station SET station_name=%s, station_adress=%s, Plz_Id =%s ,latitiude=%s ,longitude =%s,telephone =%s,mail =%s,website=%s,service=%s,selfService=%s,open=%s,fueltype_Id=%s,price=%s,label=%s,Region_Id=%s,Status_Id=%s,DateTime=%s WHERE StationID=%s AND fueltype_Id=%s AND Type_Id=%s"
        val = (self.name, self.address, self.PLZId, self.latitude, self.longitude, self.telephone, self.mail, self.website, self.service, self.selfService,
        self.open, self.FuelId, self.amount, self.label, self.RegionId,self.StatusID,self.DateT, self.id, self.FuelId,self.TypeID)
        mycursor.execute(sql,val)
        connector.commit()
        mycursor.close()


    def __del__(self):
        pass



class StationUpdate:

    species = "Update for Station"
    def __init__(self, id, type, fuelType, statusID):

       
        self.id = id
        self.fuelType = fuelType
        self.type = type
        self.statusID = statusID
        

    def UpdateSQLStationUpdate(self,connector):
        mycursor = connector.cursor()
        sql = "UPDATE tbl_Station SET Status_Id=%s WHERE StationID=%s AND fueltype_Id=%s AND Type_Id=%s"
        val = (self.statusID, self.id, self.fuelType, self.type)
        mycursor.execute(sql,val)
        connector.commit()
        mycursor.close()

    def __del__(self):
        pass






































"""

class Location:
    species = "Location name"
    def __init__(self, postCode, location):

        self.postCode = postCode
        self.location = location

    def AskCountLocation(self, connector):
        mycursor = connector.cursor()

        sql = "SELECT COUNT(*) FROM tbl_Location WHERE  (PLZ=%s OR PLZ IS NULL) AND (Location=%s OR Location IS NULL)"
        val = (self.postCode ,self.location)
        mycursor.execute(sql,val)
        myresult_count = mycursor.fetchall()
        connector.commit()
        return(myresult_count)


    def InsertSQLLocation(self,connector):

        mycursor = connector.cursor()
        sql = "INSERT INTO tbl_Location (PLZ,Location) VALUES (%s, %s)"
        val = (self.postCode, self.location)
        mycursor.execute(sql,val)
        myresult_count = mycursor.fetchall()
        connector.commit()
        connector.close()


     
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

"""