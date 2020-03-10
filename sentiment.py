'''
https://hub.packtpub.com/how-to-perform-sentiment-analysis-using-python-tutorial/
'''

print("Loading modules")
import nltk.classify.util
import pickle
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews

def extract_features(word_list):
    return dict([(word, True) for word in word_list])

print("Initialising the dataframe")
positive_fileids = movie_reviews.fileids('pos')
negative_fileids = movie_reviews.fileids('neg')

print("Number of positive reviews:", len(positive_fileids))
print("Number of negative reviews:", len(negative_fileids))

features_positive = [(extract_features(movie_reviews.words(fileids=[f])), 'Positive') for f in positive_fileids]
features_negative = [(extract_features(movie_reviews.words(fileids=[f])), 'Negative') for f in negative_fileids]

print("Splitting the dataset")
# Split the data into train and test (80/20)
threshold_factor = 0.9
threshold_positive = int(threshold_factor * len(features_positive))
threshold_negative = int(threshold_factor * len(features_negative))

features_train = features_positive[:threshold_positive] + features_negative[:threshold_negative]
features_test = features_positive[threshold_positive:] + features_negative[threshold_negative:]
print("\nNumber of training datapoints:", len(features_train))
print("Number of test datapoints:", len(features_test))
print("Initialising the classifier")
# Train a Naive Bayes classifier
classifier = NaiveBayesClassifier.train(features_train)

print("\nAccuracy of the classifier:", nltk.classify.util.accuracy(classifier, features_test))
'''
print("\nTop 10 most informative words:")
for item in classifier.most_informative_features()[:10]:
    print(item[0])
'''

#pickle_out = open("classifier.pickle", "wb")
#pickle.dump(classifier, pickle_out)
#pickle_out.close()

pickle_in = open("classifier.pickle", "rb")
classifier = pickle.load(pickle_in)


def classify(string):
    probdist = classifier.prob_classify(extract_features(string.split()))
    pred_sentiment = probdist.max()
    if pred_sentiment == "Positive":
        return 1
    else:
        return 0

'''
while True:
    print("\nEnter string below (enter 'break' to exit)")
    string = str(input())
    if string == "break": break
    probdist = classifier.prob_classify(extract_features(string.split()))
    pred_sentiment = probdist.max()
    print("Predicted sentiment:", pred_sentiment)
    print("Probability:", round(probdist.prob(pred_sentiment), 2),"\n")
'''
