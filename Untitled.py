import pickle
import pandas as pd

pickle_in = open("dataFrame.pickle", "rb")
dataFrame = pickle.load(pickle_in)

def showHead(n):
    '''
    Prints the first n reviews in the dataframe
    '''
    print(dataFrame.head(n))


showHead(15)
