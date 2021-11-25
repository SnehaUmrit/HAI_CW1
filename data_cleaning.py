# importing required libraries
import numpy as np
import pandas as pd
import random, re, json
from nltk import sent_tokenize

# df1 - epicurious dataset
# df2 - food.com dataset

# reading json file
df1 = pd.read_json(r"raw_data\epicurious_recipes.json")

# converting json to csv file
df1.to_csv(r"raw_data\epicurious_recipes.csv")

# reading second dataset
df2 = pd.read_csv(r"raw_data\fooddotcom_recipes.csv")

df1.replace(['', ""], np.nan, inplace=True)
df2.replace(['', ""], np.nan, inplace=True)

# removing rows with null value
df1.dropna(how='any', inplace=True)
df2.dropna(how='any', inplace=True)

# removing unnecessary rows
df1_drop_cols = 'date'
df2_drop_cols = ['id', 'contributor_id', 'submitted']

df1.drop(df1_drop_cols, inplace=True, axis=1)
df2.drop(df2_drop_cols, inplace=True, axis=1)

# choosing random 2500 data rows for each dataset
df1 = df1.sample(2500)
df2 = df2.sample(2500)

# renaming columns
df1 = df1.rename(columns={'directions': 'instructions', 'desc': 'description', 'fat': 'total_fat'})

# saving the cleaned data
df1.to_csv(r"data\information_retrieval\epicurious_recipes_cleaned.csv")

# extracting each nutrition element from food.com recipe and adding columns
df2_new_cols = ['calories', 'fat', 'sodium', 'protein']
nutrition = []
calories = []
total_fat = []
sugar = []
sodium = []
protein = []
saturated_fat = []
carbohydrate = []

# nutrition [393.6, 32.0, 147.0, 11.0, 16.0, 66.0, 15.0] indicates
# ['calories', 'total fat', 'sugar', 'sodium', 'protein', 'saturated fat', 'carbohydrate']
ignore_chars = ['[', ',', ']', '[]']

for row in df2.iterrows():
    nutrition = row[1]['nutrition'].replace('[', '')
    nutrition = nutrition.replace(']', '')
    nutrition = nutrition.replace(',', ' ')
    nutrition = nutrition.split()
    calories.append(nutrition[0])
    total_fat.append(nutrition[1])
    sugar.append(nutrition[2])
    sodium.append(nutrition[3])
    protein.append(nutrition[4])
    saturated_fat.append(nutrition[5])
    carbohydrate.append(nutrition[6])

df2['calories'] = calories
df2['total_fat'] = total_fat
df2['sugar'] = sugar
df2['sodium'] = sodium
df2['protein'] = protein
df2['saturated_fat'] = saturated_fat
df2['carbohydrate'] = carbohydrate

# renaming columns
df2 = df2.rename(columns={'name': 'title', 'tags': 'categories', 'steps': 'instructions'})

# saving the cleaned data
df2.to_csv(r"data\information_retrieval\fooddotcom_recipes_cleaned.csv")

# cleaning dataset for small_talk
# json_file = json.load(open(r"raw_data\kaggle_small_talk.json","r"))

# for intent in json_file["intents"]:
#    del intent['entities']
#    del intent['context']
#    del intent['extension']


# with open(r"data\small_talk\kaggle_small_talk_cleaned.json", 'w') as f:
#    json.dump(json_file,f)
