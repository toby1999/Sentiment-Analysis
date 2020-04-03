# -*- coding: utf-8 -*-
import random
import pickle
import plotly
import calendar
import unicodedata
from datetime import date, timedelta
import datetime
import pandas as pd
from dateutil import rrule
from dateutil.relativedelta import relativedelta
import plotly.graph_objs as go
from plotly.offline import plot
import plotly.express as px
from classify import classify
import dash
import dash_table
import operator

# `Load the dataframe`using Pickle
pickle_df  = open("Data/Pickle/dataFrame.pickle", "rb")
df  = pickle.load(pickle_df)

df = df[(df["Training company"] == "Entertainment 720")]

colours = []
with open("Data/colours.txt", "r") as colours_file:
    for colour in colours_file:
        colours.append(colour.rstrip())
colours_file.close()

'''
# Word Cloud for each course/trainer/venue
'''


def word_cloud():
    fig = go.Figure()

    # Constants
    img_width = 1600
    img_height = 900
    scale_factor = 0.5


    # Add invisible scatter trace.
    # This trace is added to help the autoresize logic work.
    fig.add_trace(
        go.Scatter(
            x=[0, img_width * scale_factor],
            y=[0, img_height * scale_factor],
            mode="markers",
            marker_opacity=0
        )
    )
    # Configure axes
    fig.update_xaxes(
        visible=False,
        range=[0, img_width * scale_factor]
    )

    fig.update_yaxes(
        visible=False,
        range=[0, img_height * scale_factor],
        # the scaleanchor attribute ensures that the aspect ratio stays constant
        scaleanchor="x"
    )
    # Add image
    fig.add_layout_image(
        dict(
            x=0,
            sizex=img_width * scale_factor,
            y=img_height * scale_factor,
            sizey=img_height * scale_factor,
            xref="x",
            yref="y",
            opacity=1.0,
            layer="below",
            sizing="stretch",
            source="")
    )

    # Configure other layout
    fig.update_layout(
        width=img_width * scale_factor,
        height=img_height * scale_factor,
        margin={"l": 0, "r": 0, "t": 30, "b": 30, "pad": 50},
        paper_bgcolor="white",
        plot_bgcolor='white',
        autosize=True,
    )

    return fig

def aspect_pie(df):

    sentiments = {'Course':0, 'Trainer':0, 'Venue':0}

    for review in df.iterrows():
        sentiment = classify(review[1][4])
        if sentiment['Course'] == -1:
            sentiments['Course'] += 1
        if sentiment['Trainer'] == -1:
            sentiments['Trainer'] += 1
        if sentiment['Venue'] == -1:
            sentiments['Venue'] += 1

    sentiments = sorted(sentiments.items(), key=operator.itemgetter(1), reverse=True)

    # Trace pie chart
    trace = go.Pie(labels=[sentiments[0][0], sentiments[1][0], sentiments[2][0]],
                   values=[sentiments[0][1], sentiments[1][1], sentiments[2][1]],
                   name="Overall",
                   hoverinfo='label',
                   marker={"colors": ["rgb(178, 25, 43)",
                                       "rgb(230, 130, 103",
                                       "rgb(249, 196, 169)"]},
                   sort=True)

    layout = dict(showlegend=True)
    return dict(data=[trace], layout=layout)



def sentiment_pie(df, aspect):

    positive = 0
    negative = 0

    for review in df.iterrows():
        sentiment = classify(review[1][4])
        if sentiment[aspect] > 0:
            positive += 1
        if sentiment[aspect] < 0:
            negative += 1


    # Trace pie chart
    trace = go.Pie(labels=["Positive", "Negative"],
                 values=[positive, negative],
                 marker={"colors": ["#264e86", "#dcdee6"]},
                 name="Overall",
                 hoverinfo='label',
                 sort=False,
                 )
    layout = dict(showlegend=True)
    return dict(data=[trace], layout=layout)

def review_frequency(df, n):
    # Number of reviews per month
    today = datetime.date(2019,4,1) # temporary date for demo
    start_date = pd.Timestamp(today + relativedelta(days=-n))

    # months in daterange stored here
    days = []
    reviews = []
    # For loop to create a list of months
    for dt in rrule.rrule(rrule.DAILY, dtstart=start_date, until=today): # dt is a datetime.datetime
        day_start = pd.Timestamp(dt)
        day_end = pd.Timestamp(dt + relativedelta(days=1))
        # Filters data frame to each day
        mask = (df['Date'] >= day_start) & (df['Date'] < day_end)
        day_df = df.loc[mask]
        day = str(dt.day)
        month = str(calendar.month_name[dt.month])
        month = ''.join(month.split())[:3]
        date = month+" "+day
        days.append(date)

        reviews.append(len(day_df.index))

    trace = go.Scatter(
        x = days,
        y = reviews,
        name="Number of reviews by day",
        fill="tozeroy",
        fillcolor="#e6f2ff",
    )
    data = [trace]

    layout = go.Layout(
        autosize=True,
        xaxis=dict(showgrid=False, tickformat='%Y-%m-%d',tickmode="auto", nticks=6, showticklabels=False),
        xaxis_title="Date",
        yaxis_title="Number of reviews",
        margin=dict(l=33, r=25, b=40, t=50, pad=4),
        paper_bgcolor="white",
        plot_bgcolor="white",
        # title_text="Review frequency over the last " + str(n) + " days",
    )
    return {"data": data, "layout": layout}


# def word_cloud2():
#     # Trace word cloud
#
#     # Word cloud data
#     random.choices(range(30), k=30)
#     words = dir(go)[:30]
#
#     #"CHECK THIS LINE ABOUT COLOURS!"colors = [plotly.colors.DEFAULT_PLOTLY_COLORS[random.randrange(1, 10)] for i in range(30)]
#
#     weights = [random.randint(15, 35) for i in range(30)]
#
#     trace = go.Scatter(x=[random.random() for i in range(30)],
#                            y=[random.random() for i in range(30)],
#                            mode='text',
#                            text=words,
#                            marker={'opacity': 0.3},
#                            textfont={'size': weights, 'color': colors})
#
#     layout = go.Layout(
#              {'xaxis': {'showgrid': False, 'showticklabels': False, 'zeroline': False},
#               'yaxis': {'showgrid': False, 'showticklabels': False, 'zeroline': False},
#               'plot_bgcolor' : 'white'})
#
#     return go.Figure(data=[trace], layout=layout)

def choropleth_map():
    # Trace choropleth map
    scl = [[0.0, "rgb(38, 78, 134)"], [1.0, "#0091D5"]]  # colors scale

    data = [
        dict(
            type="choropleth",
            colorscale=scl,
            locations=["NY", "NJ", "CA", "CO"],
            z=[1,2,3,4],
            fitbounds="locations",
            locationmode="USA-states",
            marker=dict(line=dict(color="rgb(255,255,255)", width=2)),
            colorbar=dict(len=0.8),
        )
    ]

    layout = dict(
        autosize=True,
        geo=dict(
            scope="usa",
            projection=dict(type="albers usa"),
            lakecolor="rgb(255, 255, 255)",
        ),
        margin=dict(l=10, r=10, t=0, b=0),
    )
    return dict(data=data, layout=layout)


def trainer_sentiments(df, aspect, n, color):
    today = datetime.date(2019,4,1) # temporary date for demo
    # Daterange only includes current month if 'today' is beyond 25th of the month
    if today.day > 25:
        today += datetime.timedelta(7)
    # sets the daterange to the first of the month
    end_date = today.replace(day=1)
    start_date = pd.Timestamp(end_date + relativedelta(months=-n))

    # months in daterange stored here
    months = []
    # For loop to create a list of months
    for dt in rrule.rrule(rrule.MONTHLY, dtstart=start_date, until=end_date):
        months.append(calendar.month_name[dt.month])
    months.pop()

    # Filters data frame to only contain reviews in the last n months
    df = df[(df['Date'] >= start_date)]
    # Create a list of trainers from the data frame
    trainer_list = df[aspect].unique().tolist()
    # Sentiment values for each trainer stored here
    trainer_sentiments = []
    # For loop to calculate trainer sentiments for each month in daterange
    for i in range(len(trainer_list)):
        # filters the data frame to only include the current trainer
        trainer_df = df[(df[aspect] == trainer_list[i])]
        # lists of monthly sentiment values for each trainer stored here
        sentiment_values = []

        for dt in rrule.rrule(rrule.MONTHLY, dtstart=start_date, until=end_date):
            # Sentiments for each review stored here
            review_sentiments = []

            days_in_month = calendar.monthrange(dt.year, dt.month)[1]
            month_start = dt
            month_end = dt + timedelta(days=days_in_month)

            # Filters data frame to each month
            mask = (trainer_df['Date'] >= month_start) & (trainer_df['Date'] < month_end)
            reviews_df = trainer_df.loc[mask]

            # Iterates through data frame and classifies sentiments
            for review in reviews_df.iterrows():
                sentiment = classify(review[1][4])
                review_sentiments.append(sentiment[aspect])

            # calculate average sentiment across all reviews in the month
            if len(review_sentiments) == 0:
                sentiment_values.append(None)
            else:
                avg_sentiment = sum(review_sentiments)/len(review_sentiments)
                sentiment_values.append((avg_sentiment+1)/2)
        # Append monthly sentiment values for each trainer to list of 'sentiment_values'
        trainer_sentiments.append((sentiment_values, trainer_list[i].strip()))

    # Sentiment values for Plotly stored here
    sentiments = []
    # Exclude trainers not mentioned in any reviews
    for trainer in trainer_sentiments:
        x = False
        for sentiment in trainer[0]:
            if sentiment != None:
                x = True
        if x != True:
            continue
        sentiments.append(trainer)


    fig = go.Figure(layout=dict(autosize=True,
                                xaxis=dict(showgrid=True),
                                margin=dict(l=33, r=25, b=37, t=5, pad=4),
                                paper_bgcolor="white",
                                plot_bgcolor="white",
                                xaxis_title="Month",
                                yaxis_title="Sentiment score")
    )


    x = len(colours)//len(sentiments)
    count = 0
    cols = []

    for col in range(len(sentiments)):
        cols.append(colours[count])
        count += x

    if color ==1:
        for trainer, color in zip(sentiments, cols):
            fig.add_trace(go.Scatter(x=months, y=trainer[0],
                            mode='lines+markers',
                            # line_shape='spline',
                            connectgaps=True,
                            marker=dict(color=color),
                            name=trainer[1]))
    if color == 2:
        cols2 = ['rgb(250, 230, 37)',
                 'rgb(252, 200, 40)',
                 'rgb(240, 128, 79)',
                 'rgb(208, 77, 116)',
                 'rgb(186, 53, 136)',
                 'rgb(115, 1, 168)',
                 'rgb(13, 7, 136)']
        for trainer, color in zip(sentiments, cols2):
            fig.add_trace(go.Scatter(x=months, y=trainer[0],
                            mode='lines+markers',
                            # line_shape='spline',
                            connectgaps=True,
                            marker=dict(color=color),
                            name=trainer[1]))

    return fig

def df_to_table(df):
    df = df['Trainer'].unique().tolist()
    df2 = [0.98,0.57,0.67,0.82,0.65,0.70,0.75,0.41,0.62]
    data = {'Trainer' : df, 'Sentiment' : df2}


def generate_table(dataframe, max_rows=26):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns]) ] +
        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )



import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input # For callbacks

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.Div([

        html.Div([html.H1('Dashboard')]),
        # ROW 1
        html.Div([
            html.Div([
                html.H4('Overall sentiment'),
                dcc.Graph(id="sentiment-pie",
                    figure=sentiment_pie(df, 'Course')
                )
            ], className="four columns"),
            html.Div([
                html.H4('Reasons for negative feedback'),
                dcc.Graph(id="negative-pie2",
                    figure=aspect_pie(df)
                )
            ], className="four columns"),
            html.Div([
                html.H4('Review frequency'),
                dcc.Graph(id="review-frequency",
                    figure=review_frequency(df, 180)
                )
            ], className="four columns"),
        ], className="row"),


        # ROW 2
        html.Div([
            html.Div([
                html.H4('Trainer sentiments'),
                dcc.Graph(id="trainers",
                    figure=trainer_sentiments(df, 'Trainer', 6, 1)
                )
            ], className="eight columns"),

            html.Div([
                html.H4('Venue sentiments'),
                dcc.Graph(id="choropleth",
                    figure=choropleth_map()
                )
            ], className="four columns"),
        ], className="row"),


        # ROW 3

        html.Div([
            html.H4('Course sentiments'),
            dcc.Graph(id="courses",
                figure=trainer_sentiments(df, 'Course', 6, 2)
            )
        ]),

        # ROW 4
        # html.Div([
        #     html.Div([
        #         html.H3('Reasons for negative feedback'),
        #         dcc.Graph(id="negative-pie",
        #             figure=aspect_pie(df)
        #         )
        #     ], className="six columns"),


            # html.Div([
            #     html.H3('Sunburst'),
            #     dcc.Graph(id="sunburst",
            #         figure=sunburst()
            #     )
            # ], className="six columns"),
        # ]),

        # Dropdown
        # html.Div(
        #     dcc.Dropdown(id='dropdown',
        #         options = [
        #             {'label' : 'Overall', 'value' : 'Overall'},
        #             {'label' : 'Course',  'value' : 'Course' },
        #             {'label' : 'Trainer', 'value' : 'Trainer'},
        #             {'label' : 'Venue',   'value' : 'Venue'  }
        #         ],
        #         value='Overall'
        #     )
        # ),


        # Word cloud
        # html.Div([
        #     dcc.Graph( id="wordCloud",
        #         figure=word_cloud()
        #     )
        # ]),



        html.Div([
            html.H3('All courses'),
            generate_table(df, max_rows=10)

        ], className="twelve columns")

    ], style={"margin": "5%"},)
])



# @app.callback(dash.dependencies.Output('sentiment-pie', 'figure'),
#              [dash.dependencies.Input('dropdown', "value")])

# def updateFig(option): # passing in option from dropdown
#     return "Hello"

print("Success")
if __name__ == '__main__':
    app.run_server(debug=True)
