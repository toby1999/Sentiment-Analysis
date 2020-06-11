# -*- coding: utf-8 -*-

# System libraries
import pickle
import operator
import sys
import pandas as pd

# NLP libraries
from classify import classify
import nltk
nltk.download('punkt')

# Tabs
from Home import *
from Courses import *
from Trainers import *


# Load the dataframe using Pickle
pickle_df  = open("Data/Pickle/dataFrame.pickle", "rb")
df  = pickle.load(pickle_df)

df = df[(df["Training company"] == "Entertainment 720")]



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
    

for course in course_list(df):
    print(course)



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




import dash
import dash_core_components as dcc
import dash_html_components as html

from dash.dependencies import Output, Input # For callbacks

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, suppress_callback_exceptions=True)

app.layout = html.Div(className="container", children = [
    # Header
    html.Div(
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

    # represents the URL bar, doesn't render anything
    dcc.Location(id='url', refresh=False),

    dcc.Link('Navigate to "/"', href='/'),
    html.Br(),
    dcc.Link('Navigate to "/page-2"', href='/page-2'),

    # content will be rendered in this element
    html.Div(id='page-content'),

    dcc.Tabs(id='page-tabs',
            value='tab-1',
            parent_className='custom-tabs',
            className='custom-tabs-container',
            children=[
                dcc.Tab(label='Home',
                        value='tab-1',
                        className='custom-tab',
                        selected_className='custom-tab--selected'),
                dcc.Tab(label='Courses',
                        value='tab-2',
                        className='custom-tab',
                        selected_className='custom-tab--selected'),
                dcc.Tab(label='Trainers',
                        value='tab-3',
                        className='custom-tab',
                        selected_className='custom-tab--selected'),
            ]
    ),
    html.Div(id='page-tabs-content')
])

@app.callback(Output('page-tabs-content', 'children'),
              [Input('page-tabs', 'value')])

def render_content(tab):
    if tab == 'tab-1':
        return html.Div(
            children=[
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
                            ]
                        ),
                        html.Br()
                    ]
                )
            ]
        )
    elif tab == 'tab-2':
        return html.Div(
            className="dashboard_container",
            children=[
                html.Div(
                    id='table-headers',
                    className='row',
                    children=[
                        html.Div(
                            id='title-label',
                            className='seven columns table_header',
                            children=html.P('Course Name'),
                        ),
                        html.Div(
                            className='two columns table_header',
                            children=html.P(''),
                        ),
                        html.Div(
                            className='two columns table_header',
                            children=html.P('Quantity'),
                        ),
                        html.Div(
                            className='one columns table_header',
                            children=html.P('Score'),
                        )
                    ]
                ),
                        
                        

                html.Div(id='div_variable'),

                dcc.Dropdown(
                    id='div_num_dropdown',
                    style={'visibility': 'hidden'},
                    options=[{'label':i, 'value':i} for i in range (5)],
                    value=1
                ),
            ]
        ),
    elif tab == 'tab-3':
        return html.Div(className="dashboard_container", children=[
            html.H3('Tab content 3')
        ])

@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    return html.Div([
        html.H3('You are on page {}'.format(pathname))
    ])

@app.callback(
	Output('div_variable', 'children'),
  	[Input('div_num_dropdown', 'value')]
)


def update_div(num_div):
   	
    courses = len(course_list(df))

    return [
           html.Div(
                children=[
                    html.Div(
                        className='row cell',
                        children=[
                            html.Div(
                                className='seven columns cell_text',
                                children=html.P(course_list(df)[i][0])),
                            html.Div(
                                className='two columns',
                                children=dcc.Graph(id=f'Bar #{i}',
                                                # config={'staticPlot': True},
                                                figure=row(course_list(df)[i]))),
                            html.Div(
                                className='two columns cell_text',
                                children=html.P(course_list(df)[i][1])),
                            html.Div(
                                className='one columns cell_text',
                                children=html.P("{}%".format(course_list(df)[i][4]*100))),
                            
                            ]) for i in range (courses) ]
            )
    ]

# update figure main pie chart  (based on dropdown's value)
@app.callback(
    Output("overall-pie", "figure"),
    [Input("sentiment-dropdown", "value")],
)
def overall_callback(value):
    aspect=value
    return sentiment_pie(df, aspect)

# update title main pie chart (based on dropdown's value)
@app.callback(
    Output("pie1-title", "children"),
    [Input("sentiment-dropdown", "value")],
)
def pie1_callback(value):
    if value == 7:  return 'Overall sentiment'
    if value == 8:  return 'Course sentiment'
    if value == 9:  return 'Trainer sentiment'
    if value == 10: return 'Venue sentiment'


# Frequency chart day/week/month callback
@app.callback(
    Output("review-frequency", "figure"),
    [Input("frequency_period_dropdown", "value")],
)
def time_period_callback(value):
    return frequency_chart(df, value)

# Percent change KPI 
@app.callback(
    Output("percentage-indicator", "children"),
    [Input("sentiment-dropdown", "value")],
)
def KPI_percent_indicator_callback(value):
    return percentage_change(df, value)



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
            print(name)
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
