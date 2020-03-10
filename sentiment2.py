print("Loading modules and dataset")
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier as rfc
from sklearn.model_selection import RandomizedSearchCV
stopset = list(set(stopwords.words('english')))

def word_feats(words):
    return dict([(word, True) for word in words.split() if word not in stopset])


amzn = open("data/amazon_cells_labelled.txt").read()
imdb = open("data/imdb_labelled.txt").read()
yelp = open("data/yelp_labelled.txt").read()
# Combining the datasets
datasets = [amzn, imdb, yelp]
data = []
for dataset in datasets:
    data.extend(dataset.split('\n'))
# separate each label from each sample
dataset = [sample.split('\t') for sample in data]

posids = ["I love this sandwich.", "I feel very good about these beers.", "The movie is good"]
negids = ["I hate this sandwich.", "I feel worst about these beers.", "bad film", "the food wasn't good"]


for row in dataset:
    try:
        review = row[0]
        sentiment = row[1]
        if sentiment == "1":
            posids.append(review)
        else:
            negids.append(review)
    except:
        continue

print("Ready")


pos_feats = [(word_feats(f), 'positive') for f in posids ]
neg_feats = [(word_feats(f), 'negative') for f in negids ]
#print(pos_feats)
#print(neg_feats)
trainfeats = pos_feats + neg_feats
classifier = NaiveBayesClassifier.train(trainfeats)


#print(classifier.classify(word_feats("I thought the plot was very entertaining")))

while True:
    print("Enter text below for sentiment analysis (enter 'break' to exit)")
    string = str(input())
    if string == "break": break
    print(classifier.classify(word_feats(string)))
