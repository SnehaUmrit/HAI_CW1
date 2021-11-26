# importing required libraries
import os, json, random
import pandas as pd

# importing functions from classes
from train import intent_classifier
from information_retrieval import cosine_similarity
from identity_management import get_user_name, get_user_likes, get_user_allergies
from meal_recommender import recommend_meal
from information_retrieval import ingredient_search, instruction_search, calories_search, protein_search, get_datetime,description
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
                sim = cosine_similarity(user_intent, user_input, pattern, 2)
                if sim >= max_sim:
                    max_sim = sim
                    #print(max_sim)
                    response = random.choice(intent["responses"])
                    tag = intent['tag']
                    #print('functions: ' + intent['tag'])

                    if max_sim < 0.2:
                        response = random.choice(apology_responses)

        if tag == 'updateUserName':
            name = get_user_name(user_input)
            user_name.append(name)
            response = response.replace('<HUMAN>', name)

        if tag == 'userNameQuery':
            user_name = list(filter(None, user_name))
            if check_non_null('user_name'):
                response = response.replace('<HUMAN>', get_last_non_null('user_name'))
            elif len(user_name) != 0:
                response = response.replace('<HUMAN>', user_name[-1])
            else:
                response = 'I am sorry, you have not told me your name yet!'

        if tag == 'updateTime':
            response = response.replace('<TIME>', get_datetime())

        if tag == 'updateUserFoodPreferences':
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

        if tag == 'noFoodAllergies' and check_non_null('user_likes'):
            user_allergies.append('no-allergies')
            meal = recommend_meal(get_last_non_null('user_likes'), 'no-allergies')
            response = response + ' Would you like to try ' + meal + '?'

        if tag == 'updateUserFoodAllergies':
            allergies = get_user_allergies(user_input)
            # print('allergies: ' + allergies)
            user_allergies.append(allergies)
            user_allergies = list(filter(None, user_allergies))
            # print('l'+str(check_non_null('user_likes')))
            # print(check_non_null('user_allergies'))
            if check_non_null('user_likes'):
                meal = recommend_meal(get_last_non_null('user_likes'), allergies)
                response = response + ' I found the following for you. ' + meal + '?'

        print("Bot: " + response)
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
                    #print(max_sim)
                    if max_sim < 0.4:
                        response = random.choice(apology_responses)

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
                        response = "The instructions for " + row[1]['title'] + " are as follows. " + instructions

                    if calories_search(user_input):
                        response = "The number of calories found in " + row[1]['title'] + " is " + str(row[1]['calories'])

                    if protein_search(user_input):
                        response = "The protein amount found in " + row[1]['title'] + " is " + str(row[1]['proteins'])

                    if description(user_input):
                        response = "Here's what you need to know about " +str(row[1]['title']) + ':' + str(row[1]['description'])

        print("Bot: " + response)
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

                        if max_sim < 0.2:
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
            if deleted_food_item(user_input) is None:
                response = 'Item not found!'
            else:
                response = response.replace('<FOOD_ITEM>', deleted_food_item(user_input))
                food_tracker_delete_item(user_input)

        elif tag == 'deleteAllFoodTracker':
            food_tracker_delete_all()

        elif tag == 'deleteExpiredFoodTracker':
            food_tracker_delete_expired()

        print("Bot: " + response)
        bot.append(response)
    df['user_query'] = pd.Series(user)
    df['bot_text'] = pd.Series(bot)
    df['user_name'] = pd.Series(user_name)
    df['user_likes'] = pd.Series(user_preferences)
    df['user_allergies'] = pd.Series(user_allergies)
    df['topic'] = ''
    df.to_csv(r'out_data/chat_history.csv', mode='a', index=False, header=False)

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


# Chatbot terminal
exit_bot = False
bot_greetings = ["Hello, I am Berry, your virtual sous-chef!", "Hi, My name is Berry! I am your virtual sous-chef!",
                 "Hey, Berry here! I am your virtual sous-chef!"]
user_exits = ['exit', 'quit']
bot_text = random.choice(bot_greetings)
print("Bot: " + bot_text)
# chat_df = pd.read_csv(r'out_data/chat_history.csv')

while not exit_bot:
    user_text = input("User: ")
    if user_text.lower() in user_exits:
        exit_bot = True
        bot_text = "It was nice talking to you. Take care!"
        print("Bot: " + bot_text)
    else:
        get_response(user_text, chat_df)

