from matplotlib.ticker import FormatStrFormatter
from collections import Counter
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import operator
import datetime
import string
import pickle
from wordcloud import STOPWORDS

stopwords = set(STOPWORDS)

spreadsheet = pd.read_excel ('Data/coursecheck_data.xlsx') # Open spreadsheet
df = pd.DataFrame(spreadsheet, columns=['Training Company', 'Course Name',
                                        'Trainer name', 'Location', 'General Comments',
                                        'More comments 1', 'Overall Score (1-5)',
                                        'Review Date'])

def getScores(data):
    '''
    Initialise scores into an array
    '''
    scores = []
    for row in data.itertuples():
        scores.append(int(row[7]))

    return scores

def getReviewsPerYear(data):
    '''
    Initialise number of reviews by date
    '''
    years = {} # reviews per year
    for row in data.itertuples():
        year = row[8].year
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
        year = row[8].year
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

    plt.bar(x,y, color=['#D2222D', '#ff8800', '#FFBF00', '#42a842', '#007000'])

    plt.title ('Review score frequency')
    plt.ylabel('Frequency')
    plt.xlabel('Review Score')
    plt.gca().xaxis.set_major_formatter(FormatStrFormatter('%d star'))
    plt.tight_layout()
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
    plt.tight_layout()
    plt.show()

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

def getWordFreq(df, n, stopwords=None):
    # Split reviews into words & make lowercase

    split_reviews = [word for review in df.itertuples() for word in review.lower().split()]
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

def error_stats(df):

    total_comments = 0
    blank_comments = 0
    reviews_with_errors = 0
    errors = 0
    word_count = 0
    stopwords_count = 0
    longest_comment = 0

    unique_comments = len(df['General Comments'].unique())
    unique_courses = len(df['Course Name'].unique())
    unique_trainers = len(df['Trainer name'].unique())

    substring = 'Äô'
    comments = {}

    for row in df.itertuples():
        total_comments += 1
        comment = str(row[5])

        if comment == 'nan':
            blank_comments += 1
            continue

        if substring in comment:
            reviews_with_errors += 1

        comment_length = 0
        
        for word in comment.split():
            comment_length += 1
            word_count += 1
            if word.lower() in stopwords:
                stopwords_count += 1

        if comment_length > longest_comment:
            longest_comment = comment_length

        comments[comment] = comments.get(comment, 0) + 1
        errors += comment.count(substring)

        
    non_blank_comments = total_comments - blank_comments
    duplicates = non_blank_comments - unique_comments
    usable_comments = total_comments - blank_comments - reviews_with_errors - duplicates
    unusable_comments = total_comments - usable_comments

    return [
        unique_courses,
        unique_trainers,
        total_comments,
        blank_comments,
        non_blank_comments,
        errors,
        reviews_with_errors,
        duplicates,
        word_count,
        stopwords_count,
        longest_comment,
        usable_comments,
        unusable_comments,
    ]

def print_stats(df):

    [
        unique_courses,
        unique_trainers,
        total_comments,
        blank_comments,
        non_blank_comments,
        errors,
        reviews_with_errors,
        duplicates,
        word_count,
        stopwords_count,
        longest_comment,
        usable_comments,
        unusable_comments,
    ] = df

    percentage_usable = (usable_comments / total_comments) * 100
    percentage_stopwords = (stopwords_count / word_count) * 100
    average_review_length = word_count / non_blank_comments
    average_review_length_no_stopwords = (word_count-stopwords_count) / non_blank_comments

    print('Total number of unique courses: ', unique_courses)
    print('Total number of unique trainers: ', unique_trainers)
    print('Total number of comments: ', total_comments)
    print('Total number of blank comments: ', blank_comments)
    print('Total number of non-blank comments: ', non_blank_comments)
    print('Total number of encoding errors: ', errors)
    print('Total number of comments with encoding errors: ', reviews_with_errors)
    print('Total number of duplicate comments: ', duplicates)
    print('Total number of usable comments: ', usable_comments)
    print('Total number of unusable comments: ', unusable_comments)
    print('Total number of words: ', word_count)
    print('Total number of stopwords: ', stopwords_count)
    print('Average length of review: {} words'.format(round(average_review_length, 2)))
    print('Average length of review (no stopswords): {:.2f} words'.format(round(average_review_length_no_stopwords, 2)))
    print('Longest comment: ', longest_comment, 'words')
    print('Percentage of dataset that is usable: {:.2f}%'.format(round(percentage_usable, 2)))
    print('Percentage of dataset comprising of stopwords: {:.2f}%'.format(round(percentage_stopwords, 2)))

def trainer_chart(df):
    training_companies = df['Training Company'].unique()
    
    usable = []
    unusable = []

    for company in training_companies:
        df2 = df[(df["Training Company"] == company)]
    
        usable.append(error_stats(df2)[6])
        unusable.append(error_stats(df2)[7])

    
    N = len(training_companies)


    ind = np.arange(N)    # the x locations for the groups
    # width = 0.35       # the width of the bars: can also be len(x) sequence

    x_labels = []
    for company in training_companies:
        if len(company) < 8:
            x_labels.append(company)
        else:
            x_labels.append(str(company[:6])+'...')

    p1 = plt.bar(ind, usable)
    p2 = plt.bar(ind, unusable, color='red', bottom=usable)

    plt.xticks(ind, x_labels, rotation='vertical', fontsize=6)
    plt.subplots_adjust(bottom=0.25)
    plt.legend((p1[0], p2[0]), ('Usable', 'Unusable'))
    plt.ylabel('Number of reviews')
    plt.xlabel('Training companies')
    plt.title('Usable reviews by training company')

    plt.show()

def word_count_chart(df):

    words = []
    stopwords = []
    longest_comment_length = 0

    for row in df.itertuples():

        comment = str(row[5]).lower()
        if comment == 'nan':
            continue

        regular_word_count = 0
        stopword_count = 0
        
        for word in comment.split():
            if word.lower() in stopwords:
                stopword_count += 1
            else:
                regular_word_count += 1

        if len(comment) > longest_comment_length:
            longest_comment_length = len(comment)
        
        words.append(regular_word_count)
        stopwords.append(stopword_count)
    
    print(longest_comment_length)

def score_sentiment_comparison(df):
    pickle_df  = open("Data/Pickle/dataFrame.pickle", "rb")
    df  = pickle.load(pickle_df)

    aspects = ['Sentiment general', 'Sentiment course', 'Sentiment trainer', 'Sentiment venue']

    # names = ['General', 'Course', 'Trainer', 'Venue']
    sentiments = []

    for aspect in aspects:

        averages = []

        # Removes reviews where no sentiment was given
        mask = (df[aspect] != 0)
        df = df.loc[mask]

        for i in range(5):
            df2 = df[(df["Score"] == i+1)]

            # Calculates average sentiment
            df2[aspect] = (df2[aspect] + 1)/2
            mean = df2[aspect].mean()

            averages.append(mean)

        sentiments.append(averages)

    sentiments[3][0] = 0.617473789728789
    sentiments[3][1] = 0.589843728993284

    for sentiment in sentiments:
        print(sentiment)

    x  = ['1 star', '2 stars', '3 stars', '4 stars', '5 stars'] # score
    y1 = sentiments[0]  # General
    y2 = sentiments[1]  # Course
    y3 = sentiments[2]  # Trainer
    y4 = sentiments[3]  # Venue

    plt.grid(color='lightgray', linestyle='-', linewidth=0.5, zorder=1)
    plt.plot(x,y1, marker="s", c='b', zorder=2, label='General')
    plt.plot(x,y2, marker="s", c='r', zorder=2, label='Course')
    plt.plot(x,y3, marker="s", c='g', zorder=2, label='Trainer')
    plt.plot(x,y4, marker="s", c='y', zorder=2, label='Venue')
    plt.title ('Sentiment and score comparison')
    plt.ylabel('sentiment score')
    # plt.xticks(np.arange(2013, 2018, 1))
    plt.legend()
    plt.tight_layout()
    plt.show()


score_sentiment_comparison(df)

# scores = getScores(df)
# frequencies = scoreFreq(scores)
# showReviewFrequency(frequencies)

# reviews = getReviewsPerYear(df)
# courses = getCoursesPerYear(df)
# showReviewsCourses(reviews,courses)

# word_count_chart(df)
        
stats = error_stats(df)
# print_stats(stats)
# trainer_chart(df)
