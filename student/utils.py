
def sanitizer(number, lenght):
    numstr = str(number)
    if len(numstr) < lenght:
        while len(numstr) <  lenght:
            numstr = '0'   +numstr
    return numstr