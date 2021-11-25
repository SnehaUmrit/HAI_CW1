# importing required libraries
import re, csv
import pandas as pd

from information_retrieval import cosine_similarity

def get_user_name(user_input):
    texts = ["My name is (.*)", "I am (.*)", "It is (.*)", "People call me (.*)", "This is (.*)", "I'm (.*)"]
    response = ''

    for text in texts:
        text = text.lower()
        user_input = user_input.lower()
        regex = re.search(text, user_input)
        if regex:
            response = re.findall(text, user_input)

    response = str(response)
    response = response.replace('[', '')
    response = response.replace(']', '')
    response = response.replace("'", '')
    response = response.capitalize()
    return response


def get_user_likes(user_input):
    patterns = ["I like (.*)", "I love (.*)", "I would like (.*)", "I would love (.*)", "I would like a dish with (.*)",
                "Anything (.*)", "I would love a dish with (.*)", "I would like to have anything with (.*)",
                "I would like a meal with (.*)", "I would like anything with (.*)"]

    user_likes = ''
    max_sim = float('-inf')

    for pattern in patterns:
        sim = cosine_similarity('small talk', user_input, pattern, 2)

        if sim >= max_sim:
            max_sim = sim
            # user_likes.append(user_input)
            user_likes = re.findall(pattern.lower(), user_input.lower())

    user_likes = str(user_likes)
    user_likes = user_likes.replace('[', '')
    user_likes = user_likes.replace(']', '')
    user_likes = user_likes.replace("'", '')
    return user_likes


# r = get_user_likes('Anything vegan')
# print(r)

def get_user_allergies(user_input):
    patterns = ["I am allergic to (.*)",
                "I dislike (.*)",
                "I do not like (.*)",
                "I cannot have (.*)",
                "I cannot eat (.*)",
                "Nothing with (.*)",
                "I am (.*) intolerant"]

    user_allergies = ''
    max_sim = float('-inf')

    for pattern in patterns:
        sim = cosine_similarity('small talk', user_input, pattern, 2)
        if sim >= max_sim:
            max_sim = sim
            # user_allergies.append(user_input)
            user_allergies = re.findall(pattern.lower(), user_input.lower())

    user_allergies = str(user_allergies)
    user_allergies = user_allergies.replace('[', '')
    user_allergies = user_allergies.replace(']', '')
    user_allergies = user_allergies.replace("'", '')
    return user_allergies

# r = get_user_allergies('i am allergic to soy')
# print(r)



