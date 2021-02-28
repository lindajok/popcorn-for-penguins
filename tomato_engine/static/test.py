from ast import literal_eval
with open('wtf.txt') as wtf:
    mainlist = [list(literal_eval(line)) for line in wtf]
    print(type(mainlist))
