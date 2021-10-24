import requests
import json

file = open("./data/chicken.json")

data = json.load(file)

print(data["hits"][0]["recipe"]["label"])

# print(data)


# ingredients = {
#     "chicken",
#     "fish",
#     "egg",
#     "beaf",
#     "banana",
# }

# for ingredient in ingredients:

#     params = {
#         "q": f"{ingredient}",
#         "app_id": "d736f71a",
#         "app_key": "5a61563f39257241ba253b7e87328f5a",
#         "type": "public",
#     }

#     res = requests.get(url="https://api.edamam.com/api/recipes/v2", params=params)
#     res.raise_for_status()
#     jsonData = res.json()

#     import json

# with open(f"{ingredient}.json", "w") as writeFile:
#     json.dump(jsonData, writeFile)

#     print(jsonData["hits"][0]["recipe"]["label"])
