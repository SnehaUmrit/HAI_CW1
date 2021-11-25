# importing the required libraries
import nltk, os, json
import numpy as np
import pandas as pd
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import LogisticRegression
from sklearn import svm
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, accuracy_score, f1_score
from joblib import dump, load


def intent_classifier(user_input):
    # importing all data
    label_dir = {
        "information retrieval": "data/information_retrieval",
        "small talk": "data/small_talk",
        "food tracker": "data/food_tracker"
    }

    data = []
    labels = []

    for label in label_dir.keys():
        for file in os.listdir(label_dir[label]):
            filepath = label_dir[label] + os.sep + file
            # print(filepath)
            # data stored in csv file
            if filepath.endswith(".csv"):
                csv_file = pd.read_csv(filepath)
                for row in csv_file.iterrows():
                    data.append(row[1]["title"])
                    labels.append(label)

            # data stored in json file
            elif filepath.endswith(".json"):
                json_file = json.load(open(filepath, "r"))
                for intent in json_file["intents"]:
                    for pattern in intent["patterns"]:
                        data.append(pattern)
                        labels.append(label)

    X_train, X_test, y_train, y_test = train_test_split(data, labels, stratify=labels, test_size=0.25, random_state=100)
    count_vect = CountVectorizer(stop_words=stopwords.words('english'), ngram_range=(1,2))
    X_train_counts = count_vect.fit_transform(X_train)
    tfidf_transformer = TfidfTransformer(use_idf=True, sublinear_tf=True).fit(X_train_counts)
    X_train_tf = tfidf_transformer.transform(X_train_counts)

    # clf = LogisticRegression(random_state=0).fit(X_train_tf, y_train)
    # clf = svm.SVC().fit(X_train_tf, y_train)
    clf = DecisionTreeClassifier().fit(X_train_tf, y_train)
    # clf = RandomForestClassifier().fit(X_train_tf, y_train)

    X_new_counts = count_vect.transform(X_test)
    X_new_tfidf = tfidf_transformer.transform(X_new_counts)

    predicted = clf.predict(X_new_tfidf)
    #print(confusion_matrix(y_test, predicted))
    #print('accuracy score: '+ str(accuracy_score(y_test, predicted)))
    #print('f1 score: ' + str(f1_score(y_test, predicted, average='weighted')))

    dump(clf, 'classified_data.joblib')
    loaded_classifier = load('classified_data.joblib')

    new_data = [user_input]
    processed_newdata = count_vect.transform(new_data)
    processed_newdata = tfidf_transformer.transform(processed_newdata)
    user_intent = clf.predict(processed_newdata)
    return user_intent

# testing intent_classifier function
#i = intent_classifier("anything vegan")
#print(i)

# intent = intent_classifier("how are you")
# print(intent)

#i = intent_classifier("can i get the recipe for chicken and tomato, beans")
#print(i)

# intent = intent_classifier("tell me a joke")
# print(intent)

#intent = intent_classifier("delete flour from the list")
#print(intent)

#intent = intent_classifier("delete all items")
#print(intent)