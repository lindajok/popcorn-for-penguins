'''Python script to clean the data'''
import csv
import re

with open('tomato_allrecipes.csv', newline='') as csvfile:
    filereader = csv.reader(csvfile, delimiter=',')
    recipes = []
    for row in filereader:
        recipes.append(row)

recip = []

for recipes in recipes:
    counter = 0
    without_json=[]
    for instruction in recipes:
        counter += 1
        instruction = re.sub(r'{""ing_group"":"', '"', instruction)
        instruction = re.sub(r'"}', '"', instruction)
        instruction = re.sub(r'{""meth_group"":"', '"', instruction)
        if counter > 0:
            without_json.append(instruction)
    recip.append(without_json)

recip = str(recip)

output = open('test.txt', 'w')
output.write(recip)
output.close()

#print(without_json)
#print(without_json[-1])
#print(recip[-1])

