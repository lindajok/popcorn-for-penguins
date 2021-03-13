from ast import literal_eval
with open('tomato_recipes.txt') as recipes:
    recipes_lst = [list(literal_eval(line)) for line in recipes]
    ingredients = []
    for i in range(len(recipes_lst)):
        ings = ''
        for j in range(len(recipes_lst[i][1])):
            ings += recipes_lst[i][1][j] + '*'
            print(recipes_lst[i][1][j])
        ingredients.append(ings)
f = open('ingredients.txt', 'w')
for ingredient in ingredients:
    f.write(ingredient + '@')
f.close()
