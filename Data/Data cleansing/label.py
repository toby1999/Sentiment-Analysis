import pandas as pd
from datetime import datetime

spreadsheet = pd.read_excel ('coursecheck_data.xlsx') # Open spreadsheet
dataset = pd.DataFrame(spreadsheet,
                       columns= ['General Comments'])

positive = open("positive.txt", "r")
negative = open("negative.txt", "r")

completed_positive = len(positive.readlines())
completed_negative = len(negative.readlines())

log = open("log.txt", "r")

lines = log.read().splitlines()
last_line = int(lines[-1].split(" ")[-1]) # Get line number from last time.

log = open("log.txt", "a")

def getReviews(data):
    '''
    Returns a list of reviews from the spreadsheet
    '''
    reviews = []
    for row in data.itertuples():
        comment = str(row[1])
        if comment == "nan":
            continue
        comment = comment.split(".")
        for sentence in comment:
            sentence = sentence.strip()
            if len(sentence) < 2: continue
            reviews.append(sentence)
    return reviews


reviews = getReviews(dataset)

reviews_remaining = len(reviews) - completed_positive - completed_negative
print((len(reviews) - reviews_remaining), 'total sentences labelled so far')
print(completed_positive, "positive sentences labelled")
print(completed_negative, "negative sentences labelled\n")
print(reviews_remaining, "sentences remaining")

print("\nEnter (1) for positive, (2) for negative, or any other key to exit.")

log.write("\nStart: " + str(datetime.now()))

for i in range(len(reviews)):
    if i < last_line: continue
    print("\n\n" + str(i-101) + ":    " + reviews[i])
    entry = str(input())

    if entry == '1':
        positive.write(reviews[i] + "\n")
    elif entry == '2':
        negative.write(reviews[i] + "\n")
    elif entry == '3':
        continue
    else:
        log.write("\nEnd:   " + str(datetime.now()))
        log.write("\nCompleted up to line " + str(i) + "\n")
        log.close()
        positive.close()
        negative.close()
        break
