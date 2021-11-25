from datetime import datetime

import datefinder
import pandas as pd
import re
from dateutil.parser import parse

from information_retrieval import cosine_similarity

# creating a csv file to store the list of items with expiration dates
# exp_df = pd.DataFrame()
# exp_df['food_item'] = ''
# exp_df['exp_date'] = ''
# exp_df.to_csv(r'out_data/expiration_list.csv', index=False)
exp_df = pd.read_csv(r'out_data/expiration_list.csv')
exp_df = exp_df.dropna(how='any')

# extract date from a string
def date_parser(string):
    matches = list(datefinder.find_dates(string))
    if len(matches) > 0:
        date = matches[0]
        return date

# extract food item name from a string
def food_item_parser(string):
    response = ''
    pattern = 'for (.*) on'
    result = re.search(pattern, string)
    if result:
        response = re.findall(pattern, string)

    response = str(response)
    response = response.replace('[', '')
    response = response.replace(']', '')
    response = response.replace("'", '')
    return response

# add food item name and expiration date to csv
def food_tracker_add(user_input):
    # exp_df = pd.read_csv(r'out_data/expiration_list.csv')

    food_item = []
    exp_date = []

    exp_date.append(date_parser(user_input))
    food_item.append(food_item_parser(user_input))

    if food_item != [''] and exp_date != ['']:
        exp_df['food_item'] = pd.Series(food_item)
        exp_df['exp_date'] = pd.Series(exp_date)
        exp_df.dropna(how='any', inplace=True)
        exp_df.to_csv(r'out_data/expiration_list.csv', mode='a', index=False, header=False)

#food_tracker_add('add expiration date for eggs on 2021/10/19')
#food_tracker_add('add expiration date for on 2021/10/19')
#food_tracker_add('add expiration date for milk on 2021/11/19')
#food_tracker_add('add expiration date for flour on 2022/03/19')

def deleted_food_item(user_input):
    delete_item = ['Delete (.*) from the list', 'Remove (.*) from the list']
    for each in delete_item:
        each = each.lower()
        user_input = user_input.lower()
        result = re.search(each, user_input)
        if result:
            return result.group(1)

# r = deleted_food_item('Delete eggs from the list')
# print(r)

def food_tracker_delete_all():
    exp_list = pd.read_csv(r'out_data/expiration_list.csv')
    exp_list = exp_list.dropna(how='any')

    for index, row in exp_list.iterrows():
        exp_list.drop(index, inplace=True)
    exp_list.to_csv(r'out_data/expiration_list.csv', index=False)

#food_tracker_delete_all()

def food_tracker_delete_expired():
    exp_list = pd.read_csv(r'out_data/expiration_list.csv')
    exp_list = exp_list.dropna(how='any')

    for index, row in exp_list.iterrows():
        date1 = parse(row['exp_date'])
        date2 = datetime.now()
        # print(date1 < date2)
        if date1 < date2:
            exp_list.drop(index, inplace=True)
    exp_list.to_csv(r'out_data/expiration_list.csv', index=False)
# food_tracker_delete_expired()

def food_tracker_delete_item(user_input):
    exp_list = pd.read_csv(r'out_data/expiration_list.csv')
    exp_list = exp_list.dropna(how='any')

    for index, row in exp_list.iterrows():
        if row['food_item'] in user_input.lower():
            exp_list.drop(index, inplace=True)
    exp_list.to_csv(r'out_data/expiration_list.csv', index=False)

# food_tracker_delete_item('delete eggs from the list')

def food_tracker_fetch_expired():
    exp_items = []
    exp_list = pd.read_csv(r'out_data/expiration_list.csv')
    exp_list = exp_list.dropna(how='any')

    for index, row in exp_list.iterrows():
        date1 = date_parser(row['exp_date'])
        date2 = datetime.now()
        if date1 < date2:
            exp_items.append(row['food_item'] + ' expired on ' + row['exp_date'])
    exp_items = str(exp_items)
    exp_items = exp_items.replace('[', '')
    exp_items = exp_items.replace(']', '')
    exp_items = exp_items.replace("'", '')
    return exp_items

r = food_tracker_fetch_expired()
print(r)

def food_tracker_fetch_all():
    exp_items = []
    exp_list = pd.read_csv(r'out_data/expiration_list.csv')
    exp_list = exp_list.dropna(how='any')

    for index, row in exp_list.iterrows():
        date1 = date_parser(row['exp_date'])
        date2 = datetime.now()
        if date1 < date2:
            exp_items.append(row['food_item'] + ' expired on ' + row['exp_date'])
        else:
            exp_items.append(row['food_item'] + ' expires on ' + row['exp_date'])

    exp_items = str(exp_items)
    exp_items = exp_items.replace('[', '')
    exp_items = exp_items.replace(']', '')
    exp_items = exp_items.replace("'", '')
    return exp_items

# i = food_tracker_fetch_all()
# print(i)
