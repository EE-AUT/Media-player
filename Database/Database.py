import gspread
from oauth2client.service_account import ServiceAccountCredentials
from time import time
import csv


# get all data base for user infomation
def get_Database():
    # scops of gspread to access us using below apis
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets",
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

    try:

        creds = ServiceAccountCredentials.from_json_keyfile_name(
            "./Database/json/creds.json", scope)
        client = gspread.authorize(creds)
        sheet = client.open("Users").sheet1
        data = sheet.get_all_records()

        return data  # return users information as a dictionary
    except:
        return None


# check email existance in databse
def exist_Email(Email):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets",
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

    try:
        creds = ServiceAccountCredentials.from_json_keyfile_name(
            "./Database/json/creds.json", scope)
        client = gspread.authorize(creds)
        sheet = client.open("Users").sheet1
        data = sheet.get_all_records()

        for user in data:
            if str(user["Email"]) == str(Email):
                return 1  # return true
        return 0  # if there is not
    except:
        return 2  # handle internet fault


# add user using in signup part
def add_User(user):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets",
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

    try:
        creds = ServiceAccountCredentials.from_json_keyfile_name(
            "./Database/json/creds.json", scope)
        client = gspread.authorize(creds)
        sheet = client.open("Users").sheet1
        data = sheet.get_all_records()

        sheet.insert_row(user, len(data) + 2)  # add user to end row
        return True

    # handle connection fault
    except:
        return False


# change password functiob ysing in change password part
def Change_password(oldPass, NewPass):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets",
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

    try:
        creds = ServiceAccountCredentials.from_json_keyfile_name(
            "./Database/json/creds.json", scope)
        client = gspread.authorize(creds)
        sheet = client.open("Users").sheet1
        address = sheet.find('#'+oldPass)
        sheet.update_cell(address.row, address.col, '#' +
                          NewPass)  # Update password here
        Edit_user(NewPass)  # edit user information in user.csv
        return True

    # handle connection fault
    except:
        return False

# edit information of user


def Edit_user(newPass):
    with open("./LoginPart/User.csv") as csvfile:
        oldstring = csvfile.read()
        Newstring = oldstring.split(',')[0]+','+newPass

    with open("./LoginPart/User.csv", "w") as csvfile:
        csvfile.write(Newstring)


def Delete_Account(Mediaplayer, Email):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets",
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

    try:
        creds = ServiceAccountCredentials.from_json_keyfile_name(
            "./Database/json/creds.json", scope)
        client = gspread.authorize(creds)
        sheet = client.open("Users").sheet1
        address = sheet.find(Email)
        sheet.delete_row(address.row)
        Mediaplayer.Logout()
        return True
    except:  # Handle connection fault
        return False
