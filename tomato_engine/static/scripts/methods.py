from ast import literal_eval
with open('tomato_recipes.txt') as recipes:
    recipes_lst = [list(literal_eval(line)) for line in recipes]
    methods = []
    for i in range(len(recipes_lst)):
        met = ''
        for j in range(len(recipes_lst[i][2])):
            met += recipes_lst[i][2][j] + '*'
            print(recipes_lst[i][2][j])
        methods.append(met)
f = open('methods.txt', 'w')
for method in methods:
    f.write(method + '@')
f.close()
