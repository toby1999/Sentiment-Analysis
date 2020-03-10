print("Loading modules")
import pandas as pd
import numpy  as np
import operator
import re
import word_freq
import string
import sys
import pickle
from collections import Counter
from nltk.corpus import stopwords
from tabulate    import tabulate
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier as rfc
#from sentiment1 import classify
pd.set_option('display.max_columns', None)

print("Loading spreadsheet")
spreadsheet = pd.read_excel ('test_data2.xlsx') # Open spreadsheet
dataset = pd.DataFrame(spreadsheet,
                       columns= ['Training Company', 'Course Name', 'Trainer name', 'Location', 'General Comments', 'Overall Score (1-5)', 'Review Date'])

def getReviews(data):
    '''
    Returns a list of reviews from the spreadsheet
    '''
    reviews = []
    for row in data.itertuples():
        comment = str(row[5])
        if comment == "nan": continue
        company = str(row[1])
        course = str(row[2])
        trainer = str(row[3])
        location = str(row[4])
        score = int(row[6])
        date = str(row[7])

        review = (company, course, trainer, location, comment, score, date)
        reviews.append(review)
    return reviews


def makeDataFrame(reviews):
    '''
    Creates the dataframe
    '''
    print("Loading DataFrame")
    dFrame = pd.DataFrame(data=reviews, columns=['Training company', 'Course', 'Trainer', 'Location', 'Review', 'Score', 'Date'])
    print("DataFrame ready")
    return dFrame


def showWordFreq(n_most_common):
    '''
    Prints list of n most common words
    '''
    word_frequency = word_freq.getWordFreq(dataFrame['Review'], n_most_common, stopwords.words('english'))
    print("")
    print(tabulate(word_frequency, headers=['Word', 'Frequency']))
    print("")

def showHead(n):
    '''
    Prints the first n reviews in the dataframe
    '''
    print(dataFrame.head(n))



reviews = getReviews(dataset)
dataFrame = makeDataFrame(reviews)


#pickle_out = open("dataFrame.pickle", "wb")
#pickle.dump(dataFrame, pickle_out)
#pickle_out.close()

#pickle_in = open("dataFrame.pickle", "rb")
#dataFrame = pickle.load(pickle_in)



#showWordFreq(10)
#showHead(15)



'''
vectorizer = TfidfVectorizer(min_df=15)
bow = vectorizer.fit_transform(dataFrame['Reviews'])
labels = dataFrame['Reviews']


print("Number of features:",len(vectorizer.get_feature_names()))

selected_features = \
SelectKBest(chi2, k=200).fit(bow, labels).get_support(indices=True)

vectorizer = TfidfVectorizer(min_df=15, vocabulary=selected_features)

bow = vectorizer.fit_transform(dataFrame['Reviews'])

X_train, X_test, y_train, y_test = train_test_split(bow, labels, test_size=0.33)

classifier = rfc()
classifier.fit(X_train,y_train)
print("Model accuracy:", classifier.score(X_test,y_test))

classifier.fit(bow,labels)

our_negative_sentence = vectorizer.transform(['I hated this product. It is \
not well designed at all, and it broke into pieces as soon as I got it. \
Would not recommend anything from this company.'])

our_positive_sentence = vectorizer.transform(['The movie was superb - I was \
on the edge of my seat the entire time. The acting was excellent, and the \
scenery - my goodness. Watch this movie now!'])

print(classifier.predict_proba(our_negative_sentence))
print(classifier.predict_proba(our_positive_sentence))
'''
