import nltk.tokenize
import operator
import pickle
import string
import re

print( "Loading classifier" )
pickle_in = open( "Data/Pickle/classifier.pickle", "rb" )
classifier = pickle.load(pickle_in)

# Read files containing keywords for aspect classification
course_keywords_file  = open( "Data/Aspect_keywords/course_keywords.txt",  "r" )
trainer_keywords_file = open( "Data/Aspect_keywords/trainer_keywords.txt", "r" )
venue_keywords_file   = open( "Data/Aspect_keywords/venue_keywords.txt",   "r" )

course_keywords  = [ word.rstrip() for word in course_keywords_file  ]
trainer_keywords = [ word.rstrip() for word in trainer_keywords_file ]
venue_keywords   = [ word.rstrip() for word in venue_keywords_file   ]

course_keywords_file.close()
trainer_keywords_file.close()
venue_keywords_file.close()


def aspect(sentence):
    '''
    Determines which aspect a sentiment relates to for a given sentence.
    '''
    # Remove other punctuation
    sentence = ''.join(char for char in sentence.lower() if char not in string.punctuation)
    # Split the sentence into words
    words = sentence.split()
    # List to collect sentiment aspects based on keywords
    aspects = {'course_content' : 0, 'trainer' : 0, 'venue' : 0, 'overall' : 0}

    for word in words:

        if word in course_keywords:
            aspects['course_content'] += 1

        if word in trainer_keywords:
            aspects['trainer'] += 1

        if word in venue_keywords:
            aspects['venue'] += 1

    aspects = sorted(aspects.items(), key=operator.itemgetter(1), reverse = True)
    aspect_sentiment = aspects[0][0]

    # Return sentiment aspect
    if  aspects[0][1] +\
        aspects[1][1] +\
        aspects[2][1] +\
        aspects[3][1] != 0:
        return aspect_sentiment

    else: # If no specific aspects were found, return 'overall' sentiment
        return 'overall'



def extract_features(word_list):
    # Returns a dictionary of words for the classifier
    return dict([(word, True) for word in word_list])

def classify(string):
    '''
    Takes in a review and returns its sentiments
    '''
    overall_sentiment = 0
    trainer_sentiment = 0
    course_sentiment  = 0
    venue_sentiment   = 0

    # Splits a sentence if it contains the word 'but'.
    string = string.replace(" but",".")

    # Splits the review into individual sentences
    sentences = nltk.tokenize.sent_tokenize(string)

    # Iterates through each sentence to determine sentiment aspects
    for sentence in sentences:
        # Classifier is used to determine positive or negative
        probdist = classifier.prob_classify(extract_features(sentence.split()))
        pred_sentiment = probdist.max()

        if pred_sentiment == 'Positive':
            if aspect(sentence) == 'overall':
                overall_sentiment += 1

            if aspect(sentence) == 'course_content':
                course_sentiment += 1

            if aspect(sentence) == 'trainer':
                trainer_sentiment += 1

            if aspect(sentence) == 'venue':
                venue_sentiment += 1

        else:
            if aspect(sentence) == 'overall':
                overall_sentiment -= 1

            if aspect(sentence) == 'course_content':
                course_sentiment -= 1

            if aspect(sentence) == 'trainer':
                trainer_sentiment -= 1

            if aspect(sentence) == 'venue':
                venue_sentiment -= 1


    # Dictionary to collect sentiment aspects

    review_sentiment = {'overall'        : overall_sentiment,
                        'course_content' : course_sentiment,
                        'trainer'        : trainer_sentiment,
                        'venue'          : venue_sentiment }
    return review_sentiment

print("Classifier ready")

# test = classify("It has been a fascinating subject to learn and very rewarding but I felt that the course content needed to be adjusted. No tea and coffee facilities either. The trainer was suberb. ")
# print(test)
# print(test['venue'])
