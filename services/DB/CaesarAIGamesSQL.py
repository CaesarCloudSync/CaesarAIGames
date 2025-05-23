import time
import json
import sqlite3
import subprocess
from urllib.parse import urlparse
from typing import Any, Callable, Union
from services.Constants.CaesarAIGamesConstants import CaesarAIGamesConstants
class CaesarAIGamesSQL:
    def __init__(self) -> None:
        # Makes SQL connection to remote server.
        self.connection = sqlite3.connect(CaesarAIGamesConstants.DATABASE_NAME, isolation_level=None)
        self.connection.cursor().execute("PRAGMA foreign_keys = ON")


    def check_exists(self,result :Any):
        # Checks if an entity exists from an SQL Command.
        try:
            if len(result) == 0:
                return False
            else:
                return True
        except Exception as poe:
            return False
    
    def fetch(self,result:Any):
        # Callback function that fetches data after an SQL command is run self.runcommand("SELECT * FROM names WHERE name LIKE 'bill'",self.fetch)
        return result
    
    def json_to_sql(self,datajson :Union[dict,list]):
        # Converts JSON to SQL.
        if type(datajson) == list: 
            columns = str(tuple(datajson[0].keys())).replace("'","")
            values = str(tuple(tuple(data.values())  for data in datajson))[1:-1]
            return columns,values
        elif type(datajson) == dict:
            columns = str(tuple(datajson.keys())).replace("'","")
            values = str(tuple(datajson.values())).replace("'","")
            return columns,values
        else:
            print("JSON is invalid data shape.")
            return None,None
    def run_command(self,sqlcommand : str = None,result_function : Callable =None,datatuple : tuple =None,filename :str = None,verbose:int=0):
        # Executes SQL Command or takes SQL file as input.
        #if verbose == 1:
            #if self.connection.is_connected():
            #    db_Info = self.connection.get_server_info()
            #    print("Connected to MySQL Server version ", db_Info)
        if sqlcommand == None and filename == None:
            print("Please input an SQL command or SQL filename.")
        else:
            if filename != None:
               with open(filename) as f:
                   sqlcommand = f.read()
            
            cursor = self.connection.cursor()
            #print(datatuple)
            if datatuple:
                cursor.execute(sqlcommand,datatuple)
            else:
                cursor.execute(sqlcommand)
           

            result = cursor.fetchall()
                
            
            if result_function != None:
                new_result = result_function(result)
            elif result_function == None:
                new_result = None

                #self.connection.commit()
            if verbose == 1:
                print("SQL command executed.")
                return new_result
            else:
                return new_result

    def sql_to_json(self,table,sqldata :tuple):
        # Convert SQL tuple to json
        columnsinfo = self.run_command(f"DESCRIBE {table}",self.fetch)
        columns = [col[0] for col in columnsinfo]
        #print(sqldata)
        final_json = []
        for data in sqldata:
            record = {}
            for ind in range(len(data)):
                record.update({data[ind]: columns[ind]} )
            final_json.append(record)
        
        return {table:final_json}




