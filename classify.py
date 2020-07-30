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
    aspects = {'course_content' : 0, 'trainer' : 0, 'venue' : 0, 'general' : 0}

    for word in words:

        if word in course_keywords:
            aspects['course_content'] = 1

        if word in trainer_keywords:
            aspects['trainer'] = 1

        if word in venue_keywords:
            aspects['venue'] = 1

    # Return sentiment aspect
    if  sum(aspects.values()) == 0:
        aspects['general'] = 1

    return aspects



def extract_features(word_list):
    # Returns a dictionary of words for the classifier
    return dict([(word, True) for word in word_list])

def classify(string):
    '''
    Takes in a review and returns its sentiments
    '''
    # variables to store sentiment values
    general_sentiment = 0
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
        sentiment = probdist.max() # Positive or negative

        if sentiment == 'Positive':

            if aspect(sentence)['course_content'] == 1:
                course_sentiment += 1

            if aspect(sentence)['trainer'] == 1:
                trainer_sentiment += 1

            if aspect(sentence)['venue'] == 1:
                venue_sentiment += 1

            if aspect(sentence)['general'] == 1:
                general_sentiment += 1

        if sentiment == 'Negative':

            if aspect(sentence)['course_content'] == 1:
                course_sentiment -= 1

            if aspect(sentence)['trainer'] == 1:
                trainer_sentiment -= 1

            if aspect(sentence)['venue'] == 1:
                venue_sentiment -= 1

            if aspect(sentence)['general'] == 1:
                general_sentiment -= 1

    def make_1_or_0(sentiment):
        if sentiment > 0: return  1
        if sentiment < 0: return -1
        else: return 0

    general_sentiment = make_1_or_0(general_sentiment)
    trainer_sentiment = make_1_or_0(trainer_sentiment)
    course_sentiment = make_1_or_0(course_sentiment)
    venue_sentiment = make_1_or_0(venue_sentiment)

    # Return a dictionary with sentiment aspects

    return {'General'        : general_sentiment,
            'Course'         : course_sentiment,
            'Trainer'        : trainer_sentiment,
            'Venue'          : venue_sentiment }


print("Classifier ready")

def test_segmentation():

    pos_file = open("Data/Data cleansing/positive.txt", "r").readlines()
    neg_file = open("Data/Data cleansing/negative.txt", "r").readlines()

    pos_samples = pos_file[:50]
    neg_samples = neg_file[:50]

    print("Number of positive samples:", len(pos_samples))
    print("Number of negative samples:", len(neg_samples))

    sample_sentences = pos_samples + neg_samples

    classifier_answers_file = open("Testing/Segmentation/aspects.txt","w+")
    actual_answers_file = open("Testing/Segmentation/aspects answers.txt","r").readlines()

    classifier_answers = []
    actual_answers = []

    for line in actual_answers_file:
        actual_answers.append(line.rstrip())

    for line in sample_sentences:
        result = classify(line)
        if result['General'] == -1: result['General'] = 1
        if result['Course'] == -1: result['Course'] = 1
        if result['Trainer'] == -1: result['Trainer'] = 1
        if result['Venue'] == -1: result['Venue'] = 1
        classifier_answers_file.write(str(result)+"\n")
        classifier_answers.append(str(result))

    correct = 0
    incorrect = 0

    for i in range(100):
        if classifier_answers[i] == actual_answers[i]:
            correct += 1
        else:
            incorrect += 1
    print("\nSentence segmentation accuracy:", str((correct/(correct+incorrect))*100)+"%")


'''

print("\nEnter string below (enter 'break' to exit)")

while True:
    input_text = input()
    if input_text == "break":
        break
    # print('"'+input_text+'"')
    result = classify(input_text)
    if result['General'] == 1: print("Aspect: GENERAL\nPolarity: POSITIVE")
    if result['General'] == -1: print("Aspect: GENERAL\nPolarity: NEGATIVE")
    if result['Course'] == 1: print("Aspect: COURSE CONTENT\nPolarity: POSITIVE")
    if result['Course'] == -1: print("Aspect: COURSE-CONTENT\nPolarity: NEGATIVE")
    if result['Trainer'] == 1: print("Aspect: TRAINER\nPolarity: POSITIVE")
    if result['Trainer'] == -1: print("Aspect: TRAINER\nPolarity: NEGATIVE")
    if result['Venue'] == 1: print("Aspect: VENUE\nPolarity: POSITIVE")
    if result['Venue'] == -1: print("Aspect: VENUE\nPolarity: NEGATIVE")
    print("")
'''
