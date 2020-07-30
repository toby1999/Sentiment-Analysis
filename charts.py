import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import pandas as pd
import numpy as np
import operator
import datetime
import word_freq
import pickle
import main

# Load the dataframe using Pickle
pickle_df  = open("Data/Pickle/dataFrame.pickle", "rb")
df  = pickle.load(pickle_df)

def getScores(data):
    '''
    Initialise scores into an array
    '''
    scores = []
    for row in data.itertuples():
        scores.append(int(row[6]))

    return scores

def getReviewsPerYear(data):
    '''
    Initialise number of reviews by date
    '''
    years = {} # reviews per year
    for row in data.itertuples():
        year = row[7].year
        if year not in years:
            years[year] = 0
        years[year] += 1
    years = sorted(years.items(), key=operator.itemgetter(0))
    del years[-2:] # 2019 is incomplete

    return years

def getCoursesPerYear(data):
    '''
    Initialise number of courses by date
    '''
    years = {} # reviews per year
    courses = []
    for row in data.itertuples():
        year = row[7].year
        course = str(row[3])

        if course not in courses:
            courses.append(course)
            if year not in years:
                years[year] = 0
            years[year] += 1

    years = sorted(years.items(), key=operator.itemgetter(0))
    del years[-1]

    return years

def scoreFreq(scores):
    '''
    Iterates through the reviews and returns a dictionary of word frequencies
    '''
    frequencies = {}   # Word frequencies stored here

    for score in scores:
        if score not in frequencies:
            frequencies[score] = 0
        frequencies[score] += 1

    # Sort dictionary by key value
    frequencies = sorted(frequencies.items(), key=operator.itemgetter(0))

    return frequencies


def showReviewFrequency(results):
    '''
    Shows a graph of review frequencies by review score
    '''
    x = [] # Scores are stored here
    y = [] # Frequencies are stored here
    for num in results:
        x.append(num[0])
        y.append(num[1])

    print(x)
    print(y)
    plt.bar(x,y)
    plt.title ('Review score frequency')
    plt.ylabel('Frequency')
    plt.xlabel('Review Score')
    plt.gca().xaxis.set_major_formatter(FormatStrFormatter('%d star'))
    plt.show()

def showReviewsCourses(reviews, courses):
    '''
    Shows the frequency of reviews and courses by year
    '''
    x  = [] # Years
    y1 = [] # Reviews frequency
    y2 = [] # Courses frequency

    for review in reviews:
        x.append(review[0])
        y1.append(review[1])
    for course in courses:
        y2.append(course[1])

    plt.grid(color='lightgray', linestyle='-', linewidth=0.5, zorder=1)
    plt.plot(x,y1, marker="s", c='b', zorder=2, label='Reviews')
    plt.plot(x,y2, marker="s", c='r', zorder=2, label='Courses')
    plt.title ('Number of reviews/courses per year')
    plt.ylabel('Frequency')
    plt.xticks(np.arange(2013, 2018, 1))
    plt.legend()
    plt.show()

scores = getScores(df)
frequencies = scoreFreq(scores)
showReviewFrequency(frequencies)

reviews = getReviewsPerYear(df)
courses = getCoursesPerYear(df)
showReviewsCourses(reviews,courses)
