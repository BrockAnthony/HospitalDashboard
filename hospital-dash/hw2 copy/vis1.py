
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def filter(df, min_y, max_y):
     """
     Filters the data for selected years
     :param df: df of data overtime
     :param min_y: year in the df
     :param max_y: year in the df
     :return: updated dataframe
     """
     #filtering for anything above min year
     df = df.loc[df.Year >= min_y]
     # filtering for below max year
     df = df.loc[df.Year <= max_y]
     return df

def plot(df, min_y = 1749, max_y = 2022, window = 13):
     """
     plots filtered data over time
     :param df: dataframe of data over time
     :param min_y: year in dataframe
     :param max_y: year in dataframe
     :param window: time period (int) over which to smooth data
     :return: updated figure (plot)
     """
     # creates figure and filters datafrane
     fig = go.Figure()
     df = filter(df, min_y, max_y)

     # Creates new column of smoothed data and drops null values
     df['Smoothed'] = df.Sunspot.rolling(int(window)).mean()
     df.dropna(inplace=True)

     # Plots data and updates the graph
     fig = px.line(df, x='Fractional', y=['Sunspot', 'Smoothed'], title='Sunspot Numbers Over Time',
                   labels={'Fractional': 'Year', 'value': 'Number of Sunspots'},
                   color_discrete_map={'Sunspot': 'slateblue',"Smoothed": 'red'}, height=400)
     fig.update_layout(plot_bgcolor= 'whitesmoke')

     return fig

def hide_smooth(df, min_y = 1749, max_y = 2022, window = 13):
     """
     plots filtered data over time w/o smoothed line
     :param df: dataframe of data over time
     :param min_y: year in dataframe
     :param max_y: year in dataframe
     :param window: time period (int) over which to smooth data
     :return: updated figure (plot)
     """
     fig = go.Figure()
     df = filter(df, min_y, max_y)

     # Plots data and updates the graph
     fig = px.line(df, x='Fractional', y='Sunspot', title='Sunspot Numbers Over Time',
                   labels={'Fractional': 'Year', 'value': 'Number of Sunspots'},
                   color_discrete_map={'Sunspot': 'slateblue'}, height=400)
     fig.update_layout(plot_bgcolor='whitesmoke')

     return fig