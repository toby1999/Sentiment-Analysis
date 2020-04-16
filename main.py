# -*- coding: utf-8 -*-

# System libraries
import random
import pickle
import operator
import calendar
import datetime
from dateutil import rrule
from dateutil.relativedelta import relativedelta
import pandas as pd

# NLP libraries
import nltk
from classify import classify


# Plotly libraries
import plotly
import dash
import dash_table
import dash_auth
import plotly.graph_objs as go
import plotly.express as px
nltk.download('punkt')

VALID_USERNAME_PASSWORD_PAIRS = {
    'hello': 'world'
}

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

# average_sentiment(df,'overall', datetime.date(2019,4,1), datetime.date(2019,1,1))

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
                   # marker={"colors": ["#264e86", "#dcdee6"]},
                   # hoverinfo='label',
                   # sort=True,
                   marker={'colorscale': 'Viridis'},
                   marker_color="rgb(31,119,180)",
                   )

    # fig = go.FigureWidget(data=[go.Bar(x=trainers, y=sentiments,
    #                              marker={'color': y,
    #                                            'colorscale': 'Viridis'})])

    return dict(data=[trace], layout=layout)
    # return fig





sentiment_bar(df, 'trainer')


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
                sentiment_values.append("%.2f" % ((avg_sentiment+1)/2))
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

#
#
# def df_to_table(df, aspect):
#     item_list = df[aspect].unique().tolist()
#     sentiment_values = []
#     for item in item_list:
#         review_sentiments = []
#         new_df = df[(df[aspect] == item)]
#         for review in new_df.iterrows():
#             sentiment = classify(review[1][4])[aspect]
#             if sentiment == 0: continue
#             review_sentiments.append(sentiment)
#         if len(review_sentiments) == 0:
#             sentiment_values.append(None)
#         else:
#             avg_sentiment = sum(review_sentiments)/len(review_sentiments)
#             sentiment_values.append("%.2f" % ((avg_sentiment+1)/2))
#
#
#     data = {aspect : item_list, 'Sentiment' : sentiment_values}
#     df = pd.DataFrame(data, columns=[aspect,'Sentiment'])
#     df.sort_values(by=['Sentiment'], inplace=True, ascending=False,kind='quicksort')
#     return df
#
#
# def generate_table(dataframe, max_rows=26):
#     return html.Table(
#         # Header
#         [html.Tr([html.Th(col) for col in dataframe.columns]) ] +
#         # Body
#         [html.Tr([
#             html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
#         ]) for i in range(min(len(dataframe), max_rows))]
#     )
#


import dash
# import dash_daq as daq
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input # For callbacks

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__)

auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)

main_container = {
    'background': '#f5f5f5',
    'margin':'-10px',
    'margin-top':'-20px',
}


app.layout = html.Div(className="container", children=[


    # Header
    html.Div(
        # style=header,
        className="header",
        children=[
            html.Div(
                className="dashboard_container",
                children=[
                    html.Div(
                        className='four columns',
                        children=[
                            html.Img(
                                src='https://www.coursecheck.com/assets/img/coursecheck.svg',
                                style={'margin-left' : '0px',
                                       'margin-top' : '25px',
                                       'width' : '225px'
                                }
                            )
                        ]
                    ),
                    html.Div(
                        className='eight columns',
                        children=[
                            html.H3(
                                children='SENTIMENT ANALYSIS DASHBOARD',
                                style={
                                    'textAlign': 'right',
                                    'color': 'white',
                                    'margin-top' : '40px',
                                    'margin-right' : '0px',
                                }
                            )
                        ]
                    )
                ]
            )
        ]
    ),
    html.Br(),

    # Main Dashboard
    html.Div(
        className="dashboard_container",
        children=[
            # Dropdowns & top row indicators
            html.Div(
                className="row",
                style={"position" : "relative", "height" : "100px"},
                children=[
                    # Dropdowns
                    html.Div(
                        id="dropdowns",
                        className="dropdowns four columns",
                        children=[
                            html.Div(
                                style={'display': 'inline-block'},
                                className='three columns',
                                children=[
                                    dcc.Dropdown(
                                        id='sentiment-dropdown',
                                        value=7,
                                        clearable=False,
                                        options = [
                                            { 'label' : 'Overall', 'value' : 7  },
                                            { 'label' : 'Course',  'value' : 8  },
                                            { 'label' : 'Trainer', 'value' : 9  },
                                            { 'label' : 'Venue',   'value' : 10 }
                                        ]
                                    )
                                ]
                            ),
                            html.Div(
                                style={'display': 'inline-block'},
                                className='four columns',
                                children=[
                                    dcc.Dropdown(
                                        id="frequency_period_dropdown",
                                        value="W-MON",
                                        clearable=False,
                                        options=[
                                            {"label": "By day", "value": "D"},
                                            {"label": "By week", "value": "W-MON"},
                                            {"label": "By month", "value": "M"},
                                        ]
                                    )
                                ]
                            ),
                            html.Div(
                                style={'display': 'inline-block'},
                                className='five columns',
                                children=[
                                    dcc.Dropdown(
                                        id="time_period_dropdown",
                                        value=1,
                                        clearable=False,
                                        options=[
                                            {"label": "Last quarter", "value": 1},
                                            {"label": "Last 12 months", "value": 2},
                                            {"label": "All time", "value": 3},
                                        ]
                                    )
                                ]
                            )
                        ]
                    ),
                    # Indicators
                    html.Div(
                        id="indicators",
                        className="indicators eight columns",
                        children=[
                            html.Div(
                                style={'display': 'inline-block'},
                                className='dashboard_segment four columns',
                                children=[
                                    html.H1(
                                        children=str(len(df.index)),
                                        style={'margin-top' : '0px',
                                               'margin-bottom' : '0px',
                                               "text-align" : "center"}
                                    ),
                                    html.P(
                                        children="Reviews",
                                        style={'margin-top' : '0px',
                                               'margin-bottom' : '0px',
                                               "text-align" : "center"}
                                    )
                                ]
                            ),
                            html.Div(
                                style={'display': 'inline-block'},
                                className='dashboard_segment four columns',
                                children=[
                                    html.H1(
                                        children=reviews_today(df),
                                        style={'margin-top' : '0px',
                                               'margin-bottom' : '0px',
                                               "text-align" : "center"}
                                    ),
                                    html.P(
                                        children="Reviews today",
                                        style={'margin-top' : '0px',
                                                'margin-bottom' : '0px',
                                                "text-align" : "center"}
                                    )
                                ]
                            ),
                            html.Div(
                                style={'display': 'inline-block'},
                                className='dashboard_segment four columns',
                                children=[
                                    html.H1(
                                        id='percentage-indicator',
                                        children=percentage_change(df, 'overall'),
                                        style={'margin-top' : '0px',
                                               'margin-bottom' : '0px',
                                               "text-align" : "center"}
                                    ),
                                    html.P(
                                        children="Since last quarter",
                                        style={'margin-top' : '0px',
                                               'margin-bottom' : '0px',
                                               "text-align" : "center"}
                                    )
                                ]
                            )
                        ]
                    )
                ]
            ),
            html.Br(),


            # ROW 1
            html.Div(
                className="row",
                children=[
                    # Frequency chart
                    html.Div(
                        className="dashboard_segment four columns",
                        children=[
                            html.P('Review frequency'),
                            dcc.Graph(
                                id="review-frequency",
                                figure=frequency_chart(df, "W-MON")
                            )
                        ]
                    ),
                    # Overall pie
                    html.Div(
                        id="pie1",
                        className="dashboard_segment four columns",
                        children=[
                            html.P(id="pie1-title", children="Overall sentiment"),
                            dcc.Graph(id="overall-pie",
                                figure=sentiment_pie(df, 'Sentiment overall'),
                                config={'displayModeBar': False}
                            )
                        ]
                    ),
                    # Positive pie
                    html.Div(
                        className="dashboard_segment four columns",
                        children=[
                            html.P("Reasons for positive feedback"),
                            dcc.Graph(id="positive-pie",
                                figure=aspect_pie(df, 'positive'),
                                config={'displayModeBar': False}
                            )
                        ]
                    )
                ]
            ),
            html.Br(),


            # ROW 2
            html.Div(
                className="row",
                children=[
                    html.Div(
                        className="dashboard_segment eight columns",
                        children=[
                            html.P('Trainer sentiments'),
                            dcc.Graph(
                                figure=sentiment_bar(df, 'trainer')
                            )
                            # dcc.Graph(
                            #     id="trainers",
                            #     figure=trainer_sentiments(df, 'Trainer', 6, 1)
                            # )
                        ]
                    ),

                    # Negative pie
                    html.Div(
                        className="dashboard_segment four columns",
                        children=[
                            html.P("Reasons for negative feedback"),
                            dcc.Graph(id="negative-pie",
                                figure=aspect_pie(df, 'negative'),
                                config={'displayModeBar': False}
                            )
                        ]
                    )


                    # html.Div([
                    #     html.H4('Venue sentiments'),
                    #     dcc.Graph(id="choropleth",
                    #         figure=choropleth_map()
                    #     )
                    # ], className="four columns"),
                ]
            ),
            html.Br(),

            # ROW 3

            # html.Div([
            #     html.H4('Course sentiments'),
            #     dcc.Graph(id="courses",
            #         figure=trainer_sentiments(df, 'Course', 12, 2)
            #     )
            # ]),

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



            # html.Div([
            #     html.H3('All courses'),
            #     generate_table(df_to_table(df, 'Trainer'))
            #
            # ], className="twelve columns")

    ])
])

# update pie chart figure based on dropdown's value
@app.callback(
    Output("overall-pie", "figure"),
    [Input("sentiment-dropdown", "value")],
)
def overall_callback(value):
    aspect=value
    return sentiment_pie(df, aspect)


@app.callback(
    Output("pie1-title", "children"),
    [Input("sentiment-dropdown", "value")],
)
def pie1_callback(value):
    if value == 7:  return 'Overall sentiment'
    if value == 8:  return 'Course sentiment'
    if value == 9:  return 'Trainer sentiment'
    if value == 10: return 'Venue sentiment'


# Frequency chart callback
@app.callback(
    Output("review-frequency", "figure"),
    [Input("frequency_period_dropdown", "value")],
)
def converted_leads_callback(value):
    return frequency_chart(df, value)


@app.callback(
    Output("percentage-indicator", "children"),
    [Input("sentiment-dropdown", "value")],
)
def percent_indicator_callback(value):
    return percentage_change(df, value)


#
# @app.callback(
#     Output("trainers", "figure"),
#     [Input("trainer-dropdown", "value")],
# )
# def trainer_callback(value):
#     n = value
#     return trainer_sentiments(df, 'Trainer', n, 1)
#


print("Success")
if __name__ == '__main__':
    app.run_server(debug=True)

from flask import escape

def helloWorld(request):
    """ Responds to an HTTP request using data from the request body parsed
    according to the "content-type" header.
    Args:
        request (flask.Request): The request object.
        <
http://flask.pocoo.org/docs/1.0/api/#flask.Request
>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <
http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response
>.
    """
    content_type = request.headers['content-type']
    if content_type == 'application/json':
        request_json = request.get_json(silent=True)
        if request_json and 'name' in request_json:
            name = request_json['name']
        else:
            raise ValueError("JSON is invalid, or missing a 'name' property")
    elif content_type == 'application/octet-stream':
        name = request.data

    elif content_type == 'text/plain':
        name = request.data

    elif content_type == 'application/x-www-form-urlencoded':
        name = request.form.get('name')
    else:
        raise ValueError("Unknown content type: {}".format(content_type))

    return app.index()
