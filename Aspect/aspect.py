import pandas as pd
import xml.etree.ElementTree as ET

tree = ET.parse('Data/Restaurants_Train.xml')
root = tree.getroot()

# Use this dataframe for multilabel classification
# Must use scikitlearn's multilabel binarizer

labeled_reviews = []
for sentence in root.findall("sentence"):
    entry = {}
    aterms = []
    aspects = []
    if sentence.find("aspectTerms"):
        for aterm in sentence.find("aspectTerms").findall("aspectTerm"):
            aterms.append(aterm.get("term"))
    if sentence.find("aspectCategories"):
        for aspect in sentence.find("aspectCategories").findall("aspectCategory"):
            aspects.append(aspect.get("category"))
    entry["text"], entry["terms"], entry["aspects"]= sentence[0].text, aterms, aspects
    labeled_reviews.append(entry)
labeled_df = pd.DataFrame(labeled_reviews)
print("there are",len(labeled_reviews),"reviews in this training set")
#    print(sentence.find("aspectCategories").findall("aspectCategory").get("category"))

# Save annotated reviews
labeled_df.to_pickle("annotated_reviews_df.pkl")
labeled_df.head()

from neuralcoref import Coref
import en_core_web_lg
spacy = en_core_web_lg.load()
coref = Coref(nlp=spacy)

# Define function for replacing pronouns using neuralcoref
def replace_pronouns(text):
    coref.one_shot_coref(text)
    return coref.get_resolved_utterances()[0]

# Read annotated reviews df, which is the labeled dataset for training
# This is located in the pickled files folder
annotated_reviews_df = pd.read_pickle("../pickled_files/annotated_reviews_df.pkl")
annotated_reviews_df.head(3)

# Create a new column for text whose pronouns have been replaced
annotated_reviews_df["text_pro"] = annotated_reviews_df.text.map(lambda x: replace_pronouns(x))

# uncomment below to pickle the new df
# annotated_reviews_df.to_pickle("annotated_reviews_df2.pkl")

# Read pickled file with replaced pronouns if it exists already
annotated_reviews_df = pd.read_pickle("annotated_reviews_df2.pkl")

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MultiLabelBinarizer

# Convert the multi-labels into arrays
mlb = MultiLabelBinarizer()
y = mlb.fit_transform(annotated_reviews_df.aspects)
X = annotated_reviews_df.text_pro

# Split data into train and test set
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=0)

# save the the fitted binarizer labels
# This is important: it contains the how the multi-label was binarized, so you need to
# load this in the next folder in order to undo the transformation for the correct labels.
filename = 'mlb.pkl'
pickle.dump(mlb, open(filename, 'wb'))

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB
from skmultilearn.problem_transform import LabelPowerset
import numpy as np

# LabelPowerset allows for multi-label classification
# Build a pipeline for multinomial naive bayes classification
text_clf = Pipeline([('vect', CountVectorizer(stop_words = "english",ngram_range=(1, 1))),
                     ('tfidf', TfidfTransformer(use_idf=False)),
                     ('clf', LabelPowerset(MultinomialNB(alpha=1e-1))),])
text_clf = text_clf.fit(X_train, y_train)
predicted = text_clf.predict(X_test)

# Calculate accuracy
np.mean(predicted == y_test)

# Test if SVM performs better
from sklearn.linear_model import SGDClassifier
text_clf_svm = Pipeline([('vect', CountVectorizer()),
                         ('tfidf', TfidfTransformer()),
                         ('clf-svm', LabelPowerset(
                             SGDClassifier(loss='hinge', penalty='l2',
                                           alpha=1e-3, max_iter=6, random_state=42)))])
_ = text_clf_svm.fit(X_train, y_train)
predicted_svm = text_clf_svm.predict(X_test)

#Calculate accuracy
np.mean(predicted_svm == y_test)

import pickle
# Train naive bayes on full dataset and save model
text_clf = Pipeline([('vect', CountVectorizer(stop_words = "english",ngram_range=(1, 1))),
                     ('tfidf', TfidfTransformer(use_idf=False)),
                     ('clf', LabelPowerset(MultinomialNB(alpha=1e-1))),])
text_clf = text_clf.fit(X, y)

# save the model to disk
filename = 'naive_model1.pkl'
pickle.dump(text_clf, open(filename, 'wb'))

#mlb.inverse_transform(predicted)
pred_df = pd.DataFrame(
    {'text_pro': X_test,
     'pred_category': mlb.inverse_transform(predicted)
    })

pd.set_option('display.max_colwidth', -1)
pred_df.head()
