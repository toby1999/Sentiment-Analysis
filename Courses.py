from plotly import graph_objs as go

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

    