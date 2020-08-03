import gspread
from oauth2client.service_account import ServiceAccountCredentials
from time import time
import csv


def get_Database():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets",
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

    try:

        creds = ServiceAccountCredentials.from_json_keyfile_name(
            "./Database/json/creds.json", scope)
        client = gspread.authorize(creds)
        sheet = client.open("test").sheet1
        data = sheet.get_all_records()

        return data
    except:
        return None


def exist_Email(Email):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets",
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

    try:
        creds = ServiceAccountCredentials.from_json_keyfile_name(
            "./Database/json/creds.json", scope)
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
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets",
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

    try:
        creds = ServiceAccountCredentials.from_json_keyfile_name(
            "./Database/json/creds.json", scope)
        client = gspread.authorize(creds)
        sheet = client.open("test").sheet1
        data = sheet.get_all_records()

        sheet.insert_row(user, len(data) + 2)
        return True

    except Exception as e:
        print(e)
        return False


def Change_password(oldPass, NewPass):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets",
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

    try:
        creds = ServiceAccountCredentials.from_json_keyfile_name(
            "./Database/json/creds.json", scope)
        client = gspread.authorize(creds)
        sheet = client.open("test").sheet1
        address = sheet.find('#'+oldPass)
        sheet.update_cell(address.row, address.col, '#'+NewPass)
        Edit_user(NewPass)
        return True

    except:
        print('OH')
        return False

def Edit_user(newPass):
    with open("LoginPart/User.csv") as csvfile:
        oldstring = csvfile.read()
        Newstring = oldstring.split(',')[0]+','+newPass

    with open("LoginPart/User.csv", "w") as csvfile:
        csvfile.write(Newstring)

if __name__ == "__main__":
    print(get_Database())
