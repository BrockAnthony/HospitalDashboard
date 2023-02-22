from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import vis1
import vis2

def clean_data(df):
    """
    cleaning sun data
    :param df: a data frame of sunspot info
    :return: a cleaned data frame with columns titled and data in the correct type
    """
    # splitting the data frame into columns and naming them
    df.columns = ['Year']
    df = df['Year'].str.split(';', expand=True)
    df.columns = ['Year', 'Month', 'Fractional', 'Sunspot', 'd', 'e', 'f']
    # casting data to needed type
    df['Sunspot'] = df['Sunspot'].astype('float')
    df['Year'] = df['Year'].astype('int')
    df['Fractional'] = df['Fractional'].astype('float')

    return df

# creating app and reading in data frame
app = Dash(__name__, assets_folder='/Users/vivianweigel/Desktop/DS3500/hw2')
f1 = pd.read_csv('monthlysun.csv')
f1 = clean_data(f1)

# Creating app layout
app.layout = html.Div(children=[
    # Title and logo section
    html.Div(id='header', children=[
        html.Div(id='titles', children=[
            html.H1('Sunspot Dashboard', id='title'),
            html.H5('Exploring sunspot trends with data collected by the World Data collective SILSO')]),
        html.Div(id='logos', children=[
            html.Img(src='https://www.sidc.be/silso/IMAGES/logos/LOGO-DEF-H75px.png')])
    ]),
    html.Div(id='body', children=[
    # Sunspots over time section
    html.Div(id='sect1', children=[
        html.P('Show smoothed data?'),
        dcc.Dropdown(id='smoothshow', options=['show', 'hide'], value='show'),
        html.P('Time frame (in months) to smooth data over:'),
        dcc.Input(id='smoother', value=13, placeholder=13),
        dcc.Graph(
            id='graph1',
            figure = vis1.plot(f1)
        ),
        dcc.RangeSlider(id='g1slider', min=1750, max=2022, step=50,
                        marks={1750: '1750', 1800: '1800', 1850: '1850', 1900: '1900',
                               1950: '1950', 2000: '2000', 2022: '2022'}, value=[1750,2022]),
    ]),

    html.Div(className='col2', children=[
        # Sun img
        html.Div(id='sect3', children=[
             html.P('Real time image of the sun:'),
             html.Img(id='sun_img', src='https://soho.nascom.nasa.gov/data/realtime/hmi_igr/1024/latest.jpg'),
             dcc.Slider(id='photoslider', min=0, max=40, step=10,
                        marks={0:'SDO Continuum', 10: 'SDO Magnetron', 20:'EIT 171', 30: 'EIT 195', 40: 'LASCO C2'})]),
        # sunspot period over time
        html.Div(id='sect2', children=[
            dcc.Graph(
             id='graph2',
             figure=vis2.plot(f1)),
            html.P('Period (in years) of Sunspot Cycle'),
            dcc.Input(id='period', value=11, placeholder=11)
         ]),

        ])])
])

# referring to slider and input to update first graph
@app.callback(
    Output('graph1', 'figure'),
    Input('g1slider', 'value'),
    Input('smoother', 'value'),
    Input('smoothshow', 'value'))
def plot_yr_range(yr_range, window, show):
    if show == 'show':
        fig = vis1.plot(f1, yr_range[0], yr_range[1], window)
        fig.update_layout(transition_duration=500)
    elif show == 'hide':
        fig = vis1.hide_smooth(f1, yr_range[0], yr_range[1], window)
        fig.update_layout(transition_duration=500)

    return fig

#referring to slider and input to update second graph
@app.callback(
    Output('graph2','figure'),
    Input('g1slider', 'value'),
    Input('period', 'value'))
def plot_variability(yr_range, period):
    fig = vis2.plot(f1, yr_range[0], yr_range[1], period)
    fig.update_layout(transition_duration=500)

    return fig

# referring to slider to change which image is shown
@app.callback(
    Output('sun_img', 'src'),
    Input('photoslider', 'value'))
def change_photo(value):
    # dictionary of img sources
    sun_imgs = {0:'https://soho.nascom.nasa.gov/data/realtime/hmi_igr/1024/latest.jpg',
                10:'https://soho.nascom.nasa.gov/data/realtime/hmi_mag/512/latest.jpg',
                20: 'https://soho.nascom.nasa.gov/data/realtime/eit_171/512/latest.jpg',
                30:'https://soho.nascom.nasa.gov/data/realtime/eit_195/512/latest.jpg',
                40:'https://soho.nascom.nasa.gov/data/realtime/c2/512/latest.jpg'}
    return sun_imgs[value]

if __name__ == '__main__':
    app.run_server(port=9090)
