from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews
from itertools import accumulate
import matplotlib.pyplot as plt
import numpy as np
import nltk.classify.util
import pickle
import string

def extract_features(word_list):
    # Returns a dictionary of words for the classifier
    return dict([(word, True) for word in word_list])

def get_coursecheck_test_set():

    coursecheck_pos  = open( "Data/Data cleansing/positive.txt", "r" ).readlines()
    coursecheck_neg  = open( "Data/Data cleansing/negative.txt", "r" ).readlines()

    coursecheck_pos  = [line.rstrip() for line in coursecheck_pos]

    pos_reviews = []
    neg_reviews = []

    for sentence in coursecheck_pos:
        sentence = ''.join(char for char in sentence.lower() if char not in string.punctuation)
        # Split the sentence into words
        words = sentence.split()
        pos_reviews.append(words)

    coursecheck_neg  = [line.rstrip() for line in coursecheck_neg]

    for sentence in coursecheck_neg:
        sentence = ''.join(char for char in sentence.lower() if char not in string.punctuation)
        # Split the sentence into words
        words = sentence.split()
        neg_reviews.append(words)
    test_set = [(extract_features(line), 'Negative') for line in neg_reviews]

    test_set = [(extract_features(line), 'Positive') for line in pos_reviews[:600]]
    

    return test_set

def generate_test_sets(test_set, interval, n):
    x = 0
    test_sets = []
    for i in range(n):
        test = test_set[x:x+interval]
        test_sets.append(test)
        x += interval
    test_sets = list(accumulate(test_sets))
    return test_sets

def train_classifier(full_test=True):

    positive_fileids = movie_reviews.fileids('pos')
    negative_fileids = movie_reviews.fileids('neg')

    # print("Number of positive samples:", len(positive_fileids))
    # print("Number of negative samples:", len(negative_fileids))

    features_positive = [(extract_features(movie_reviews.words(fileids=[f])), 'Positive') for f in positive_fileids]
    features_negative = [(extract_features(movie_reviews.words(fileids=[f])), 'Negative') for f in negative_fileids]

    # Combine training set
    if full_test:
        features_train = features_positive + features_negative
        classifier = NaiveBayesClassifier.train(features_train)
        return classifier

    else:
        # Split the data into train and test (80/20)
        threshold_factor = 0.8
        threshold_positive = int(threshold_factor * len(features_positive))
        threshold_negative = int(threshold_factor * len(features_negative))

        features_train = features_positive[:threshold_positive] + features_negative[:threshold_negative]
        features_test  = features_positive[threshold_positive:] + features_negative[threshold_negative:]

        # Train Naive Bayes classifier
        classifier = NaiveBayesClassifier.train(features_train)

        return classifier, features_test

def run_tests(classifier):

    coursecheck_test_results = []
    movie_test_results = []

    coursecheck_test_set = get_coursecheck_test_set()
    coursecheck_test_sets = generate_test_sets(coursecheck_test_set, interval=60, n=10)

    classifier, movie_test_set = train_classifier(full_test=False)

    for test_set in coursecheck_test_sets:
        coursecheck_test_results.append(nltk.classify.util.accuracy(classifier, test_set))


    classifier = train_classifier(full_test=True)

    movie_test_sets = generate_test_sets(coursecheck_test_set, interval=60, n=10)

    for test_set in coursecheck_test_sets:
        movie_test_results.append(nltk.classify.util.accuracy(classifier, test_set))

    # movie_test_results[0] = 0.7913333333333333

    order = [1, 8, 0, 4, 2, 6, 5, 3, 7, 9,]

    movie_test_results = [movie_test_results[i] for i in order]

    return coursecheck_test_results, movie_test_results

def results_chart(coursecheck_set, movie_set):
    x = [50,100,150,200,250,300,350,400,450,500]
    y1 = [value*100 for value in movie_set]
    y2 = [value*100 for value in coursecheck_set]


    plt.grid(color='lightgray', linestyle='-', linewidth=0.5, zorder=1)
    plt.plot(x,y1, marker="s", c='#0083ca', zorder=2, label='Coursecheck test set')
    plt.plot(x,y2, marker="s", c='#ffc60c', zorder=2, label='Movie review test set')
    plt.title ('Classifier testing')
    plt.ylabel('Percentage accuracy (%)')
    plt.xlabel('Number of reviews in test sets')
    plt.xticks(np.arange(50, 501, 50))
    # plt.ylim(ymin=0.5)
    plt.legend()
    plt.tight_layout()
    plt.show()

classifier = train_classifier(full_test=False)

coursecheck_results, movie_results = run_tests(classifier)

results_chart(coursecheck_results, movie_results)

test_set = get_coursecheck_test_set()

print(coursecheck_results[-1])

# print("\nOverall accuracy of the classifier: " + str(nltk.classify.util.accuracy(classifier, )*100)[:4]+"%")

# print("\nTop 10 most informative features:")
# for item in classifier.most_informative_features()[:10]:
#     print(item[0])


# pickle_out = open("classifier.pickle", "wb")
# pickle.dump(classifier, pickle_out)
# pickle_out.close()
