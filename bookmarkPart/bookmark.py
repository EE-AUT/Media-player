import re
import csv
import os





# add bookmark to data file and existed tags
def add_Bookmark(bookmark, session, filename):

    file_format = (filename.split("/")[-1]).split(".")[-1]
    if file_format == "csv": # edit tag if file format is csv
        try:
            with open(filename) as csvfile: # open file and get string to add bookmark it
                string = csvfile.read()
        except: # file path error
            pass

        # if there is session in csv file
        if re.search(session, string):
            new_text = re.sub(session, session + "\n" + bookmark + "#*", string)
        # if there not is session in csv file
        else: 
            new_text = string + "\n" + session + "\n" + bookmark + "#*"
        

        # write data to csv
        with open(filename, "w") as csvfile:
            csvfile.write(new_text)








if __name__ == "__main__":
    pass
