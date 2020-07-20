import gspread
from oauth2client.service_account import ServiceAccountCredentials
from time import time





def get_Database():
    scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

    try: 
        start = time()

        creds = ServiceAccountCredentials.from_json_keyfile_name("Database/json/creds.json", scope)
        client = gspread.authorize(creds)
        sheet = client.open("test").sheet1
        data = sheet.get_all_records()

        end = time()

        
        # print(data)
        # print(round(end - start, 2))
        return data

    except:
        print("error occured")
        return None


def exist_Email(Email):
    scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

    try:
        creds = ServiceAccountCredentials.from_json_keyfile_name("Database/json/creds.json", scope)
        client = gspread.authorize(creds)
        sheet = client.open("test").sheet1
        data = sheet.get_all_records()

        for user in data:
            if str(user["Email"]) == str(Email):
                return 1 
        return 0
    except:
        return 2

def add_User(user):
    scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

    try:
        creds = ServiceAccountCredentials.from_json_keyfile_name("Database/json/creds.json", scope)
        client = gspread.authorize(creds)
        sheet = client.open("test").sheet1
        data = sheet.get_all_records()  

        sheet.insert_row(user, len(data) + 2)
        return True

    except:
        return False

                



if __name__ == "__main__":
    print(get_Database())
    
    