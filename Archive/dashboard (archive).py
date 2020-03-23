import pandas as pd
import pickle
import plotly.express as px
import chart_studio
from classify import classify
from plotly.graph_objs import *
import plotly.graph_objects as go
import plotly.offline as py



pickle_df  = open("Data/Pickle/dataFrame.pickle", "rb")
dataFrame  = pickle.load(pickle_df)

pickle_cl  = open("Data/Pickle/classifier.pickle", "rb")
classifier  = pickle.load(pickle_cl)



def companySentiments(dataFrame):

    average_sentiments = []

    count = 0
    sentiment_count = 0
    last_company = ""

    for row, column in dataFrame.iterrows():
        if row == 0: last_company = str(column[0])
        count += 1
        #print(last_company)
        review = str(column[4])
        company = column[0]
        sentiment = int(classify(review))
        sentiment_count += sentiment
        if company != last_company:
            average_sentiments.append((last_company, (sentiment_count/count)))
            last_company = company
            count = 0
            sentiment_count = 0
        if row == len(dataFrame.index) -1:
            average_sentiments.append((company, (sentiment_count/count)))
            print("Break")
            break

    for i in range(len(average_sentiments)):
        print(i, "\t", round(average_sentiments[i][1], 2), "\t", average_sentiments[i][0])

    x = []
    y = []

    for item in average_sentiments:
        x.append(item[0])
        y.append(item[1])

    return x,y

companySentiments = companySentiments(dataFrame)
x = companySentiments[0]
y = companySentiments[1]

def getLocations(dataFrame, inputCompany):

    reviews = []
    for row, column in dataFrame.iterrows():
        review = str(column[4])
        location = str(column[3])
        company = str(column[0])
        if company != inputCompany: continue
        if location == 'nan': continue
        reviews.append((review,column[3]))

    return reviews


Aviato = getLocations(dataFrame, "Aviato")

trainers = ["Cammy Massenburg",
            "Ronni Rutan",
            "Janay Rohe",
            "Sheridan Niver",
            "Rita Findlay",
            "Eli Stager",
            "Janae Watters",
            "Millicent Celaya",
            "Cristin Swinger",
            "Gil Paylor",
            "Delora Shealy",
            "Norma Dinkins",
            "Leonardo Olson",
            "Lily Bullock",
            "Charlene Serio",
            "Muriel Rosol",
            "Annie Ishida",
            "Kassandra Molton",
            "Romona Julien",
            "Raymon Viramontes",
            "Yajaira Lovell",]

courses = ["Management Development with Insights",
           "Business and Report Writing Skills",
           "Root Cause Analysis",
           "Interviewing successfully for recruitment",
           "Reception and Telephony Skills",
           "Assertiveness at Work",
           "Managing the Salesforce",
           "Presentation Skills",
           "Microsoft Excel Introduction",
           "Appraisal Skills Awareness"]

scores = [0.88, 0.70, 0.88, 0.84, 0.62, 0.91, 0.68, 0.65, 0.77, 0.75, 0.80, 0.65, 0.58, 0.62, 0.71, 0.79, 0.83, 0.77, 0.61, 0.70, 0.75]

data_overall = [
        {
            'values': [0.68, 0.12, 0.2],
            'type': 'pie',
            'hovertext' : ['Positive', 'Negative', 'Neutral'],
        }]

data_course = [
        {
            'values': [0.75, 0.12, 0.13],
            'type': 'pie',
            'hovertext' : ['Positive', 'Negative', 'Neutral'],
        }]

data_trainer = [
        {
            'values': [0.63, 0.16, 0.21],
            'type': 'pie',
            'hovertext' : ['Positive', 'Negative', 'Neutral'],
        }]

data_venue = [
        {
            'values': [0.55, 0.20, 0.25],
            'type': 'pie',
            'hovertext' : ['Positive', 'Negative', 'Neutral'],
        }]


import dash
import dash_core_components as dcc
import dash_html_components as html

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([

    html.Div(children='Toby Wigglesworth.'),
# Placeholder 1

    html.Div(html.H1(' ')),
    html.Div(html.H1('Acceleration Training.ltd')),
    # 4 pie charts: ->

    html.Div([
        html.Div([
            #html.H4('Average sentiment by Overall'),
            dcc.Graph(
                id='g11',
                figure={
                    'data': data_overall,
                    'layout': {
                    'title': 'Overall Sentiment',
                    'showlegend' : False,


            }})
        ], className="three columns"),

        html.Div([
            #html.H4('Average sentiment by Course'),
            dcc.Graph(
                id='g22',
                figure={
                    'data': data_course,
                    'layout': {
                    'title': 'Course Sentiment',
                    'showlegend' : False,


            }})
        ], className="three columns"),

        html.Div([
            #html.H4('Average sentiment by Trainer'),
            dcc.Graph(
                id='g33',
                figure={
                    'data': data_trainer,
                    'layout': {
                    'title': 'Trainer Sentiment',
                    'showlegend' : False,


            }})
        ], className="three columns"),

        html.Div([
            #html.H4('Average sentiment by Venue'),
            dcc.Graph(
                id='g44',
                figure={
                    'data': data_venue,
                    'layout': {
                    'title': 'Venue Sentiment',
                    'showlegend' : False,


            }})
        ], className="three columns"),
    ], className="row"),

    # 4 bar charts: ->
    html.Div([
        html.Div([
            #html.H4('Average sentiment by location'),
            dcc.Graph(
                id='g1',
                figure={
                    'data': [{'x': ["Peterborough", "Aylesford", "Birmingham", "London"],
                              'y': [0.77, 0.79, 0.85, 0.72], 'type': 'bar'}],
                    'layout': {
                    'title': 'Average sentiment by location'
            }})
        ], className="six columns"),

        html.Div([
            #html.H4('Average sentiment by Trainer'),
            dcc.Graph(
                id='g2',
                figure={
                    'data': [{'x': trainers,
                              'y': scores, 'type': 'bar'}],
                    'layout': {
                    'title': 'Average sentiment by Trainer'
            }})
        ], className="six columns"),
    ], className="row"),
    html.Div([
        html.Div([
            #html.H4('Top 10 performing courses'),
            dcc.Graph(
                id='g3',
                figure={
                    'data': [{'x': courses,
                              'y': [0.96,0.91,0.85,0.83,0.82,0.76,0.76,0.73,0.72,0.69], 'type': 'bar'}],
                    'layout': {
                    'title': 'Top 10 performing courses'
            }})
        ], className="six columns"),

        html.Div([
            #html.H4('Average sentiment over last 6 months'),
            dcc.Graph(
                id='g4',
                figure={
                    'data': [{'x': ["Jan","Feb","Mar","Apr","May"],
                              'y': [0.85,0.86,0.79,0.88,0.89], 'type': 'bar'}],
                    'layout': {
                    'title': 'Average sentiment over last 6 months'
            }})
        ], className="six columns"),
    ], className="row")
])




'''
app.layout = html.Div(children=[
    html.H1(children='Sentiment Analysis'),

    html.Div(children='Toby Wigglesworth.'),

    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                #{'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                {'x': x, 'y': y, 'type': 'bar', 'name': u'Montréal'},
            ],
            'layout': {
                'title': 'Average sentiment score by company'
            }
        }
    )

])

'''
if __name__ == '__main__':
    app.run_server(debug=True)

# Location, average sentiment
# Trainer, average sentiment
# Course, average sentiment
# Year, average sentiment

# Placeholder 1
