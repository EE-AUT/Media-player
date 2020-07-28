import time



def to_second(time):
    _split = time.split(":")

    result = 0
    count = len(_split) - 1
    for t in _split:
        try:
            result = result + int(t) * (60 ** count)
        except Exception as e:
            print(e)
        count = count - 1
    return result


def millis_to_format(millis):
    second = int(millis / 1000)
    return time.strftime("%H:%M:%S", time.gmtime(second))
