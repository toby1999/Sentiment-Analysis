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
