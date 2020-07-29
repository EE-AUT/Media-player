import csv
import difflib



class tag:
    def __init__(self, sessName):
        self.sessName = sessName # session Name
        self.tagsDict = {} # datas dictionary
        # read datas from csv file and save them in tagDict
        with open(str(sessName) + ".csv ") as csvfile:
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


    # find closest keys
    def find_Closest_to(self, word):
        suggest = self.__find__(word)
        for key in difflib.get_close_matches(word, self):
            suggest = suggest + self.__find__(key)
        
        # print(suggest.sort())
        suggest = list(set(suggest))
        suggest.sort(key= lambda x: self.srch_by_tagName(x))
        return suggest # list
    
    
    # find similar words
    def __find__(self, word):
        suggest = []
        for key in self:
            if key.find(word) != -1:
                suggest.append(key)
        return suggest


    # set class iterable
    def __iter__(self):
        return iter(self.tagsDict)







if __name__ == "__main__":
    print("testing tag module ...")
    a = tag(1)




# create thread for fiding the tag
# try except for reading line of file