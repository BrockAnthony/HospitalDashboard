import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import vis1

def plot(df, min_y = 1749, max_y = 2022, period = 11):
    """
    overlays filtered data over a period
    :param df: dataframe of data points overtime
    :param min_y: year in df
    :param max_y: year in df
    :param period: int of period
    :return: updated figure (plot)
    """
    # filtering for user selected year range
    df = vis1.filter(df, min_y, max_y)
    df['Years'] = df['Fractional'] % int(period)

    #Plotting the data
    fig = px.scatter(df, x='Years', y='Sunspot', title='Variability of Sunspots',
                     labels={'Fractional': 'Year', 'Sunspot': 'Number of Sunspots'},
                     color_discrete_sequence=['blue'], height=300, width=600)

    #updating the figure
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)')

    return fig