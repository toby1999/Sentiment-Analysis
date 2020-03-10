print("Loading modules")
import pandas as pd
import numpy  as np
import operator
import re
import word_freq
import string
import sys
import ast
import string
from collections import Counter
from nltk.corpus import stopwords
from tabulate    import tabulate
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier as rfc
from sklearn.model_selection import RandomizedSearchCV
from scipy import stats


'''
def openAmazon():
    print("Reading file")
    file = open("amazon.json", "r")
    reviews = []
    for x in file:
        record = ast.literal_eval(x)
        score = int(record["overall"])
        if 2 <= score <=4 :
            continue
        review = record["reviewText"]
        if score ==5: sentiment = 1
        if score ==1: sentiment = 0
        reviews.append([review,sentiment])
    file.close()
    print("\nFile read successfully")
    return reviews
'''

def makeDataFrame(reviews):
    '''
    Creates the dataframe
    '''
    dFrame = pd.DataFrame(data=reviews, columns=['Reviews', 'Sentiment'])
    dFrame = dFrame[dFrame["Sentiment"].notnull()]
    #dFrame = dFrame.sample(frac=1)
    return dFrame

def showHead(dataFrame, n):
    '''
    Prints the first n reviews in the dataframe
    '''
    print(dataFrame.head(n)[['Reviews', 'Sentiment']], "\n")


amzn = open("amazon_cells_labelled.txt").read()
imdb = open("imdb_labelled.txt").read()
yelp = open("yelp_labelled.txt").read()
# Combining the datasets
datasets = [amzn, imdb, yelp]
data = []
for dataset in datasets:
    data.extend(dataset.split('\n'))
# separate each label from each sample
dataset = [sample.split('\t') for sample in data]



dataFrame = makeDataFrame(dataset)

dataFrame['Word Count'] = [len(review.split()) for review in dataFrame['Reviews']]

dataFrame['Uppercase Char Count'] = [sum(char.isupper() for char in review) \
                                    for review in dataFrame['Reviews']]

dataFrame['Special Char Count'] = [sum(char in string.punctuation for char in review) \
                                  for review in dataFrame['Reviews']]

showHead(dataFrame, 5)

vectorizer = TfidfVectorizer(min_df=15)
bow = vectorizer.fit_transform(dataFrame['Reviews'])
labels = dataFrame['Sentiment']

print(len(vectorizer.get_feature_names()))

selected_features = SelectKBest(chi2, k=200).fit(bow, labels).get_support(indices=True)

vectorizer = TfidfVectorizer(min_df=15, vocabulary=selected_features)

bow = vectorizer.fit_transform(dataFrame['Reviews'])
bow
print(len(vectorizer.get_feature_names()))

X_train, X_test, y_train, y_test = train_test_split(bow, labels, test_size=0.33)

classifier = rfc()
classifier.fit(X_train,y_train)
print("Model accuracy:", classifier.score(X_test,y_test))



classifier.fit(bow,labels)

negative_sentence = vectorizer.transform(['I hated this product. It is \
not well designed at all, and it broke into pieces as soon as I got it. \
Would not recommend anything from this company.'])

positive_sentence = vectorizer.transform(['The movie was superb - I was \
on the edge of my seat the entire time. The acting was excellent, and the \
scenery - my goodness. Watch this movie now!'])

print(classifier.predict_proba(negative_sentence))
print(classifier.predict_proba(positive_sentence))
