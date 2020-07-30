import re
import nltk
import pickle
import numpy as np
import pandas as pd
from os import path
from wordcloud import WordCloud, ImageColorGenerator, STOPWORDS, get_single_color_func

stopwords = set(STOPWORDS)

# Deserializing dataframe
pickle_df  = open("Data/Pickle/dataFrame.pickle", "rb")
df  = pickle.load(pickle_df)
df = df[(df["Training company"] == "Entertainment 720")]

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

green = get_single_color_func('darkgreen')
red = get_single_color_func('red')

# Generate positive word cloud
print("Preparing positive cloud")
positive_words = " ".join([word for word in words if word in positive_list])
positive_cloud = WordCloud(stopwords=stopwords,
                           color_func=green,
                           background_color='white',
                           max_words=50,
                           width=600,
                           height=600,
                           ).generate(positive_words)

# Generate negative word cloud
print("Preparing negative cloud")
negative_words = " ".join([word for word in words if word in negative_list])
negative_cloud = WordCloud(stopwords=stopwords,
                           color_func=red,
                           background_color='white',
                           max_words=50,
                           width=600,
                           height=600,
                           ).generate(negative_words)

print("Generating files")
positive_cloud.to_file("Data/Wordcloud_data/wordcloud_pos.png")
negative_cloud.to_file("Data/Wordcloud_data/wordcloud_neg.png")
