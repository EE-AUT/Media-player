import difflib
from editPart import timeconvert as tc
import re


def find_Closest_to(tags, word):
    suggest = __find__(tags, word)
    # tags = {text.lower(): val for text, val in tags.items()} # change all text to lower case
    for key in difflib.get_close_matches(word, tags.keys()):
        suggest = {**suggest, **(__find__(tags, key))}
    result = {}
    for key in suggest:  # delete repeated
        if not key in result.keys():
            result.update({key: suggest[key]})
    # sort tags by time
    result = {text: time for text, time in sorted(
        result.items(), key=lambda item: tc.to_second(item[1]))}
    return result  # dict


def __find__(tags, word):
    suggest = {}
    for key in tags:
        if key.lower().find(word.lower()) != -1:
            suggest.update({key: tags[key]})
    return suggest  # return dict
