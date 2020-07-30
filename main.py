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

pd.options.mode.chained_assignment = None

# Load the dataframe using Pickle
pickle_df  = open("Data/Pickle/dataFrame.pickle", "rb")
df  = pickle.load(pickle_df)

df = df[(df["Training company"] == "Entertainment 720")]

# aspect_bar(df)

import dash
import dash_daq as daq
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
                            html.H6(
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
                dcc.Tab(label='Venue',
                        value='tab-4',
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
                                                        { 'label' : 'General', 'value' : 7  },
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
                                                    value="M",
                                                    clearable=False,
                                                    options=[
                                                        {"label": "By day", "value": "D"},
                                                        {"label": "By week", "value": "W-MON"},
                                                        {"label": "By month", "value": "M"},
                                                        {"label": "By quarter", "value": "Q"},
                                                        {"label": "By year", "value": "A"},
                                                    ]
                                                )
                                            ]
                                        ),
                                        html.Div(
                                            style={'display': 'inline-block'},
                                            className='five columns',
                                            children=[
                                                dcc.Dropdown(
                                                    id="time-period-dropdown",
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
                                                    children=percentage_change(df, 'general'),
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
                                            figure=frequency_chart(df, "M")
                                        )
                                    ]
                                ),
                                # Overall pie
                                html.Div(
                                    id="pie1",
                                    className="dashboard_segment four columns",
                                    children=[
                                        html.P(id="pie1-title", children="General sentiment"),
                                        dcc.Graph(id="overall-pie",
                                            figure=overall_pie(df, 'Sentiment general'),
                                            config={'displayModeBar': False}
                                        )
                                    ]
                                ),
                                # Positive pie
                                html.Div(
                                    className="dashboard_segment four columns",
                                    children=[
                                        html.P(
                                            id="aspect-title",
                                            style={'display': 'inline-block'},
                                            children=["Reasons for positive feedback"]
                                        ),
                                        daq.ToggleSwitch(
                                            id='polarity-toggle',
                                            style={'display': 'inline-block', 'float':'right', 'margin-top':'5px'},
                                            size=30,
                                            value=False
                                        ),
                                        # html.Div(id='toggle-switch-output'),
                                        dcc.Graph(
                                            id="aspect-pie",
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
                                        html.P(
                                            id='sentiment-chart-title',
                                            children=['Overall sentiment change']
                                        ),
                                        dcc.Graph(
                                            id='sentiment-chart',
                                            figure=sentiment_chart(df, ['Sentiment general',
                                                                        'Sentiment trainer',
                                                                        'Sentiment course'], 'M')

                                        )
                                    ]
                                ),
                                html.Div(
                                    className="dashboard_segment four columns",
                                    children=[
                                        html.P(
                                            id='sentiment-bar-title',
                                            children=['Average sentiment']
                                        ),
                                        dcc.Graph(
                                            id='sentiment-bar',
                                            figure=sentiment_bar(df)
                                        )
                                    ]
                                ),
                            ]
                        ),
                        html.Br()
                    ]
                )
            ]
        )
    elif tab == 'tab-2':
        global nclicks
        nclicks = [None for i in range(len(course_list(df)))]+[0]

        return html.Div(
            className="dashboard_container",
            children=[
                html.Div(
                    id='course_div',
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
                        html.Hr(),

                        html.Div(
                            id='course_list_div'
                        ),
                    ]
                ),
                html.Div(
                    id='button_div',
                    style={'display' : 'none'},
                    className='two columns',
                    children=[
                        html.Button('Back', id='back-button', className='back-button', n_clicks=0)
                    ]
                ),

                html.Div(
                    html.H1(
                        id='title_div',
                        className='ten columns',
                        style={'text-align' : 'right', 'vertical-align': 'middle', 'font-family': "HelveticaNeue", 'color' : 'rgb(64,64,64)'}
                    )
                ),

                dcc.Dropdown(
                    id='div_num_dropdown',
                    style={'display': 'none'},
                    options=[{'label':i, 'value':i} for i in range (5)],
                    value=1
                ),
            ]
        ),
    elif tab == 'tab-3':
        return html.Div(className="dashboard_container", children=[
            html.H3('Tab content 3')
        ]),
    elif tab == 'tab-4':
        return html.Div(className="dashboard_container", children=[
            html.H3('Tab content 4')
        ])



@app.callback(
	Output('course_list_div', 'children'),
  	[Input('div_num_dropdown', 'value')])

def update_div(num_div):
   	
    courses = len(course_list(df))

    return [
           html.Div(
                children=[
                    html.Div(
                        className='row cell',
                        id="row {}".format(i),
                        children=[
                            html.Div(
                                className='seven columns cell_text',
                                children=html.P(course_list(df)[i][0])),
                            html.Div(
                                className='two columns',
                                children=dcc.Graph(id=f'Bar #{i}',
                                                config={'staticPlot': True},
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

nclicks = [None for i in range(len(course_list(df)))]+[0]


@app.callback(
        [dash.dependencies.Output('title_div','children'),
         dash.dependencies.Output('button_div','style'),
         dash.dependencies.Output('course_div','style')],
        [dash.dependencies.Input('row {}'.format(i),'n_clicks') for i in range(len(course_list(df)))]+
        [dash.dependencies.Input('back-button', 'n_clicks')])


def update_dist(*argv):
    global nclicks
    
    title = ""
    
    # If course is clicked
    for i in range(len(argv)-1):
        if argv[i] != nclicks[i]:
            title = str(course_list(df)[i][0])
            button = {'display' : 'block'}
            courses = {'display' : 'none'}
        
    # If back button is clicked
    if argv[-1] != nclicks[-1]:
        button = {'display' : 'none'}
        courses = {'display' : 'inline'}
    
    nclicks=argv


    return title, button, courses




# Update positive/negative aspect pie

@app.callback(
    dash.dependencies.Output('aspect-pie', 'figure'),
    [dash.dependencies.Input('polarity-toggle', 'value')])

def update_output(value):
    if value == False:
        return aspect_pie(df, 'positive')
    else:
        return aspect_pie(df, 'negative')

@app.callback(
    dash.dependencies.Output('aspect-title', 'children'),
    [dash.dependencies.Input('polarity-toggle', 'value')])

def update_output(value):
    if value == False:
        return "Reasons for positive feedback"
    else:
        return "Reasons for negative feedback"

# update figure main pie chart based on dropdown's value
@app.callback(
    Output("overall-pie", "figure"),
    [Input("sentiment-dropdown", "value")],
)
def overall_callback(value):
    aspect=value
    return overall_pie(df, aspect)

# update figure sentiment chart based on dropdown's value
@app.callback(
    Output("sentiment-chart", "figure"),
    [Input("sentiment-dropdown", "value"),
     Input("frequency_period_dropdown", "value")],
)
def sentiment_chart_callback(value, freq):
    if value == 7:  return sentiment_chart(df,['Sentiment general',
                                               'Sentiment course',
                                               'Sentiment trainer'], freq)
                                               
    if value == 8:  return sentiment_chart(df,['Sentiment course'], freq)
    if value == 9:  return sentiment_chart(df,['Sentiment trainer'], freq)
    if value == 10: return sentiment_chart(df,['Sentiment venue'], freq)

# update title main pie chart based on dropdown's value
@app.callback(
    Output("pie1-title", "children"),
    [Input("sentiment-dropdown", "value")],
)
def pie1_callback(value):
    if value == 7:  return 'General sentiment'
    if value == 8:  return 'Course sentiment'
    if value == 9:  return 'Trainer sentiment'
    if value == 10: return 'Venue sentiment'

# update title sentiment chart based on dropdown's value
@app.callback(
    Output("sentiment-chart-title", "children"),
    [Input("sentiment-dropdown", "value")],
)
def sentiment_chart_title_callback(value):
    if value == 7:  return 'Sentiment change'
    if value == 8:  return 'Course sentiment change'
    if value == 9:  return 'Trainer sentiment change'
    if value == 10: return 'Venue sentiment change'


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
