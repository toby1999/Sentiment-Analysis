# -*- coding: utf-8 -*-
print("")
import random
import pickle
import plotly
import unicodedata
import plotly.graph_objs as go
from plotly.offline import plot
import plotly.express as px
from classify import classify
# `Load the dataframe`using Pickle
pickle_df  = open("Data/Pickle/dataFrame.pickle", "rb")
df  = pickle.load(pickle_df)

df = df[ (df["Training company"] == "Aperture Science") ]

print(df.head()) # Print head of the dataframe



def sentiment_pie(data):
    # Trace pie chart
    trace = go.Pie(labels = ["Positive", "Negative", "Neutral"],
                 values = data,
                 marker = {
                 'colors' : ['rgb(10, 120, 0)',       # Green
                             'rgb(220, 85, 85)',      # Red
                             'rgb(195, 195, 195)',]}, # Grey
                 name = "Overall",
                 hoverinfo = 'label',
                 sort = False)
    layout = dict(title="Average Sentiment", showlegend=True)
    return dict(data=[trace], layout=layout)

def review_frequency():
    # Number of reviews per month
    trace = go.Scatter(
        x = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
        y = [50,56,44,65,59,60],
        name="Number of reviews by month",
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


def word_cloud():
    # Trace word cloud

    # Word cloud data
    random.choices(range(30), k=30)
    words = dir(go)[:30]
    colors = [plotly.colors.DEFAULT_PLOTLY_COLORS[random.randrange(1, 10)] for i in range(30)]
    weights = [random.randint(15, 35) for i in range(30)]

    trace = go.Scatter(x=[random.random() for i in range(30)],
                           y=[random.random() for i in range(30)],
                           mode='text',
                           text=words,
                           marker={'opacity': 0.3},
                           textfont={'size': weights, 'color': colors})

    layout = go.Layout(
             {'xaxis': {'showgrid': False, 'showticklabels': False, 'zeroline': False},
              'yaxis': {'showgrid': False, 'showticklabels': False, 'zeroline': False},
              'plot_bgcolor' : 'white'})

    return go.Figure(data=[trace], layout=layout)

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

def best_trainers(df):
    #df = df.groupby("Trainer")
    df = df["Trainer"].unique().tolist()
    trainers = []
    for trainer in df:
        trainers.append(trainer)

    fig = go.Figure(layout=dict(autosize=True,
                                xaxis=dict(showgrid=True),
                                margin=dict(l=33, r=25, b=37, t=5, pad=4),
                                paper_bgcolor="white",
                                plot_bgcolor="white")
    )

    fig.add_trace(go.Scatter(x=['Jan','Feb','Mar','Apr','May','Jun'], y=[0.74,0.76,0.69,0.71,0.70,0.75],
                    mode='lines+markers',
                    line_shape='spline',
                    name=trainers[0]))
    fig.add_trace(go.Scatter(x=['Jan','Feb','Mar','Apr','May','Jun'], y=[0.75,0.72,0.74,0.63,0.65,0.64],
                    mode='lines+markers',
                    line_shape='spline',
                    name=trainers[1]))
    return fig





import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input # For callbacks

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.Div([
        # Sentiment pie charts
        html.Div(
            dcc.Graph(id="sentiment-pie",
                figure=sentiment_pie([0.75, 0.08, 0.17])
            )
        ),
        # Dropdown
        html.Div(
            dcc.Dropdown(id='dropdown',
                options = [
                    {'label' : 'Overall', 'value' : 'Overall'},
                    {'label' : 'Course',  'value' : 'Course' },
                    {'label' : 'Trainer', 'value' : 'Trainer'},
                    {'label' : 'Venue',   'value' : 'Venue'  }
                ],
                value='Overall'
            )
        ),
        # Word cloud
        html.Div([
            dcc.Graph( id="wordCloud",
                figure=word_cloud()
            )
        ]),
        # Number of reviews
        html.Div(
            dcc.Graph(id="review frequency",
                figure=review_frequency()
            )
        ),
        html.Div(
            dcc.Graph(id="choropleth",
                figure=choropleth_map()
            )
        ),
        html.Div(
            dcc.Graph(id="trainers§",
                figure=best_trainers(df)
            )
        )
    ])
])

# @app.callback(dash.dependencies.Output('sentiment-pie', 'figure'),
#              [dash.dependencies.Input('dropdown', "value")])

# def updateFig(option): # passing in option from dropdown
#     return "Hello"

print("Success")
if __name__ == '__main__':
    app.run_server(debug=True)
