import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
from plotly import graph_objs as go
from dash.dependencies import Input, Output, State
import plotly.express as px

from word_cloud import get_words, most_common

# Screen 1: Course/trainer list

def row(course):

    fig = go.Figure(data = [go.Bar( y=[course[0]], x=[course[2]], orientation='h', width=0.4, marker_color='#109c33'),
                            go.Bar( y=[course[0]], x=[course[3]], orientation='h', width=0.4, marker_color='#eb4034')])

    fig.update_layout(barmode='stack',
                      xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                      yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                      margin=dict(l=0, r=0, b=0, t=0, pad=0),
                      paper_bgcolor="white",
                      plot_bgcolor="white",
                      showlegend=False,
                      height=40,
                      )
    return fig

def course_list(df):
    '''
    Returns a list of courses with corresponding total number of positive/negative reviews
    '''

    df = df.loc[df['Sentiment course'] != 0]

    courses = df['Course'].unique()

    course_list = []

    for course in courses:
        df2 = df.loc[df['Course'] == course]
        total_count = len(df2.index)
        df3 = df2.loc[df2['Sentiment course'] == 1]
        positive_count = len(df3.index)
        df3 = df2.loc[df2['Sentiment course'] == -1]
        negative_count = len(df3.index)
        sentiment_score = round((positive_count/total_count),2)
        course_list.append((course, total_count, positive_count, negative_count, sentiment_score))
    
    course_list = sorted(course_list, key = lambda x: x[4], reverse=True)
    
    return course_list

def trainer_list(df):
    '''
    Returns a list of trainers with corresponding total number of positive/negative reviews
    '''

    df = df.loc[df['Sentiment trainer'] != 0]

    trainers = df['Trainer'].unique()

    trainer_list = []

    for trainer in trainers:
        df2 = df.loc[df['Trainer'] == trainer]
        total_count = len(df2.index)
        df3 = df2.loc[df2['Sentiment trainer'] == 1]
        positive_count = len(df3.index)
        df3 = df2.loc[df2['Sentiment trainer'] == -1]
        negative_count = len(df3.index)
        sentiment_score = round((positive_count/total_count),2)
        trainer_list.append((trainer, total_count, positive_count, negative_count, sentiment_score))
    
    trainer_list = sorted(trainer_list, key = lambda x: x[4], reverse=True)
    
    return trainer_list

# Screen 2: Course charts

# Row 1
def top_trainers(df):
    df = df[(df["Sentiment trainer"] != 0)]

    trainer_names = []
    sentiments = []

    list_of_trainers = trainer_list(df)


    if len(list_of_trainers) <= 1:
        color_swatch = ['#238823']
    elif len(list_of_trainers) == 2:
        color_swatch = ['#238823', '#FFBF00']
    elif len(list_of_trainers) == 3:
        color_swatch = ['#238823', '#FFBF00', '#D2222D']
    elif len(list_of_trainers) == 4:
        color_swatch = ['#007000', '#238823', '#FFBF00', '#D2222D']
    elif len(list_of_trainers) == 5:
        color_swatch = ['#007000', '#238823', '#42a842', '#FFBF00', '#D2222D']
    elif len(list_of_trainers) == 6:
        color_swatch = ['#007000', '#238823', '#42a842', '#7fc24f', '#FFBF00', '#D2222D']
    elif len(list_of_trainers) == 7:
        color_swatch = ['#007000', '#0b7d0b', '#238823', '#349934', '#7fc24f', '#FFBF00', '#D2222D']
    elif len(list_of_trainers) == 8:
        color_swatch = ['#007000', '#0b7d0b', '#238823', '#349934', '#7fc24f', '#FFBF00', '#ff8800', '#D2222D']
    elif len(list_of_trainers) == 9:
        color_swatch = ['#007000', '#0b7d0b', '#238823', '#349934', '#42a842', '#7fc24f', '#FFBF00', '#ff8800', '#D2222D']
    else:
        extra_colors = []
        for i in range(len(list_of_trainers)-9):
            extra_colors.append('#349934')
        color_swatch = ['#007000',
                        '#0b7d0b',
                        '#238823',
                        '#349934'] + extra_colors + ['#42a842',
                                                     '#7fc24f',
                                                     '#FFBF00',
                                                     '#ff8800',
                                                     '#D2222D']


    for trainer in list_of_trainers:
        trainer_names.append(trainer[0])
        sentiments.append(trainer[4])

    layout = dict(showlegend=False,
                  margin=dict(l=110, r=10, b=30, t=5, pad=4),
                  yaxis=dict(autorange="reversed"),
                  xaxis=dict(showgrid=False,
                             zeroline=True,
                             showticklabels=False,
                             ),
    )

    trace = go.Bar(y=trainer_names,
                   x=sentiments,
                   orientation="h",
                   text=sentiments,
                   textposition='auto',
                   marker={'color' : color_swatch, 'colorscale': 'RdYlGn'},
                   hoverinfo='y',
                )

    return dict(data=[trace], layout=layout)

def course_sentiment_chart(df2):
    # df2 = df[(df['Date'] > '2018-03-01') & (df['Date'] < '2019-03-01')]
    # Removes reviews where no sentiment was given
    mask = (df2['Sentiment course'] != 0)
    df2 = df2.loc[mask]
    # Calculates average sentiment
    df2['Sentiment course'] = (df2['Sentiment course'] + 1)/2
    sentiments = (df2.set_index('Date')
                    .resample('M')['Sentiment course']
                    .mean()
                    .to_frame()
                    .reset_index())

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=sentiments["Date"],
            y=sentiments['Sentiment course'],
            # line_shape='spline',
            line=dict(color='#7e238c'),
            mode='lines',
            fill="tozeroy",
            hoverinfo='x+y',
            hovertemplate = 'Average sentiment: %{y:.2f}<Br>%{x}<extra></extra>',
        )
    )

    fig.update_layout(
        autosize=True,
        yaxis=dict(range=[0,1],
                   autorange=False,
                   showgrid=True,
                   zeroline=True,
                   showline=True,
                   visible=True,
                   linecolor='black'),
        margin=dict(l=33, r=25, b=37, t=5),
        paper_bgcolor="white",
        plot_bgcolor="white",
        xaxis=dict(
            zeroline=True,
            showgrid=True,
            showline=True,
            visible=True,
            linecolor='black',
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                        label="1m",
                        step="month",
                        stepmode="backward"),
                    dict(count=6,
                        label="6m",
                        step="month",
                        stepmode="backward"),
                    dict(count=1,
                        label="YTD",
                        step="year",
                        stepmode="todate"),
                    dict(count=1,
                        label="1y",
                        step="year",
                        stepmode="backward"),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type="date"
        )
    )


    return fig

# Row 2
def common_words_bar(df, polarity):

    if polarity == 'positive':
        df = df[(df["Sentiment course"] == 1)]
    if polarity == 'negative':
        df = df[(df["Sentiment course"] == -1)]

    frequencies = []
    common_words = []

    positive_words, negative_words = get_words(df)

    if polarity == 'positive':
        words = most_common(positive_words)
    if polarity == 'negative':
        words = most_common(negative_words)

    n = 0
    for word_freq in words:
        word = word_freq[0]
        frequency = word_freq[1]
        n += 1
        frequencies.append(frequency)
        common_words.append(word)
        if n == 15:
            break

    

    layout = dict(showlegend=False,
                  margin=dict(l=100, r=25, b=15, t=5, pad=4),
                  yaxis={'autorange': 'reversed'},
                  xaxis=dict(showticklabels=False,
                             showgrid=False,
                             zeroline=True,

                  ),
    )

    trace = go.Bar(x=frequencies[:15],
                   y=common_words[:15],
                   width=0.8,
                   orientation='h',

                )

    return dict(data=[trace], layout=layout)

def get_sentences(df, polarity, word=None):
    if word == None:
        return [""]

    if polarity == 'positive':
        df = df[(df["Sentiment course"] == 1)]
    if polarity == 'negative':
        df = df[(df["Sentiment course"] == -1)]


    reviews = [review for review in df['Review']]

    sentences = []

    for review in reviews:
        for sentence in review.split("."):
            if word.lower() in sentence.lower():
                sentences.append(sentence.strip())


    return sentences