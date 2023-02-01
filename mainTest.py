def positive(x):
    return x > 0
_list = list(filter(positive, [10, -31,  0, -15, 16]))
print(_list)