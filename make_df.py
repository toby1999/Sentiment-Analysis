print("Loading modules")
import pandas as pd
import word_freq
import pickle
import nltk
from classify import classify
from datetime import datetime
from tabulate import tabulate
from nltk.corpus import stopwords

pd.set_option('display.max_columns', None)
# nltk.download()
print("Loading spreadsheet")
spreadsheet = pd.read_excel ('Data/coursecheck_data.xlsx') # Open spreadsheet
dataset = pd.DataFrame(spreadsheet,
                       columns= ['Training Company', 'Course Name',
                                 'Trainer name', 'Location', 'General Comments',
                                 'More comments 1', 'Overall Score (1-5)',
                                 'Review Date'])

def getReviews(data):
    '''
    Returns a list of reviews from the Excel spreadsheet
    '''
    reviews = []

    for row in data.itertuples():
        comment = str(row[5])
        more_comments = str(row[6])
        # Omit blank comments
        if comment == 'nan' and more_comments == 'nan' : continue

        company  =  str(row[1]).strip()
        course   =  str(row[2]).strip()
        trainer  =  str(row[3]).strip()
        location =  str(row[4]).strip()
        score    =  int(row[7])
        date     =  pd.Timestamp(datetime.strptime(str(row[8]) , '%Y-%m-%d %H:%M:%S'))

        if comment == 'nan':
            review = (company, course, trainer, location, more_comments, score, date)
            reviews.append(review)

        if more_comments == 'nan':
            review = (company, course, trainer, location, comment, score, date)
            reviews.append(review)

        else:
            comment = comment + ". " + more_comments
            review = (company, course, trainer, location, comment, score, date)
            reviews.append(review)

    return reviews



def makeDataFrame(reviews):
    '''
    Creates the dataframe
    '''
    print("Loading DataFrame")
    df = pd.DataFrame(data = reviews,
                          columns = ['Training company',
                                     'Course',
                                     'Trainer',
                                     'Location',
                                     'Review',
                                     'Score',
                                     'Date'])
    print("DataFrame ready ({} reviews)".format(str(len(df.index))))
    return df


def getSentiments(df):
    sentiments_overall = []
    sentiments_course  = []
    sentiments_trainer = []
    sentiments_venue   = []
    for review in df.iterrows():
        sentiment = classify(review[1][4])
        sentiments_overall.append(sentiment['Overall'])
        sentiments_course .append(sentiment['Course' ])
        sentiments_trainer.append(sentiment['Trainer'])
        sentiments_venue  .append(sentiment['Venue' ])
    return sentiments_overall, sentiments_course, sentiments_trainer, sentiments_venue

def dump(df):
    print("Serializing dataFrame...")
    pickle_out = open("Data/Pickle/dataFrame.pickle", "wb")
    pickle.dump(df, pickle_out)
    pickle_out.close()


def showWordFreq(n_most_common):
    '''
    Prints list of n most common words
    '''
    word_frequency = word_freq.getWordFreq(dataFrame['Review'],
                                           n_most_common,
                                           stopwords.words('english'))

    print("\n" + tabulate(word_frequency,
                          headers   = ['Word', 'Frequency'],
                          showindex = "always") + "\n")



reviews = getReviews(dataset)
df = makeDataFrame(reviews)

print("Classifying reviews...")
sentiment_overall, sentiment_course, sentiment_trainer, sentiment_venue = getSentiments(df)

df['Sentiment overall'] = sentiment_overall
df['Sentiment course'] = sentiment_course
df['Sentiment trainer'] = sentiment_trainer
df['Sentiment venue'] = sentiment_venue

# dump(df)
# print(df.head())
# showWordFreq(10)

print("Done")
