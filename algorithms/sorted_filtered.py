# Sort by:
# 0 = alphabetical
# 1 = rating
# 2 = newly released
# 3 = ranking

# Filter by:
# 0 = china
# 1 = egypt
# 2 = greece
# 3 = japan
# 4 = middleeast
# 5 = norway
# 6 = rome
# 7 = lgbtq
# 8 = neurodivergent
# 9 = all games

def get_sorted_filtered(games, rankings):
    # sorted_filtered: sort type: filter type: game id
    sorted_filtered = [[[], [], [], [], [], [], [], [], [], []], 
                       [[], [], [], [], [], [], [], [], [], []], 
                       [[], [], [], [], [], [], [], [], [], []], 
                       [[], [], [], [], [], [], [], [], [], []]]
    
    # Initially sort by ID
    games = sorted(games, key=lambda x: x["id"])
    # Label all games with rankings
    for i in range(9):
        current_rank_ids = sorted(rankings[i], key=lambda x: x[1])

        j = 0
        k = 0
        while (j != len(current_rank_ids) and k != len(games)):
            if current_rank_ids[j][1] == games[k]['id']:
                games[k][f'rank_{i}'] = current_rank_ids[j][0]
                j += 1
                k += 1

            elif current_rank_ids[j][1] > games[k]['id']:
                k += 1
            
            elif current_rank_ids[j][1] < games[k]['id']:
                j += 1
                
    games_filter_list = []
    games_filter_list.append([ game for game in games if 'rank_0' in game ]) # china
    games_filter_list.append([ game for game in games if 'rank_1' in game ]) # egypt
    games_filter_list.append([ game for game in games if 'rank_2' in game ]) # greece
    games_filter_list.append([ game for game in games if 'rank_3' in game ]) # japan
    games_filter_list.append([ game for game in games if 'rank_4' in game ]) # middleeast
    games_filter_list.append([ game for game in games if 'rank_5' in game ]) # norway
    games_filter_list.append([ game for game in games if 'rank_6' in game ]) # rome
    games_filter_list.append([ game for game in games if 'rank_7' in game ]) # lgbtq
    games_filter_list.append([ game for game in games if 'rank_8' in game ]) # neurodivergent
    
    for i in range(9):
        GAME_NAME = [ game for game in games_filter_list[i] if "name" in game ]
        sorted_filtered[0][i] = sorted(GAME_NAME, key=lambda x: x["name"])
        
        GAME_RATING = [ game for game in games_filter_list[i] if "total_rating" in game ]
        sorted_filtered[1][i] = sorted(GAME_RATING, key=lambda x: x["total_rating"], reverse=True)

        GAME_RELEASE = [ game for game in games_filter_list[i] if "first_release_date" in game and game["first_release_date"] < 1731801600 ]
        sorted_filtered[2][i] = sorted(GAME_RELEASE, key=lambda x: x["first_release_date"], reverse=True)
        
        GAME_RANKING = [ game for game in games_filter_list[i] if f"rank_{i}" in game ]
        sorted_filtered[3][i] = sorted(GAME_RANKING, key=lambda x: x[f"rank_{i}"])
        
    GAME_NAME = [ game for game in games if "name" in game ]
    sorted_filtered[0][9] = sorted(GAME_NAME, key=lambda x: x["name"])

    GAME_RATING = [ game for game in games if "total_rating" in game ]
    sorted_filtered[1][9] = sorted(GAME_RATING, key=lambda x: x["total_rating"], reverse=True)

    GAME_RELEASE = [ game for game in games if "first_release_date" in game and game["first_release_date"] < 1731801600 ]
    sorted_filtered[2][9] = sorted(GAME_RELEASE, key=lambda x: x["first_release_date"], reverse=True)
    
    return sorted_filtered