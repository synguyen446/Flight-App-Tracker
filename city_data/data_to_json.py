GROUPS = [['A','B','C','D','E','F','G'],
         ['H','I','J','K','L','M','N','O'],
         ['P','Q','R','S','T','U','V','W','X','Y','Z']]

import json

data ={}
for i in range(3):
    with open(f'cities{i}.txt') as file:
        content = file.readlines()
        for letter in GROUPS[i]:
            city_list = []
            for city in content:
                if city[0].upper() == letter:
                    city_list.append(city.strip())
            data.update(
            {    
                letter:city_list
            })
        
    with open('data.json', 'w') as json_file:
        json.dump(data, json_file) 

print(data)
