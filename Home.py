import pandas as pd
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
from plotly import graph_objs as go

import operator
import datetime
from dateutil.relativedelta import relativedelta

def aspect_pie(df, polarity):

    sentiments = {'Course':0, 'Trainer':0, 'Venue':0}

    if polarity == 'positive':
        colorscheme = {"colors": ["rgb(0, 109, 44)",
                                  "rgb(75, 191, 106)",
                                  "rgb(161, 217, 155)"]}
        for review in df.iterrows():
            if review[1][8] == 1:
                sentiments['Course'] += 1
            if review[1][9] == 1:
                sentiments['Trainer'] += 1
            if review[1][10] == 1:
                sentiments['Venue'] += 1

    if polarity == 'negative':
        colorscheme = {"colors": ["rgb(178, 25, 43)",
                                  "rgb(230, 130, 103",
                                  "rgb(249, 196, 169)"]}
        for review in df.iterrows():
            if review[1][8] == -1:
                sentiments['Course'] += 1
            if review[1][9] == -1:
                sentiments['Trainer'] += 1
            if review[1][10] == -1:
                sentiments['Venue'] += 1

    sentiments = sorted(sentiments.items(), key=operator.itemgetter(1), reverse=True)

    # Trace pie chart
    trace = go.Pie(labels=[sentiments[0][0], sentiments[1][0], sentiments[2][0]],
                   values=[sentiments[0][1], sentiments[1][1], sentiments[2][1]],
                   marker=colorscheme,
                   hoverinfo='label',
                   hole=.5,
                   sort=True)

    layout = dict(showlegend=True, margin=dict(t=0, b=0))

    return dict(data=[trace], layout=layout)

def sentiment_pie(df, aspect):

    positive = 0
    negative = 0

    for review in df.iterrows():
        sentiment = int(review[1][aspect])
        if sentiment > 0:
            positive += 1
        if sentiment < 0:
            negative += 1


    # Trace pie chart
    trace = go.Pie(labels=["Positive", "Negative"],
                   values=[positive, negative],
                   marker={"colors": ["#264e86", "#dcdee6"]},
                   hoverinfo='label',
                   hole=.5,
                   sort=False)

    layout = dict(showlegend=True, margin=dict(t=0, b=0))

    return dict(data=[trace], layout=layout)


def frequency_chart(df, period):
    df["Date"] = pd.to_datetime(df["Date"])

    df = (
        df.groupby([pd.Grouper(key="Date", freq=period)])
        .count()
        .reset_index()
        .sort_values("Date")
    )

    trace = go.Scatter(
        x=df["Date"],
        y=df["Review"],
        fill="tozeroy",
        fillcolor="#e6f2ff",
    )

    data = [trace]

    layout = go.Layout(
        autosize=True,
        xaxis=dict(showgrid=False),
        margin=dict(l=33, r=25, b=37, t=5, pad=4),
        paper_bgcolor="white",
        plot_bgcolor="white",
    )

    return {"data": data, "layout": layout}



def reviews_today(df):
    today = datetime.date(2019,4,1)
    df["Date"] = pd.to_datetime(df["Date"])

    df = (
        df.groupby([pd.Grouper(key="Date", freq="D")])
        .count()
        .reset_index()
        .sort_values("Date", ascending=False)
    )

    df = df[(df['Date'] == pd.to_datetime(today))]
    reviews_today = df['Review'].values[0]

    return reviews_today


def average_sentiment(df, aspect, end_date, start_date):
    # Filter dataframe to date range
    start_date = pd.to_datetime(start_date, format="%Y-%m-%d")
    end_date = pd.to_datetime(end_date, format="%Y-%m-%d")
    # df["Date"] = pd.to_datetime(df["Date"], format="%Y-%m-%d")
    mask = (df['Date'] >= start_date) & (df['Date'] < end_date)
    df = df.loc[mask]

    if aspect == 'overall':
        aspect = 7
    if aspect == 'course':
        aspect = 8
    if aspect == 'trainer':
        aspect = 9
    if aspect == 'venue':
        aspect = 10

    positive = 0
    negative = 0

    for row in df.iterrows():
        if row[1][aspect] ==  1:
            positive += 1
        if row[1][aspect] == -1:
            negative += 1

    total = positive + negative

    if total == 0: return "No reviews"

    average_sentiment = positive / total

    return average_sentiment



def percentage_change(df, aspect):
    today = datetime.date(2019,3,31)

    quarter = ((today.month-1)//3) + 1

    if quarter == 1:
        last_quarter_end = today.replace(month=1, day=1) - relativedelta(days=1)
    if quarter == 2:
        last_quarter_end = today.replace(month=4, day=1) - relativedelta(days=1)
    if quarter == 3:
        last_quarter_end = today.replace(month=7, day=1) - relativedelta(days=1)
    if quarter == 4:
        last_quarter_end = today.replace(month=10, day=1) - relativedelta(days=1)

    last_quarter_start = last_quarter_end - relativedelta(months=3) + relativedelta(days=1)

    average_this_quarter = average_sentiment(df, aspect, today, last_quarter_end)
    if average_this_quarter == "No reviews": return "No reviews"

    average_last_quarter = average_sentiment(df, aspect, last_quarter_end, last_quarter_start)

    sentiment_change = (average_this_quarter - average_last_quarter)*100

    percentage_change = ("%+.0f" % sentiment_change) + "%"

    return percentage_change


def sentiment_bar(df, aspect):

    key = aspect.capitalize()
    trainers = df[key].unique().tolist()


    end_date = datetime.date(2019,4,1)
    start_date = datetime.date(2019,1,1)

    if key == 'Overall':
        aspect = 7
    if key == 'Course':
        aspect = 8
    if key == 'Trainer':
        aspect = 9
    if key == 'Venue':
        aspect = 10

    sentiments = []

    for trainer in trainers:
        trainer_df = df[(df[key] == trainer)]
        average = average_sentiment(trainer_df, aspect, end_date, start_date)
        sentiments.append(average)

    sentiments, trainers = zip(*sorted(zip(sentiments, trainers)))

    layout = dict(showlegend=False)

    trace = go.Bar(x=trainers,
                   y=sentiments,
                   width=0.5,
                   marker={'colorscale': 'Viridis'},
                   marker_color="rgb(31,119,180)",
                   )

    return dict(data=[trace], layout=layout)