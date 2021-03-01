from ast import literal_eval
with open('tomato_recipes.txt') as recipes:
    recipes_lst = [list(literal_eval(line)) for line in recipes]
    titles = []
    for i in range(len(recipes_lst)):
        titles.append(recipes_lst[i][0])

f = open('titles.txt', 'w')
for title in titles:
    f.write(title + '*')
f.close()

