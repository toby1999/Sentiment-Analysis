import re
import nltk
import pickle
import operator
import numpy as np
import pandas as pd
from os import path
from word_freq import printFreq
from wordcloud import WordCloud, ImageColorGenerator, STOPWORDS, get_single_color_func
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import PorterStemmer


stopwords = set(STOPWORDS)
porter=PorterStemmer()

# Deserializing dataframe
pickle_df  = open("Data/Pickle/dataFrame.pickle", "rb")
df  = pickle.load(pickle_df)
df = df[(df["Training company"] == "Entertainment 720")]

def get_words(df):

    # Removes any unwanted punctuation, special characters or numbers
    reviews = " ".join(review for review in df['Review'])
    reviews = re.sub("[^A-Za-z" "]+"," ",reviews).lower()
    reviews = re.sub("[0-9" "]+"," ",reviews)

    # Splits reviews into a list of words
    words = reviews.split(" ")

    # Open positive and negative word lists
    with open("Data/Wordcloud_data/positive-words.txt","r") as positive:
        positive_list = positive.read().split("\n")

    with open("Data/Wordcloud_data/negative-words.txt", "r", encoding="ISO-8859-1") as negative:
        negative_list = negative.read().split("\n")

    positive_words = " ".join([word for word in words if word in positive_list])
    negative_words = " ".join([word for word in words if word in negative_list])
    
    return positive_words, negative_words


def most_common(text):
    '''
    Iterates through text and returns a dictionary of word frequencies
    '''
    wordfreq = {}   # Word frequencies stored here

    for word in text.split():
        if word not in wordfreq:
            wordfreq[word] = 0
        wordfreq[word] += 1

    # Sort dictionary by key value
    wordfreq = sorted(wordfreq.items(), key=operator.itemgetter(1), reverse = True)

    return wordfreq

def generate_clouds(positive_words, negative_words):

    positive_cloud = WordCloud(stopwords=stopwords,
                                color_func=get_single_color_func('darkgreen'),
                                background_color='white',
                                max_words=50,
                                width=600,
                                height=600,
                                ).generate(positive_words)


    negative_cloud = WordCloud(stopwords=stopwords,
                                color_func=get_single_color_func('red'),
                                background_color='white',
                                max_words=50,
                                width=600,
                                height=600,
                                ).generate(negative_words)


    print("Generating files")
    positive_cloud.to_file("Data/Wordcloud_data/wordcloud_pos.png")
    negative_cloud.to_file("Data/Wordcloud_data/wordcloud_neg.png")

# positive_words, negative_words = get_words(df)
# generate_clouds(positive_words, negative_words)
