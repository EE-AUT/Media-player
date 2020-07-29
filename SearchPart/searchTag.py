import difflib
from editPart import timeconvert as tc




def find_Closest_to(tags, word):
    suggest = __find__(tags, word)
    for key in difflib.get_close_matches(word, tags):
        suggest = suggest + tags.__find__(key)
        
    # print(suggest.sort())
    suggest = list(set(suggest))
    suggest.sort(key= lambda x: self.tc.to_second(tags[x]))
    return suggest # list
    



def __find__(tags, word):
    suggest = []
    for key in tags:
        if key.find(word) != -1:
            suggest.append(key)
    return suggest