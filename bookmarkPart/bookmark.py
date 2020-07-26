import re
import csv
import os





def add_Bookmark(bookmark, session, filename):
    try:
        with open(filename) as csvfile:
            string = csvfile.read()
    except: # file path error
        pass

    new_text = re.sub(session, session + "\n" + bookmark + ",*", string)

    with open(filename, "w") as csvfile:
        csvfile.write(new_text)





if __name__ == "__main__":
    pass
