import json
import math

with open('igdb_games.json', 'r') as file:
    games = json.load(file)
    
with open('igdb_keywords.json', 'r') as file:
    keywords = json.load(file)
    
# text: game id -> summary + storyline
game_text = {}
# tfidfs: game id -> term -> tf-idf
tfidfs = {}
# ndwet: term -> number of documents with each term (ndwet)
ndwet = {}
# tagged_games: game id -> term/keyword -> TF-IDF/max TF-IDF (?)
tagged_games = {}
# keywords_dict: keyword id -> keyword(s)
keywords_dict = {}
# game_categories: game id -> categories [(category, category value/weight)]
game_categories = {}

letters = "abcdefghijklmnopqrstuvwxyz-"
ignore_list = []

with open('ignore_list.txt', 'r') as file:
    for line in file:
        ignore_list.append(line.strip())
ignore_list.append("")

for game in games:
    text = ""
    if 'storyline' in game:
        text += game['storyline'] + " "
    if 'summary' in game:
        text += game['summary'] + " "
    if 'storyline' in game or 'summary' in game:
        game_text[game['id']] = text
        
for id in game_text:
    cleaned_text = []
    text = game_text[id].split()
    for i in range(len(text)):
        text[i] = text[i].lower()
        text[i] = ''.join(char for char in text[i] if char in letters)
        
        if text[i] not in ignore_list:
            cleaned_text.append(text[i])

    game_text[id] = cleaned_text

for id in game_text:
    text = list(set(game_text[id]))

    for term in text:
        if term not in ndwet:
            ndwet[term] = 1
        else:
            ndwet[term] += 1

for id in game_text:
    tfidfs[id] = {}
    
    text = game_text[id]
    
    for term in text:
        if term not in tfidfs[id]:
            tfidfs[id][term] = 1
        else:
            tfidfs[id][term] += 1
            
    for term in tfidfs[id]:
        tfidfs[id][term] = (math.log(tfidfs[id][term]) + 1) * (math.log((len(game_text) + 1) / (ndwet[term] + 1)) + 1)

for keyword in keywords:
    keywords_dict[keyword['id']] = keyword['name']

for game in games:
    game_id = game['id']
    
    if game_id in game_text:
        tagged_games[game_id] = tfidfs[game_id]
        
    if 'keywords' in game:
        if game_id not in tagged_games:
            tagged_games[game_id] = {}
            
        keyword_list = game['keywords']
        for keyword_id in keyword_list:
            tagged_games[game_id][keywords_dict[keyword_id]] = 20
            
term_lists = []
term_list_CHINA = []
term_list_EGYPT = []
term_list_GREECE = []
term_list_JAPAN = []
term_list_MIDDLEEAST = []
term_list_NORWAY = []
term_list_ROME = []

with open('culture_term_lists/china.txt') as file:
    for line in file:
        term_list_CHINA.append(line.strip())

with open('culture_term_lists/egypt.txt') as file:
    for line in file:
        term_list_EGYPT.append(line.strip())
        
with open('culture_term_lists/greece.txt') as file:
    for line in file:
        term_list_GREECE.append(line.strip())
        
with open('culture_term_lists/japan.txt') as file:
    for line in file:
        term_list_JAPAN.append(line.strip())
        
with open('culture_term_lists/middle_east.txt') as file:
    for line in file:
        term_list_MIDDLEEAST.append(line.strip())
        
with open('culture_term_lists/norway.txt') as file:
    for line in file:
        term_list_NORWAY.append(line.strip())
        
with open('culture_term_lists/rome.txt') as file:
    for line in file:
        term_list_ROME.append(line.strip())
        
term_lists.append(term_list_CHINA)
term_lists.append(term_list_EGYPT)
term_lists.append(term_list_GREECE)
term_lists.append(term_list_JAPAN)
term_lists.append(term_list_MIDDLEEAST)
term_lists.append(term_list_NORWAY)
term_lists.append(term_list_ROME)

# C, E, G, J, M, N, R
counts = [0 for i in range(7)]

for id in tagged_games:
    game_categories[id] = []
    # C, E, G, J, M, N, R
    values = [0 for i in range(7)]
    for term in tagged_games[id]:
        for i in range(7):
            if term in term_lists[i]:
                values[i] += tagged_games[id][term]
    
    for i in range(7):
        if values[i] >= 20:
            game_categories[id].append((i, values[i]))
            counts[i] += 1

print(f"China: {counts[0]}")
print(f"Egypt: {counts[1]}")
print(f"Greece: {counts[2]}")
print(f"Japan: {counts[3]}")
print(f"Middle east: {counts[4]}")
print(f"Norway: {counts[5]}")
print(f"Rome: {counts[6]}")