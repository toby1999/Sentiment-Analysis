print("Loading modules")
import pandas as pd
import operator
import re
import word_freq
import string
import sys
import tabulate
import pickle
from collections import Counter
from nltk.corpus import stopwords

pd.set_option('display.max_columns', None)

print("Loading spreadsheet")
spreadsheet = pd.read_excel ('Data/coursecheck_data.xlsx') # Open spreadsheet
dataset = pd.DataFrame(spreadsheet,
                       columns= ['Training Company', 'Course Name',
                                 'Trainer name', 'Location', 'General Comments',
                                 'Overall Score (1-5)', 'Review Date'])

def getReviews(data):
    '''
    Returns a list of reviews from the spreadsheet
    '''
    reviews = []
    for row in data.itertuples():
        comment = str(row[5])

        if comment == "nan": continue

        company     = str(row[1])
        course      = str(row[2])
        trainer     = str(row[3])
        location    = str(row[4])
        score       = int(row[6])
        date        = str(row[7])

        review = (company, course, trainer, location, comment, score, date)
        reviews.append(review)

    return reviews


def makeDataFrame(reviews):
    '''
    Creates the dataframe
    '''
    print("Loading DataFrame")
    dFrame = pd.DataFrame(data=reviews,
                          columns=['Training company', 'Course',
                                   'Trainer', 'Location',
                                   'Review', 'Score', 'Date'])
    print("DataFrame ready")
    return dFrame


def showWordFreq(n_most_common):
    '''
    Prints list of n most common words
    '''
    word_frequency = word_freq.getWordFreq(dataFrame['Review'], n_most_common, stopwords.words('english'))
    # print(tabulate(word_frequency, headers=['Word', 'Frequency']))
    count = 0
    for word in word_frequency:
        count += 1
        print(count, word[1], "\t", word[0])

def showHead(n):
    '''
    Prints the first n reviews in the dataframe
    '''
    print(dataFrame.head(n))


reviews = getReviews(dataset)
dataFrame = makeDataFrame(reviews)

# pickle_out = open("dataFrame.pickle", "wb")
# pickle.dump(dataFrame, pickle_out)
# pickle_out.close()

# showHead(15)

showWordFreq(500)
