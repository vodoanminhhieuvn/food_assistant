recipe_parts = [{'entity': 'ingredient', 'start': -47, 'end': -43, 'value': 'rice', 'extractor': 'RegexEntityExtractor'},
                {'entity': 'or', 'start': -42, 'end': -40,
                    'value': 'or', 'extractor': 'RegexEntityExtractor'},
                {'entity': 'ingredient', 'start': -39, 'end': -34,
                    'value': 'water', 'extractor': 'RegexEntityExtractor'},
                {'entity': 'or', 'start': -23, 'end': -21,
                    'value': 'or', 'extractor': 'RegexEntityExtractor'},
                {'entity': 'preparation_technique', 'start': -20, 'end': -13,
                    'value': 'boiling', 'extractor': 'RegexEntityExtractor'},
                {'entity': 'or', 'start': -12, 'end': -10,
                    'value': 'or', 'extractor': 'RegexEntityExtractor'},
                {'entity': 'preparation_technique', 'start': -9, 'end': -3,
                 'value': 'drying', 'extractor': 'RegexEntityExtractor'}]
search_list = []
for index, val in enumerate(recipe_parts):
    if (val["entity"] == "or"
        and (index == 0 or index == len(recipe_parts)-1
             or recipe_parts[index+1]["entity"] == "or")):
        del recipe_parts[index]


print(list(map(lambda x: x["value"], recipe_parts)))
branch_list = []
index = 0
while index < len(recipe_parts):
    bl_len = len(branch_list)
    if recipe_parts[index]["entity"] == "or":
        if recipe_parts[index-1]["entity"] == recipe_parts[index+1]["entity"]:
            for i in range(bl_len):
                raw_item = branch_list[0]
                del raw_item[-1]
                branch_list.append(raw_item+[recipe_parts[index-1]])
                branch_list.append(raw_item+[recipe_parts[index+1]])
                del branch_list[0]
            index += 1
    else:
        if bl_len == 0:
            branch_list.append([recipe_parts[index]])
        else:
            for item in branch_list:
                item.append(recipe_parts[index])
    index += 1

for item in branch_list:
    search_list.append(item[0]["value"])
    for i in range(1, len(item)):
        search_list[-1] += " "+item[i]["value"]

print(search_list)
