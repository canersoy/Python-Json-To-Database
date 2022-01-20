import json
from dbOperations import dbOperations
from collections import Counter

class userOperations:
    #Init dbOperations class with instance of config from input dict config, 
    #jsonData as empty dict, insertIntoQuery as empty str,
    #tableId from tableId, dbOp from dBOperations class
    def __init__(self,config,tableId):
        self.config = config
        self.jsonData = {}
        self.insertIntoQuery = ""
        self.tableId = tableId
        self.dbOp = dbOperations(config,tableId)

    #Read JSON file
    def __parseJsonFile(self):
        json_file = open(self.config["DEFAULT"]["json_file"])
        self.jsonData = json.load(json_file)
    
    #Dynamically create a new Insert Into query for each user in the JSON file
    #and exectute it
    def __insertUserData(self):
        for user in self.jsonData:
            self.insertIntoQuery = f"""
                INSERT INTO user_{self.tableId}
                    (email,
                    name_surname,
                    emailuserlk,
                    usernamelk,
                    birth_year,
                    birth_month,
                    birth_day,
                    country,
                    isActive)
                VALUES
                    ({user["email"]},
                    {user["profile"]["name"]},
                    {1 if sum((Counter(user["email"])&Counter(user["username"])).values()) >= 3 else 0},
                    {1 if user["username"] in user["profile"]["name"].split() else 0},
                    {user["profile"]["dob"].split("-")[0]},
                    {user["profile"]["dob"].split("-")[1]},
                    {user["profile"]["dob"].split("-")[2]},
                    {user["profile"]["address"].split(", ")[2]},
                    {1});
                """
            self.dbOp.__executeInsertIntoTableQuery(self.insertIntoQuery)
        self.dbOp.__closeDB()
    
    def readJsonAndInsertUserData(self):
        self.__parseJsonFile()
        self.__insertUserData()