import plotly.express as px


def generate_chart(df, chart_type, chart_x, chart_y):
    """
    Takes query result and chart info from LLM.
    Returns a Plotly figure or None.
    """

    # no chart needed
    if chart_type == "none" or chart_x is None or chart_y is None:
        return None

    # check columns exist in dataframe
    if chart_x not in df.columns or chart_y not in df.columns:
        return None

    if chart_type == "bar":
        fig = px.bar(df, x=chart_x, y=chart_y)

    elif chart_type == "line":
        fig = px.line(df, x=chart_x, y=chart_y)

    elif chart_type == "pie":
        fig = px.pie(df, names=chart_x, values=chart_y)

    elif chart_type == "scatter":
        fig = px.scatter(df, x=chart_x, y=chart_y)

    else:
        return None

    return fig