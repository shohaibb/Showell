import json

def get_rankings():
    with open('igdb_games.json', 'r') as file:
        games = json.load(file)
        
    with open('igdb_keywords.json', 'r') as file:
        keywords = json.load(file)
        
    query_CHINA = ""
    query_EGYPT = ""
    query_GREECE = ""
    query_JAPAN = ""
    query_MIDDLEEAST = ""
    query_NORWAY = ""
    query_ROME = ""

    with open('culture_term_lists/china.txt') as file:
        for line in file:
            query_CHINA += line.strip() + " "

    with open('culture_term_lists/egypt.txt') as file:
        for line in file:
            query_EGYPT += line.strip() + " "
            
    with open('culture_term_lists/greece.txt') as file:
        for line in file:
            query_GREECE += line.strip() + " "
            
    with open('culture_term_lists/japan.txt') as file:
        for line in file:
            query_JAPAN += line.strip() + " "
            
    with open('culture_term_lists/middle_east.txt') as file:
        for line in file:
            query_MIDDLEEAST += line.strip() + " "
            
    with open('culture_term_lists/norway.txt') as file:
        for line in file:
            query_NORWAY += line.strip() + " "
            
    with open('culture_term_lists/rome.txt') as file:
        for line in file:
            query_ROME += line.strip() + " "
            
    query_LGBTQ = ""
    query_NEURODIVERGENT = ""

    with open('identity_term_lists/lgbtq.txt') as file:
        for line in file:
            query_LGBTQ += line.strip() + " "
            
    with open('identity_term_lists/neurodivergent.txt') as file:
        for line in file:
            query_NEURODIVERGENT += line.strip() + " "
            
    # Turning keywords into a dictionary for later use
    keywords_dict = {}
    for keyword in keywords:
        keywords_dict[keyword['id']] = keyword['name']

    letters = "abcdefghijklmnopqrstuvwxyz-"

    # DATA PREPROCESSING

    # 1. Concatenating storyline, summary, and keywords
    # 2. Only allowing lowercase letters + hyphen

    # GAME ID -> TEXT
    CLEANED_DATA = {}

    for game in games:
        FULL_TEXT = "" #FULL GAME TEXT
        GAME_TEXT = "" #FINAL GAME TEXT
        
        if 'summary' in game:
            FULL_TEXT += game['summary'] + " "
            
        if 'storyline' in game:
            FULL_TEXT += game['storyline'] + " "
            
        if 'keywords' in game:
            KEYWORD_LIST = game['keywords']
            for keyword_id in KEYWORD_LIST:
                FULL_TEXT += ''.join(keywords_dict[keyword_id].split()) + " "
                
        for word in FULL_TEXT.split():
            CURRENT_WORD = ''.join(char for char in word.lower() if char in letters)
            if len(CURRENT_WORD) > 0:
                GAME_TEXT += CURRENT_WORD + " "
                
        if len(GAME_TEXT) > 0:
            CLEANED_DATA[game['id']] = GAME_TEXT
            
    import numpy as np
    import pandas as pd
    pd.set_option('display.max_rows', None)
    from sklearn.feature_extraction.text import TfidfVectorizer

    GAME_IDS = list(CLEANED_DATA.keys())
    GAME_TEXTS = list(CLEANED_DATA.values())

    VECTORIZER = TfidfVectorizer()
    TFIDF_MATRIX = VECTORIZER.fit_transform(GAME_TEXTS)

    query_vector_CHINA = VECTORIZER.transform([query_CHINA])
    query_vector_EGYPT = VECTORIZER.transform([query_EGYPT])
    query_vector_GREECE = VECTORIZER.transform([query_GREECE])
    query_vector_JAPAN = VECTORIZER.transform([query_JAPAN])
    query_vector_MIDDLEEAST = VECTORIZER.transform([query_MIDDLEEAST])
    query_vector_NORWAY = VECTORIZER.transform([query_NORWAY])
    query_vector_ROME = VECTORIZER.transform([query_ROME])
    query_vector_LGBTQ = VECTORIZER.transform([query_LGBTQ])
    query_vector_NEURODIVERGENT = VECTORIZER.transform([query_NEURODIVERGENT])

    from sklearn.metrics.pairwise import cosine_similarity

    similarities_CHINA = cosine_similarity(query_vector_CHINA, TFIDF_MATRIX)
    similarities_EGYPT = cosine_similarity(query_vector_EGYPT, TFIDF_MATRIX)
    similarities_GREECE = cosine_similarity(query_vector_GREECE, TFIDF_MATRIX)
    similarities_JAPAN = cosine_similarity(query_vector_JAPAN, TFIDF_MATRIX)
    similarities_MIDDLEEAST = cosine_similarity(query_vector_MIDDLEEAST, TFIDF_MATRIX)
    similarities_NORWAY = cosine_similarity(query_vector_NORWAY, TFIDF_MATRIX)
    similarities_ROME = cosine_similarity(query_vector_ROME, TFIDF_MATRIX)
    similarities_LGBTQ = cosine_similarity(query_vector_LGBTQ, TFIDF_MATRIX)
    similarities_NEURODIVERGENT = cosine_similarity(query_vector_NEURODIVERGENT, TFIDF_MATRIX)

    games_ranked_CHINA = similarities_CHINA.argsort()[0][::-1]
    games_ranked_EGYPT = similarities_EGYPT.argsort()[0][::-1]
    games_ranked_GREECE = similarities_GREECE.argsort()[0][::-1]
    games_ranked_JAPAN = similarities_JAPAN.argsort()[0][::-1]
    games_ranked_MIDDLEEAST = similarities_MIDDLEEAST.argsort()[0][::-1]
    games_ranked_NORWAY = similarities_NORWAY.argsort()[0][::-1]
    games_ranked_ROME = similarities_ROME.argsort()[0][::-1]
    games_ranked_LGBTQ = similarities_LGBTQ.argsort()[0][::-1]
    games_ranked_NEURODIVERGENT = similarities_NEURODIVERGENT.argsort()[0][::-1]
    
    CHINA_RANKINGS = []
    for rank, idx in enumerate(games_ranked_CHINA, 1):
        GAME_ID = GAME_IDS[idx]
        score = similarities_CHINA[0, idx]
        CHINA_RANKINGS.append((rank, GAME_ID))
        
    EGYPT_RANKINGS = []
    for rank, idx in enumerate(games_ranked_EGYPT, 1):
        GAME_ID = GAME_IDS[idx]
        score = similarities_EGYPT[0, idx]
        EGYPT_RANKINGS.append((rank, GAME_ID))
        
    GREECE_RANKINGS = []
    for rank, idx in enumerate(games_ranked_GREECE, 1):
        GAME_ID = GAME_IDS[idx]
        score = similarities_GREECE[0, idx]
        GREECE_RANKINGS.append((rank, GAME_ID))
        
    JAPAN_RANKINGS = []
    for rank, idx in enumerate(games_ranked_JAPAN, 1):
        GAME_ID = GAME_IDS[idx]
        score = similarities_JAPAN[0, idx]
        JAPAN_RANKINGS.append((rank, GAME_ID))
        
    MIDDLEEAST_RANKINGS = []
    for rank, idx in enumerate(games_ranked_MIDDLEEAST, 1):
        GAME_ID = GAME_IDS[idx]
        score = similarities_MIDDLEEAST[0, idx]
        MIDDLEEAST_RANKINGS.append((rank, GAME_ID))
        
    NORWAY_RANKINGS = []
    for rank, idx in enumerate(games_ranked_NORWAY, 1):
        GAME_ID = GAME_IDS[idx]
        score = similarities_NORWAY[0, idx]
        NORWAY_RANKINGS.append((rank, GAME_ID))
        
    ROME_RANKINGS = []
    for rank, idx in enumerate(games_ranked_ROME, 1):
        GAME_ID = GAME_IDS[idx]
        score = similarities_ROME[0, idx]
        ROME_RANKINGS.append((rank, GAME_ID))
        
    LGBTQ_RANKINGS = []
    for rank, idx in enumerate(games_ranked_LGBTQ, 1):
        GAME_ID = GAME_IDS[idx]
        score = similarities_LGBTQ[0, idx]
        LGBTQ_RANKINGS.append((rank, GAME_ID))
        
    NEURODIVERGENT_RANKINGS = []
    for rank, idx in enumerate(games_ranked_NEURODIVERGENT, 1):
        GAME_ID = GAME_IDS[idx]
        score = similarities_NEURODIVERGENT[0, idx]
        NEURODIVERGENT_RANKINGS.append((rank, GAME_ID))
        
    return [
        CHINA_RANKINGS,
        EGYPT_RANKINGS,
        GREECE_RANKINGS,
        JAPAN_RANKINGS,
        MIDDLEEAST_RANKINGS,
        NORWAY_RANKINGS,
        ROME_RANKINGS,
        LGBTQ_RANKINGS,
        NEURODIVERGENT_RANKINGS
    ]