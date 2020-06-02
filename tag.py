import csv


class tag:
    def __init__(self, sessNumber):
        self.sessNumber = sessNumber # session number
        self.tagsDict = {} # datas dictionary
        # read datas from csv file and save them in tagDict
        with open(str(sessNumber) + ".csv") as csvfile:
            file_reader = csv.reader(csvfile, delimiter=',')
            self.tagsDict = {rows[0]:self.__getTime__(rows[1]) for rows in file_reader}


    # function for casting time string to seconds
    def __getTime__(self, tim):
        result = 0
        count = 2
        for t in tim.rsplit(":"):
            result = result + float(t) * (60 ** count)
            count = count - 1
        return result
    
    # return time of special tag
    def srch_by_tagName(self, tagName):
        return self.tagsDict[tagName]






if __name__ == "__main__":
    print("testing tag module ...")
    a = tag(1)
    print(a.tagsDict)