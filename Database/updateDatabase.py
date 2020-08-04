import re
import csv
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from time import time



def upload_Database(user, filename, filepath):
    scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]


    try:
        creds = ServiceAccountCredentials.from_json_keyfile_name("./Database/json/creds.json", scope)
        client = gspread.authorize(creds)
        spreadsheets = client.list_spreadsheet_files()
        data = get_csvData(filepath)
        for sh in spreadsheets:
            if sh["name"] == user: # there is user spreadsheet
                sh = client.open(user)
                worksheets = sh.worksheets()
                for wsh in worksheets:
                    if wsh.title == filename: # there is worksheet for tags or not
                        sheet = sh.worksheet(filename)
                        sheet.delete_rows(1, len(sheet.get_all_values()))
                        sheet.insert_rows(data)
                        return True
                sheet = sh.add_worksheet(title=filename, rows=10000, cols= 20) # create new worksheet if there in no worksheet for tags
                sheet.insert_rows(data)
                return True
        return False

    except Exception as e:
        print(e)
        return False



# download data base from google sheet
def download_Database(user, filename, filepath):
    scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    
    try:
        creds = ServiceAccountCredentials.from_json_keyfile_name("./Database/json/creds.json", scope)
        client = gspread.authorize(creds)
        sh = client.open(user)
        sheet = sh.worksheet(filename)
        data = sheet.get_all_values()
        return set_csvData(filepath, data) #return result of writing data to csv
    except Exception as e:
        print(e)
        return False
        
        
def get_csvData(filepath):
    data = []
    try:
        with open(filepath) as csvfile:
            file_reader = csv.reader(csvfile, delimiter='#')
            for row in file_reader:
                data.append(row)
        return data
    except Exception as e:
        print(e)
        return None 



def set_csvData(filepath, data):
    try:
        with open(filepath, "w") as csvfile:
            for row in data:
                if len(row) == 2 and row[1] == "":
                    csvfile.write(row[0]+ "\n")
                elif len(row) == 2:
                    csvfile.write(row[0] + "#" + row[1] + "\n")
                elif len(row) == 3:
                    csvfile.write(row[0] + "#" + row[1] + "#" + row[2] + "\n")
        return True
    except Exception as e:
        print(e)
        return False       


# return Worksheet and succesful result
def get_allworksheet(user):
    scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    try:
        creds = ServiceAccountCredentials.from_json_keyfile_name("./Database/json/creds.json", scope)
        client = gspread.authorize(creds)
        spreadsheets = client.list_spreadsheet_files()
        for sh in spreadsheets:
            if sh["name"] == user: # there is user spreadsheet
                sheet = client.open(user)
                sheetAdmin = client.open("ap.mediaplayer@gmail.com")
                worksheets = sheet.worksheets()
                worksheetsGlobal = sheetAdmin.worksheets()
                # Globa
                return worksheets, True, worksheetsGlobal, True

        print("there is no databse for this user")
        try: # if there is no Spreadsheet with user
            sh = client.create(user)
            return [], True, [], False
        except Exception as e: # handle Exception
            print(e)
            return [], False, [], False
        
    except Exception as e:
        print(e)
        return [], False, [], False
        

            
















if __name__ == "__main__":
    pass