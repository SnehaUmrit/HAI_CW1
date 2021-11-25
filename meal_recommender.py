import os
import pandas as pd

from information_retrieval import cosine_similarity


# takes in user likes and allergies to recommend a meal from available dataset
def recommend_meal(user_likes, user_allergies):

    max_sim = float('-inf')
    if len(user_allergies) == 0:
        user_allergies = 'no-allergies'
    else:
        user_allergies = str(user_allergies)
    user_likes = str(user_likes)

    meal = ''

    for file in os.listdir(r"data/information_retrieval"):
        filepath = r"data/information_retrieval" + os.sep + file
        csv_file = pd.read_csv(filepath)
        csv_file = csv_file.dropna()
        for row in csv_file.iterrows():
            categories = str(row[1]['categories']) + str(row[1]['ingredients'])
            sim = cosine_similarity('information retrieval', user_likes, categories, 2)
            # print(sim)
            if sim >= max_sim:
                max_sim = sim
                if user_allergies == 'no-allergies':
                    meal = row[1]['title']
                else:
                    if not (user_allergies in row[1]['ingredients']):
                        meal = row[1]['title']
    # print(max_sim)
    return meal

#m = recommend_meal('chicken', 'yellow onion')
#print(m)
