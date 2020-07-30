from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews
import nltk.classify.util
import pickle
import string

def extract_features(word_list):
    # Returns a dictionary of words for the classifier
    return dict([(word, True) for word in word_list])

positive_fileids = movie_reviews.fileids('pos')
negative_fileids = movie_reviews.fileids('neg')

print("Number of positive samples:", len(positive_fileids))
print("Number of negative samples:", len(negative_fileids))

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
test_set = [(extract_features(line), 'Positive') for line in pos_reviews]


features_positive = [(extract_features(movie_reviews.words(fileids=[f])), 'Positive') for f in positive_fileids]
features_negative = [(extract_features(movie_reviews.words(fileids=[f])), 'Negative') for f in negative_fileids]

# Combine training set
features_train = features_positive + features_negative

# Train Naive Bayes classifier
classifier = NaiveBayesClassifier.train(features_train)

print("\nOverall accuracy of the classifier: " + str(nltk.classify.util.accuracy(classifier, test_set)*100)[:4]+"%")

# print("\nTop 10 most informative features:")
# for item in classifier.most_informative_features()[:10]:
#     print(item[0])


# pickle_out = open("classifier.pickle", "wb")
# pickle.dump(classifier, pickle_out)
# pickle_out.close()
