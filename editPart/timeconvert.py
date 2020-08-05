import time


# convert time from format to second
def to_second(time):
    _split = time.split(":")

    result = 0
    count = len(_split) - 1
    for t in _split:
        try:
            result = result + int(t) * (60 ** count)
        except:
            pass
        count = count - 1
    return result  # return second


# convert millisecond to time format string using time module
def millis_to_format(millis):
    second = int(millis / 1000)  # milli second to second
    return time.strftime("%H:%M:%S", time.gmtime(second))
