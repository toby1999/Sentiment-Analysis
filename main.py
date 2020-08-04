# -*- coding: utf-8 -*-

# System libraries
import pickle
import operator
import sys
import pandas as pd
import base64

image_filename = 'Data/Wordcloud_data/wordcloud_pos.png'
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

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
df = df[(df['Date'] < '2019-04-01')]




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
                                                    id='aspect-dropdown',
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
                                                    id="frequency-dropdown",
                                                    value="Q",
                                                    clearable=False,
                                                    options=[
                                                        {"label": "By week", "value": "W"},
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
                                                    value=3,
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
                                                    id='total-reviews-kpi',
                                                    style={'margin-top' : '0px',
                                                        'margin-bottom' : '0px',
                                                        "text-align" : "center"}
                                                ),
                                                html.P(
                                                    children="Total reviews",
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
                                        html.H2('Review frequency'),
                                        dcc.Graph(
                                            id="review-frequency",
                                            figure=frequency_chart(df, "Q")
                                        )
                                    ]
                                ),
                                # Overall pie
                                html.Div(
                                    id="pie1",
                                    className="dashboard_segment four columns",
                                    children=[
                                        html.H2(id="pie1-title", children="General sentiment"),
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
                                        html.H2(
                                            id="aspect-title",
                                            style={'display': 'inline-block'},
                                            children=["Reasons for positive feedback"]
                                        ),
                                        daq.ToggleSwitch(
                                            id='pie-polarity-toggle',
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
                                        html.H2(
                                            id='sentiment-chart-title',
                                            children=['Sentiment change']
                                        ),
                                        dcc.Graph(
                                            id='sentiment-chart',
                                            figure=sentiment_line_chart(df, 'Sentiment general', 'Q')

                                        )
                                    ]
                                ),
                                html.Div(
                                    className="dashboard_segment four columns",
                                    children=[
                                        html.H2(
                                            id='sentiment-bar-title',
                                            children=['Average sentiment']
                                        ),
                                        dcc.Graph(
                                            id='aspect-bar',
                                            figure=aspect_bar(df)
                                        )
                                    ]
                                ),
                            ]
                        ),
                        html.Br(),
                        html.Br(),
                    ]
                )
            ]
        )
    elif tab == 'tab-2':
        global nclicks
        nclicks = [None for i in range(len(course_list(df)))]+[None,0]
        global current_state
        current_state = []

        return html.Div(
            className="dashboard_container",
            children=[
                html.Div(
                    id='course_list_div',
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
                            id='course_list'
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
                html.Br(),

                html.Div(
                    html.H1(
                        id='title_div',
                        className='ten columns',
                        style={'text-align' : 'right',
                               'font-family': "HelveticaNeue",
                               'color' : 'rgb(64,64,64)'}
                    )
                ),

                html.Div(
                    id="course_main",
                    style={'display': 'none'},
                    children=[

                        # Row 0
                        html.Div(
                            className='row',
                            children=[
                                html.Div(
                                    id='graph23',
                                    className='dashboard_segment four columns',
                                    children=[
                                        html.H2("Average trainer sentiments"),
                                        dcc.Graph(
                                            figure=top_trainers(df),
                                            style={'height': '400px'},
                                        )
                                    ]
                                ),
                                html.Div(
                                    id='graph25',
                                    className='dashboard_segment eight columns',
                                    children=[
                                        html.H2("Last 12 months average course sentiment"),
                                        dcc.Graph(
                                            figure=course_sentiment_chart(df),
                                            style={'height': '400px'},
                                        )
                                    ]
                                )
                            ]
                        ),
                        html.Br(),

                        # Row 1
                        html.Div(
                            className='row',
                            children=[
                                html.Div(
                                    id='course_negative_word_freq_div',
                                    className='dashboard_segment three columns',
                                    children=[
                                        html.H2(
                                            id='course_features_title',
                                            style={'display' : 'inline-block'},
                                            children=["Top positive features"]
                                        ),
                                        dcc.Graph(
                                            id='course-positive-word-freq',
                                            style={'height': '400px'},
                                        )
                                    ]
                                ),
                                html.Div(
                                    id='table_course_div',
                                    className='dashboard_segment five columns',
                                    children=[
                                        html.H2("Reviews"),
                                        html.Div(
                                            id='list_course_reviews_div',
                                            style = {"height": "400px", "overflow": "auto"},
                                            children=[
                                                html.P(
                                                    id='list_course_reviews',
                                                )
                                            ]
                                        )
                                    ]
                                ),
                                html.Div(
                                    id='word_cloud_div',
                                    className='dashboard_segment four columns',
                                    children=[
                                        html.H2("Word cloud"),
                                    ]
                                )
                            ]
                        ),
                        html.Br(),
                    ]
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
            html.H3('Tab content 3'),
        ]),
    elif tab == 'tab-4':
        return html.Div(className="dashboard_container", children=[
            html.H3('Tab content 4')
        ])


# Update list of courses
@app.callback(
	Output('course_list', 'children'),
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
                            # Make above into seven columns
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
                                children=html.P("{}".format(course_list(df)[i][4]))),
                            ]) for i in range (courses) ]
            )
    ]

nclicks = [None for i in range(len(course_list(df)))]+[None, 0]
current_state = []

# Update course page
@app.callback(
        [dash.dependencies.Output('title_div','children'),
         dash.dependencies.Output('button_div','style'),
         dash.dependencies.Output('course_list_div','style'),
         dash.dependencies.Output('course_main','style'),
         dash.dependencies.Output('course-positive-word-freq','figure'),
         dash.dependencies.Output('list_course_reviews','children')],
        [dash.dependencies.Input('row {}'.format(i),'n_clicks') for i in range(len(course_list(df)))]+
        [dash.dependencies.Input('course-positive-word-freq', 'clickData')]+
        [dash.dependencies.Input('back-button', 'n_clicks')])


def update_dist(*argv):
    global nclicks
    global current_state
    global df
    
    clicked_word = ""
    course_name = ""

    # If word is clicked
    if argv[-2] != nclicks[-2] or (argv == nclicks):
        clicked_word = argv[-2]['points'][0]['label']
        course_name = current_state[0]
        button = current_state[1]
        course_table = current_state[2]
        course_main = current_state[3]
        figure = current_state[4]
        review_snippets = []
        sentences = get_sentences(figure, 'positive', word=clicked_word)
        for sentence in sentences:
            review_snippets.append(html.Hr())
            review_snippets.append(str(sentence)+'.')
            review_snippets.append(html.Br())

    else:
        clicked_word = None

    
    # If course is clicked
    for i in range(len(argv)-2):
        
        if argv[i] != nclicks[i]:

            course_name = str(course_list(df)[i][0])
            button = {}
            course_table = {'display' : 'none'}
            course_main = {}
            figure = df[(df["Course"] == course_name)]

            review_snippets = []
            sentences = get_sentences(figure, 'positive', word=clicked_word)
            for sentence in sentences:
                review_snippets.append(sentence)
                review_snippets.append(html.Br())
                review_snippets.append(html.Br())

            current_state = [course_name, button, course_table, course_main, figure, review_snippets]
            # print(current_state)
        
        
    # If back button is clicked
    if argv[-1] != nclicks[-1]:
        button = {'display' : 'none'}
        course_table = {}
        course_main = {'display' : 'none'}
        figure = pd.DataFrame({'Sentiment course':[0], 'Review':[""]})
        review_snippets = ""

    # if argv[-2] != nclicks[-2]:
        
    
    nclicks=argv


    return [course_name,
            button,
            course_table,
            course_main,
            common_words_bar(figure, 'positive'),
            review_snippets]




# Toggle positive/negative for aspect pie
@app.callback(
    dash.dependencies.Output('aspect-pie', 'figure'),
    [dash.dependencies.Input('pie-polarity-toggle', 'value'),
     dash.dependencies.Input("time-period-dropdown", "value")])

def update_output(switch, period):
    global df

    if period == 1:
        df2 = df[(df['Date'] > '2019-01-01') & (df['Date'] < '2019-04-01')]
    if period == 2:
        df2 = df[(df['Date'] > '2018-04-01') & (df['Date'] < '2019-04-01')]
    if period == 3:
        df2 = df[(df['Date'] < '2019-04-01')]

    if switch == False:
        return aspect_pie(df2, 'positive')
    else:
        return aspect_pie(df2, 'negative')

# Update title positive/negative for aspect pie
@app.callback(
    dash.dependencies.Output('aspect-title', 'children'),
    [dash.dependencies.Input('pie-polarity-toggle', 'value')])

def update_output(value):
    if value == False:
        return "Reasons for positive feedback"
    else:
        return "Reasons for negative feedback"

# update main pie chart based on dropdown's value
@app.callback(
    Output("overall-pie", "figure"),
    [Input("aspect-dropdown", "value"),
     Input("time-period-dropdown", "value")],
)
def overall_callback(aspect, period):
    global df

    if period == 1:
        df2 = df[(df['Date'] > '2019-01-01') & (df['Date'] < '2019-04-01')]
    if period == 2:
        df2 = df[(df['Date'] > '2018-04-01') & (df['Date'] < '2019-04-01')]
    if period == 3:
        df2 = df[(df['Date'] < '2019-04-01')]

    return overall_pie(df2, aspect)

# update title main pie chart based on dropdown's value
@app.callback(
    Output("pie1-title", "children"),
    [Input("aspect-dropdown", "value")],
)
def pie1_callback(value):
    if value == 7:  return 'General sentiment'
    if value == 8:  return 'Course sentiment'
    if value == 9:  return 'Trainer sentiment'
    if value == 10: return 'Venue sentiment'

# update sentiment-change chart based on dropdowns
@app.callback(
    Output("sentiment-chart", "figure"),
    [Input("aspect-dropdown", "value"),
     Input("frequency-dropdown", "value"),
     Input("time-period-dropdown", "value")],
)
def sentiment_chart_callback(value, freq, period):
    global df

    if period == 1:
        df2 = df[(df['Date'] > '2019-01-01') & (df['Date'] < '2019-04-01')]
    if period == 2:
        df2 = df[(df['Date'] > '2018-04-01') & (df['Date'] < '2019-04-01')]
    if period == 3:
        df2 = df[(df['Date'] < '2019-04-01')]

    if value == 7:  return sentiment_line_chart(df2,'Sentiment general', freq)
    if value == 8:  return sentiment_line_chart(df2,'Sentiment course', freq)
    if value == 9:  return sentiment_line_chart(df2,'Sentiment trainer', freq)
    if value == 10: return sentiment_line_chart(df2,'Sentiment venue', freq)

@app.callback(
    Output("aspect-bar", "figure"),
    [Input("time-period-dropdown", "value")],
)
def aspect_bar_callback(period):
    global df

    if period == 1:
        df2 = df[(df['Date'] > '2019-01-01') & (df['Date'] < '2019-04-01')]
    if period == 2:
        df2 = df[(df['Date'] > '2018-04-01') & (df['Date'] < '2019-04-01')]
    if period == 3:
        df2 = df[(df['Date'] < '2019-04-01')]
    
    return aspect_bar(df2)


# update title sentiment-change chart based on dropdowns
@app.callback(
    Output("sentiment-chart-title", "children"),
    [Input("aspect-dropdown", "value")],
)
def sentiment_chart_title_callback(value):
    if value == 7:  return 'Sentiment change'
    if value == 8:  return 'Course sentiment change'
    if value == 9:  return 'Trainer sentiment change'
    if value == 10: return 'Venue sentiment change'


# Update frequency chart based on dropdowns
@app.callback(
    Output("review-frequency", "figure"),
    [Input("frequency-dropdown", "value"),
     Input("time-period-dropdown", "value")],
)
def update_frequency_chart(freq, period):

    global df

    if period == 1:
        df2 = df[(df['Date'] > '2019-01-01') & (df['Date'] < '2019-04-01')]
    if period == 2:
        df2 = df[(df['Date'] > '2018-04-01') & (df['Date'] < '2019-04-01')]
    if period == 3:
        df2 = df[(df['Date'] < '2019-04-01')]

    return frequency_chart(df2, freq)


# Update percent change KPI
@app.callback(
    Output("percentage-indicator", "children"),
    [Input("aspect-dropdown", "value")],
)
def KPI_percent_indicator_callback(value):
    return percentage_change(df, value)

@app.callback(
    Output("total-reviews-kpi", "children"),
    [Input("time-period-dropdown", "value")],
)
def KPI_total_reviews_callback(period):
    global df

    if period == 1:
        df2 = df[(df['Date'] > '2019-01-01') & (df['Date'] < '2019-04-01')]
    if period == 2:
        df2 = df[(df['Date'] > '2018-04-01') & (df['Date'] < '2019-04-01')]
    if period == 3:
        df2 = df[(df['Date'] < '2019-04-01')]

    return str(len(df2.index))


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
