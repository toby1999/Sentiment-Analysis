import operator
import string
from collections import Counter

def wordFrequency(reviews):
    '''
    Iterates through the reviews and returns a dictionary of word frequencies
    '''
    wordfreq = {}   # Word frequencies stored here

    for review in reviews:
        for word in review:
            if word not in wordfreq:
                wordfreq[word] = 0
            wordfreq[word] += 1

    # Sort dictionary by key value
    wordfreq = sorted(wordfreq.items(), key=operator.itemgetter(1), reverse = True)

    return wordfreq

def printFreq(wordfreq):
    # Print (n) most common words
    n = 0
    for x in wordfreq:
        print(n+1,"\t", x[1], "\t", x[0])
        n += 1
        if n == 25:
            break

def getWordFreq(dataFrame, n, stopwords=None):
    # Split reviews into words & make lowercase
    split_reviews = [word for review in dataFrame for word in review.lower().split()]
    # Remove punctuation/special characters
    split_reviews = [''.join(char for char in review if char not in string.punctuation)
                    for review in split_reviews]
    # Remove stopwords
    if stopwords:
        split_reviews = [word for word in split_reviews if word not in stopwords]
    # Strip whitespace
    split_reviews = [review for review in split_reviews if review]

    wordFreq = Counter(split_reviews).most_common(n)

    return wordFreq
