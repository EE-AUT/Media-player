import re
import csv
import os


# using re module for finding and editing tag
def edit_Tags(befor, after, filename):
    file_format = (filename.split("/")[-1]).split(".")[-1]
    if file_format == "csv":  # edit tag if file format is csv
        with open(filename) as csvfile:
            string = csvfile.read()

        with open(filename, "w") as csvfile:
            csvfile.write(re.sub(befor, after, string))  # save edited string

