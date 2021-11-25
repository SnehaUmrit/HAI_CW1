# importing required libraries
import os, json, random
import pandas as pd

# importing functions from classes
from train import intent_classifier
from information_retrieval import cosine_similarity
from identity_management import get_user_name, get_user_likes, get_user_allergies
from meal_recommender import recommend_meal
from information_retrieval import ingredient_search, instruction_search, calories_search, sugar_search, protein_search, \
    sodium_search, carbs_search,get_datetime,description, get_similarity
from food_tracker import food_tracker_add, deleted_food_item,date_parser, \
    food_item_parser, food_tracker_fetch_all, food_tracker_fetch_expired, food_tracker_delete_item, food_tracker_delete_expired, food_tracker_delete_all

def get_response(user_input, df):
    max_sim = float('-inf')
    response = ""
    user = [user_input]
    bot = []
    user_name = []
    user_preferences = []
    user_allergies = []
    topic = []

    apology_responses = ["I am sorry. I do not understand you :(", "Can you please try rephrasing?",
                         "I am sorry. I don't know :(", "I am sorry. I have no idea."]

    # classifying user intent by calling intent_classifier function
    user_intent = intent_classifier(user_input)
    # print(user_intent)
    if user_intent == 'small talk':
        for file in os.listdir(r"data/small_talk"):
            filepath = r"data/small_talk" + os.sep + file
            json_file = json.load(open(filepath, "r"))
            for intent in json_file["intents"]:
                for pattern in intent["patterns"]:
                    sim = cosine_similarity(user_intent, user_input, pattern, 3)
                    if sim >= max_sim:
                        max_sim = sim
                        response = random.choice(intent["responses"])
                        #print('functions: ' + intent['tag'])

                        if intent['tag'] == 'updateUserName':
                            name = get_user_name(user_input)
                            user_name.append(name)
                            response = response.replace('<HUMAN>', name)

                        if intent['tag'] == 'userNameQuery':
                            user_name = list(filter(None, user_name))
                            if len(user_name) == 0:
                                response = 'I am sorry, you have not told me your name yet!'
                            else:
                                response = response.replace('<HUMAN>', user_name[-1])

                        if intent['tag'] == 'updateTime':
                            response = response.replace('<TIME>', get_datetime())

                        if intent['tag'] == 'updateUserFoodPreferences':
                            # get user preferences and allergies when stated by user
                            likes = get_user_likes(user_input)
                            #print(likes)
                            user_preferences.append(likes)
                            user_preferences = list(filter(None, user_preferences))

                            allergies = get_user_allergies(user_input)
                            #print('allergies: '+ allergies)
                            user_allergies.append(allergies)
                            user_allergies = list(filter(None, user_allergies))

                            if check_non_null('user_allergies') :
                                allergies = get_last_non_null('user_allergies')
                                if allergies == 'no-allergies':
                                    meal = recommend_meal(get_last_non_null('user_likes'),'no-allergies')
                                    response = response.replace('<FOOD_ITEMS>', meal)
                                else:
                                    meal = recommend_meal(get_last_non_null('user_likes'),
                                                          get_last_non_null('user_allergies'))
                                    response = response.replace('<FOOD_ITEMS>', meal)
                            else:
                                response = "Do you have any allergies?"

                        if intent['tag'] == 'noFoodAllergies' and check_non_null('user_likes'):
                            user_allergies.append('no-allergies')
                            meal = recommend_meal(get_last_non_null('user_likes'), 'no-allergies')
                            response = response + ' Would you like to try ' + meal + '?'

                        if intent['tag'] == 'updateUserFoodAllergies':
                            allergies = get_user_allergies(user_input)
                            # print('allergies: ' + allergies)
                            user_allergies.append(allergies)
                            user_allergies = list(filter(None, user_allergies))
                            # print('l'+str(check_non_null('user_likes')))
                            # print(check_non_null('user_allergies'))
                            if check_non_null('user_likes'):
                                meal = recommend_meal(get_last_non_null('user_likes'), allergies)
                                response = response + ' I found the following for you. ' + meal + '?'

                        if sim < 0.2:
                            response = random.choice(apology_responses)

        # print("Bot: " + response)
        bot.append(response)

    elif user_intent == 'information retrieval':
        for file in os.listdir(r"data/information_retrieval"):
            filepath = r"data/information_retrieval" + os.sep + file
            csv_file = pd.read_csv(filepath)
            for row in csv_file.iterrows():
                pattern = str(row[1]['title']) + str(row[1]['categories'])
                sim = cosine_similarity(user_intent, user_input, pattern, 4)
                if sim >= max_sim:
                    max_sim = sim
                    ingredients = []
                    instructions = []
                    if ingredient_search(user_input):
                        # print(row[1]['title'])
                        ingredients = row[1]['ingredients'].replace('[', '')
                        ingredients = ingredients.replace(']', '')
                        ingredients = ingredients.replace("'", '')
                        ingredients = ingredients.replace('"', '')
                        # ingredients = ingredients.split("'")
                        response = "The ingredients for " + row[1]['title'] + " are " + ingredients

                    if instruction_search(user_input):
                        # print(row[1]['title'])
                        instructions = row[1]['instructions'].replace('[', '')
                        instructions = instructions.replace(']', '')
                        instructions = instructions.replace("'", '')
                        instructions = instructions.replace('"', '')
                        instructions = instructions.replace("'", "\n")
                        response = "The instructions for " + row[1]['title'] + "are as follows. " + instructions

                    if calories_search(user_input):
                        response = "The number of calories found in " + row[1]['title'] + " is " + str(row[1]['calories'])

                    if sugar_search(user_input):
                        response = "Amount of sugar in " + row[1]['title'] + " is " + str(row[1]['sugar'])

                    if sodium_search(user_input):
                        response = "The sodium amount in " + row[1]['title'] + " is " + str(row[1]['sodium'])

                    if sodium_search(user_input):
                        response = "The protein amount found in " + row[1]['title'] + " is " + str(row[1]['sodium'])

                    if carbs_search(user_input):
                        response = "The amount of carbohydrates found in " + row[1]['title'] + " is " + str(row[1]['carbohydrate'])

                    if description(user_input):
                        response = "Here's what you need to know about " +str(row[1]['title']) + ':' + str(row[1]['description'])

                    #if item_search(user_input):
                    #   response = "Would you like to try " + str(row[1]['title']) + "?"

                    if sim < 0.2:
                        response = random.choice(apology_responses)

        # print("Bot: " + response)
        bot.append(response)

    elif user_intent == 'food tracker':
        for file in os.listdir(r"data/food_tracker"):
            filepath = r"data/food_tracker" + os.sep + file
            json_file = json.load(open(filepath, "r"))
            tag = ''
            for intent in json_file["intents"]:
                for pattern in intent["patterns"]:
                    sim = cosine_similarity(user_intent, user_input, pattern, 1)
                    if sim >= max_sim:
                        max_sim = sim
                        response = random.choice(intent["responses"])
                        tag = intent['tag']

                        if sim < 0.2:
                            response = random.choice(apology_responses)
        # print(tag)
        if tag == 'updateFoodTracker':
            response = response.replace('<EXP_DATE>', str(date_parser(user_input)))
            response = response.replace('<FOOD_ITEM>', food_item_parser(user_input))
            food_tracker_add(user_input)

        elif tag == 'fetchFoodTrackerAll':
            fetched_items = food_tracker_fetch_all()
            if len(fetched_items) == 0:
                response = 'Sorry,no items found!'
            else:
                response = response.replace('<FETCH_ITEMS>', fetched_items)

        elif tag == 'fetchFoodTrackerExpired':
            fetched_items = food_tracker_fetch_expired()
            if len(fetched_items) == 0:
                response = 'No expired items found!'
            else:
                response = response.replace('<FETCH_ITEMS>', fetched_items)

        elif tag == 'deleteItemFoodTracker':
            food_tracker_delete_item(user_input)
            if deleted_food_item(user_input) is None:
                response = 'Item not found!'
            else:
                response = response.replace('<FOOD_ITEM>', deleted_food_item(user_input))

        elif tag == 'deleteAllFoodTracker':
            food_tracker_delete_all()

        elif tag == 'deleteExpiredFoodTracker':
            food_tracker_delete_expired()

        bot.append(response)
    df['user_query'] = pd.Series(user)
    df['bot_text'] = pd.Series(bot)
    df['user_name'] = pd.Series(user_name)
    df['user_likes'] = pd.Series(user_preferences)
    df['user_allergies'] = pd.Series(user_allergies)
    df['topic'] = ''
    df.to_csv(r'out_data/chat_history.csv', mode='a', index=False, header=False)
    return response

# creating a csv file for chat history
chat_df = pd.DataFrame()
chat_df['user_query'] = ''
chat_df['bot_text'] = ''
chat_df['user_name'] = ''
chat_df['user_likes'] = ''
chat_df['user_allergies'] = ''
chat_df['topic'] = ''
chat_df.to_csv(r'out_data/chat_history.csv', index=False)

def check_non_null(fieldname):
    df = pd.read_csv(r'out_data/chat_history.csv')
    flag = len(df[fieldname].value_counts()) > 0
    return flag

def get_last_non_null(fieldname):
    df = pd.read_csv(r'out_data/chat_history.csv')
    df = df[fieldname].dropna()
    item_list = []
    for each in df:
        item_list.append(each)
    return item_list[-1]


filepath = r'benchmark_data.csv'
file = pd.read_csv(filepath)
chat_df = pd.read_csv(r'out_data/chat_history.csv')

user_intent = []
expected_ans = []
actual_answer = []

for row in file.iterrows():
    user_query = row[1]['user_query']
    user_intent = row[1]['user_intent']
    expected_ans.append(row[1]['bot_answer'])
    actual_answer.append(get_response(user_query, chat_df))
    # print(actual_answer)


# sim2 = get_similarity('information retrieval', str(expected_ans), str(actual_answer), 1, 'manhattan')
# print('Similarity using manhattan distance: ' + str(sim2))

# sim3 = get_similarity('information retrieval', str(expected_ans), str(actual_answer), 1, 'jaccard')
# print('Similarity using jaccard: ' + str(sim3))

sim4 = get_similarity('information retrieval', str(expected_ans), str(actual_answer), 1, 'euclidean')
print('Similarity using euclidean distance: ' + str(sim4))

sim1 = cosine_similarity('information retrieval', str(expected_ans), str(actual_answer), 1)
print('Cosine Similarity: ' + str(sim1))

