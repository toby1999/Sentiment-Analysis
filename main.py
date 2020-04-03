print("Loading modules")
import pandas as pd
import word_freq
import pickle
from datetime import datetime
from tabulate import tabulate
from nltk.corpus import stopwords

pd.set_option('display.max_columns', None)

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
    dFrame = pd.DataFrame(data = reviews,
                          columns = ['Training company',
                                     'Course',
                                     'Trainer',
                                     'Location',
                                     'Review',
                                     'Score',
                                     'Date'])
    print("DataFrame ready (" +str(len(dFrame.index)), "reviews)")
    return dFrame


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


def showHead(n):
    # Prints the first n reviews in the dataframe
    print(dataFrame.head(n))


reviews = getReviews(dataset)
dataFrame = makeDataFrame(reviews)

pickle_out = open("Data/Pickle/dataFrame.pickle", "wb")
pickle.dump(dataFrame, pickle_out)
pickle_out.close()

from flask import escape

def hello_world(request):
    """ Responds to an HTTP request using data from the request body parsed
    according to the "content-type" header.
    Args:
        request (flask.Request): The request object.
        <
http://flask.pocoo.org/docs/1.0/api/#flask.Request
>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <
http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response
>.
    """
    content_type = request.headers['content-type']
    if content_type == 'application/json':
        request_json = request.get_json(silent=True)
        if request_json and 'name' in request_json:
            name = request_json['name']
        else:
            raise ValueError("JSON is invalid, or missing a 'name' property")
    elif content_type == 'application/octet-stream':
        name = request.data

    elif content_type == 'text/plain':
        name = request.data

    elif content_type == 'application/x-www-form-urlencoded':
        name = request.form.get('name')
    else:
        raise ValueError("Unknown content type: {}".format(content_type))
    return 'Hello world {}!'.format(escape(name))

#showHead(15)

showWordFreq(10)
