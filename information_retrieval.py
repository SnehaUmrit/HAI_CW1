# Importing required libraries
import nltk, os, json, random
import numpy
import numpy as np
import pandas as pd
from nltk.util import ngrams
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
from scipy import spatial
from math import log10
import sys, warnings
from datetime import datetime
from scipy.spatial import distance

if not sys.warnoptions:
    warnings.simplefilter("ignore")

# Global variables
sb_stemmer = SnowballStemmer('english')
english_stopwords = stopwords.words('English')
tokenizer = nltk.RegexpTokenizer(r"\w+")


# Term-frequency Inverse Document Frequency for any number of vectors
def tfidf_weighting(*vectors):
    N = len(vectors)
    tfidf_vectors = [np.zeros(len(vectors[0])) for vector in vectors]
    for i in range(len(vectors[0])):

        term_booleans = []
        for j in range(len(vectors)):
            term_booleans.append(vectors[j][i] != 0)
        n = sum(term_booleans)

        for j in range(len(vectors)):
            frequency = vectors[j][i]
            tfidf = log10(1 + frequency) * log10(N / n)
            tfidf_vectors[j][i] = tfidf
    return tfidf_vectors


def logfreq_weighting(vector):
    lf_vector = []
    for frequency in vector:
        lf_vector.append(log10(1 + frequency))
    return np.array(lf_vector)


def cosine_similarity(intent, string_1, string_2, ngram):
    strings = [string_1, string_2]

    # Tokenising and removing punctuation
    tokens = []
    for string in strings:
        tokens.append(tokenizer.tokenize(string))

    # Removing stopwords in select dataset only and normalising casing
    docs = []
    for token in tokens:
        if intent == "information retrieval":
            docs.append([word.lower() for word in token if word not in english_stopwords])
        else:
            docs.append([word.lower() for word in token])

    # Performing stemming
    stemmed_docs = []
    for doc in docs:
        stemmed_docs.append([sb_stemmer.stem(word) for word in doc])
    docs = stemmed_docs

    if ngram == '2':
        # Generating bigram document
        bigram_docs = []
        for doc in docs:
            bigram_docs.extend(list(ngrams(doc, 2)))
        docs = bigram_docs

    if ngram == '3':
        # Generating trigram document
        trigram_docs = []
        for doc in docs:
            trigram_docs.extend(list(ngrams(doc, 3)))
        docs = trigram_docs

    if ngram == '4':
        # Generating 4-gram document
        fourgram_docs = []
        for doc in docs:
            fourgram_docs.extend(list(ngrams(doc, 4)))
        docs = fourgram_docs

    # Creating vocabulary
    vocab = []
    for doc in docs:
        for item in doc:
            if item not in vocab:
                vocab.append(item)

                # Creating bag-of-word
    bow = []
    for doc in docs:
        vector = np.zeros(len(vocab))
        for item in doc:
            index = vocab.index(item)
            vector[index] += 1

        bow.append(vector)
    # print(vocab)
    # print(bow)
    query = bow[0]
    bow = dict(d1=bow[1])
    for d in bow.keys():
        try:
            sim = 1 - spatial.distance.cosine(query, bow[d])
        except:
            sim = 0
    # print(sim)
    return sim


# cosine_similarity("food tracker", "add expiration date for flour on 2022/02/15", "Add expiration date for flour on 2021/11/9 ", 1)
# cosine_similarity("information retrieval", 'cheese and bread', "hello who are you", 2)

# r = cosine_similarity("food recommender", "i like cheese and bread", "i like cheese", '2')
# print(r)
# r = cosine_similarity("food recommender", "i like cheese and bread", "i like cheese", '3')
# print(r)
# r = cosine_similarity("food recommender", "i like cheese and bread", "i like cheese", '4')
# print(r)
# r = cosine_similarity("small talk", "hello how are you", "hello how are you", '2')
# print(r)
# r = cosine_similarity("small talk", "hello how are you", "hello how are you", '3')
# print(r)
# r = cosine_similarity("small talk", "hello how are you", "hello how are you", '4')
# print(r)

def ingredient_search(user_input):
    ingredients_search = ["ingredients", "ingredient", "cooking items", "baking items"]
    find_ing = False

    for i in ingredients_search:
        if i.lower() in user_input.lower():
            find_ing = True

    return find_ing


def item_search(user_input):
    items_list = ['like', 'love', 'likes']
    find_item = False

    for i in items_list:
        if i.lower() in user_input.lower():
            find_item = True

    return find_item


def description(user_input):
    items_list = ['What is', 'What are']
    find_item = False

    for i in items_list:
        if i.lower() in user_input.lower():
            find_item = True

    return find_item


def instruction_search(user_input):
    instructions_search = ["instructions", "give me the recipe", "can you tell me the recipe for",
                           "can i have the preparation instructions for", 'meal', 'dish', 'food', "recipe", "recipes",
                           "how to"]
    find_ins = False

    for j in instructions_search:
        if j in user_input:
            find_ins = True

    return find_ins


def calories_search(user_input):
    calories_list = ["calories", "nutrients", "how many calories", "number of calories"]
    find_cal = False

    for i in calories_list:
        if i in user_input:
            find_cal = True

    return find_cal


def sugar_search(user_input):
    sugar_list = ["sugar", "sugars"]
    find_sug = False

    for i in sugar_list:
        if i in user_input:
            find_sug = True

    return find_sug


def protein_search(user_input):
    protein_list = ["protein", "proteins"]
    find_pro = False

    for i in protein_list:
        if i in user_input:
            find_pro = True

    return find_pro


def sodium_search(user_input):
    sodium_list = ["sodium", "sodiums"]
    find_sod = False

    for i in sodium_list:
        if i in user_input:
            find_sod = True

    return find_sod


def carbs_search(user_input):
    carbs_list = ["carb", "carbs", "carbohydrate", "carbohydrates"]
    find_carb = False

    for i in carbs_list:
        if i in user_input:
            find_carb = True

    return find_carb


def get_datetime():
    now = datetime.now()
    day = datetime.today().strftime('%A')
    dt = now.strftime("%B %d %Y %H:%M")
    return str(day) + ", " + str(dt)


def manhattan(vector_1, vector_2):
    diff = abs(vector_1 - vector_2)
    return diff.sum()


def get_similarity(intent, string_1, string_2, ngram, metric):
    strings = [string_1, string_2]

    # Tokenising and removing punctuation
    tokens = []
    for string in strings:
        tokens.append(tokenizer.tokenize(string))

    # Removing stopwords in select dataset only and normalising casing
    docs = []
    for token in tokens:
        if intent == "information retrieval":
            docs.append([word.lower() for word in token if word not in english_stopwords])
        else:
            docs.append([word.lower() for word in token])

    # Performing stemming
    stemmed_docs = []
    for doc in docs:
        stemmed_docs.append([sb_stemmer.stem(word) for word in doc])
    docs = stemmed_docs

    if ngram == '2':
        # Generating bigram document
        bigram_docs = []
        for doc in docs:
            bigram_docs.extend(list(ngrams(doc, 2)))
        docs = bigram_docs

    if ngram == '3':
        # Generating trigram document
        trigram_docs = []
        for doc in docs:
            trigram_docs.extend(list(ngrams(doc, 3)))
        docs = trigram_docs

    if ngram == '4':
        # Generating 4-gram document
        fourgram_docs = []
        for doc in docs:
            fourgram_docs.extend(list(ngrams(doc, 4)))
        docs = fourgram_docs

    # Creating vocabulary
    vocab = []
    for doc in docs:
        for item in doc:
            if item not in vocab:
                vocab.append(item)

                # Creating bag-of-word
    bow = []
    for doc in docs:
        vector = np.zeros(len(vocab))
        for item in doc:
            index = vocab.index(item)
            vector[index] += 1

        bow.append(vector)

    bow = tfidf_weighting(bow[0], bow[1])
    if metric == 'manhattan':
        dis = manhattan(bow[0], bow[1])
        sim = 1 / (1 + dis)
    elif metric == 'jaccard':
        sim = jaccard(bow[0], bow[1])
    elif metric == 'euclidean':
        dis = distance.euclidean(bow[0], bow[1])
        sim = 1 / (1 + dis)

    return sim

def jaccard(list1, list2):
    intersection = len(list(set(list1).intersection(list2)))
    union = (len(list1) + len(list2)) - intersection
    return float(intersection) / union