import re
import csv
import os




def edit_Tags(befor, after, filename):
    with open(filename) as csvfile:
        string = csvfile.read()

    with open(filename, "w") as csvfile:
        csvfile.write(re.sub(befor+"#", after+"#", string))



if __name__ == "__main__":
    pass