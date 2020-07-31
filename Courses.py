import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
from plotly import graph_objs as go
from dash.dependencies import Input, Output, State

from word_cloud import get_words, most_common

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
        percent_positive = round((positive_count/total_count),2)
        course_list.append((course, total_count, positive_count, negative_count, percent_positive))
    
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
        percent_positive = round((positive_count/total_count),2)
        trainer_list.append((trainer, total_count, positive_count, negative_count, percent_positive))
    
    trainer_list = sorted(trainer_list, key = lambda x: x[4], reverse=True)
    
    return trainer_list


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

def common_words_bar(df, polarity):

    df = df[(df["Sentiment course"] != 0)]

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
                  margin=dict(l=100, r=25, b=37, t=5, pad=4),
                  yaxis={'autorange': 'reversed'},
                  xaxis={'ticks': ''},
    )

    trace = go.Bar(x=frequencies[:15],
                   y=common_words[:15],
                   width=0.8,
                   orientation='h',

                )

    return dict(data=[trace], layout=layout)

def top_trainers(df):
    df = df[(df["Sentiment trainer"] != 0)]

    trainer_names = []
    sentiments = []

    trainer_lists = trainer_list(df)

    for trainer in trainer_lists:
        trainer_names.append(trainer[0])
        sentiments.append(trainer[4])

    layout = dict(showlegend=False,
                  margin=dict(l=33, r=33, b=70, t=5, pad=4),
    )

    trace = go.Bar(x=trainer_names,
                   y=sentiments,
                   width=0.5,
                )

    return dict(data=[trace], layout=layout)

def course_sentiment_chart(df):

    # Removes reviews where no sentiment was given
    mask = (df['Sentiment course'] != 0)
    df = df.loc[mask]
    # Calculates average sentiment
    df['Sentiment course'] = (df['Sentiment course'] + 1)/2
    sentiments = (df.set_index('Date')
                    .resample('M')['Sentiment course']
                    .mean()
                    .to_frame()
                    .reset_index())

    trace = go.Scatter(
        x=sentiments["Date"],
        y=sentiments['Sentiment course'],
        line_shape='spline',
        line=dict(color='#7e238c'),
        mode='lines',
    )



    layout = go.Layout(
        autosize=True,
        xaxis=dict(showgrid=False),
        yaxis=dict(range=[0,1.1], autorange=False),
        margin=dict(l=33, r=25, b=37, t=5, pad=4),
        paper_bgcolor="white",
        plot_bgcolor="white",
    )

    return {"data": [trace], "layout": layout}