"""code to create the map and associated graphs"""
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

COSTS = ['Cost of Charity Care','Total Bad Debt Expense','Cost of Uncompensated Care',
             'Total Unreimbursed and Uncompensated Care','Overhead Non-Salary Costs',
             'Depreciation Cost','Wage-Related Costs (Core)', 'Wage-Related Costs (RHC/FQHC)',
             'Total Salaries (adjusted)','Contract Labor','Wage Related Costs for Part - A Teaching Physicians',
             'Wage Related Costs for Interns and Residents', 'Inventory', 'Investments',
             'Total Other Expenses']

INCOME = ['Total Assets','Inpatient Revenue','Outpatient Revenue',
             'Net Income from Service to Patients','Total Other Income',
             'Total Income', 'Net Revenue from Medicaid']

MAIN =['Net Income', 'Total Costs', 'Net Patient Revenue']

def create_map(df):
    # Plotting using plotly
    # Inputting token
    # mapping with changing color
    pd.options.plotting.backend = 'plotly'
    px.set_mapbox_access_token(
        'pk.eyJ1Ijoid2VpZ2Vsdml2aWFuIiwiYSI6ImNsMXdhYjVrcjBiZ3AzZWxtczZjNHd6OGIifQ.tc-vqaSVnexmAp1s9ocCUw')

    # mapping with changing size of the points
    fig = px.scatter_mapbox(df, lat='LATITUDE', lon="LONGITUDE",
                            hover_data=["City", "State Code", "Net Income"],
                            hover_name="NAME_x",
                            size='Absolute Net Income', size_max=30,
                            color='Sign Net Income',
                            )


    #changing where initial map show
    fig.update_layout(
        hovermode='closest',
        mapbox=dict(
            accesstoken='pk.eyJ1Ijoid2VpZ2Vsdml2aWFuIiwiYSI6ImNsMXdhYjVrcjBiZ3AzZWxtczZjNHd6OGIifQ.tc-vqaSVnexmAp1s9ocCUw',
            bearing=0,
            center=go.layout.mapbox.Center(
                lat=39.8,
                lon=-96.5
            ),
            pitch=0,
            zoom=2.6
        )
    )

    return fig

def create_pie(df, hospital, choice = 'Costs'):
    if choice == 'Income':
        cats = ['Total Assets','Inpatient Revenue','Outpatient Revenue',
             'Net Income from Service to Patients','Total Other Income',
             'Total Income', 'Net Revenue from Medicaid']
    else:
        cats = COSTS

    df = df.loc[df['NAME'] == hospital]
    for index, row in df.iterrows():
        amounts = []
        for col in cats:
            amounts.append(df[col][index])
    pie_df = pd.DataFrame()
    pie_df['Expense'] = cats
    pie_df['Amount($)'] = amounts

    fig = px.pie(pie_df, values='Amount($)', names='Expense')
    return fig

def bar_chart(df, hospital):
    df2 = df.mean(axis=0)
    df = df.loc[df['NAME'] == hospital]

    hospital = []

    # gathering hospital values
    for index, row in df.iterrows():
        amounts = []
        for col in MAIN:
            amounts.append(df[col][index])
            hospital.append(df['NAME'][index])

    # getting averages
    for col in MAIN:
        amounts.append(df2[col])
        hospital.append('Avg. of All Hospitals')

    # creating bar chart data frame
    bar_df = pd.DataFrame()
    bar_df['Hospital Metrics'] = MAIN * 2
    bar_df['Amount($)'] = amounts
    bar_df['Hospital'] = hospital

    # creating figure
    fig = px.bar(bar_df, y='Amount($)', x='Hospital Metrics', color='Hospital', barmode='group', title='General Hospital Metrics for Selected Hospital')
    fig.update_layout(legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.01
    ))


    return fig

def double_bar_chart(df, hospital1, hospital2, choice = 'Costs', per_bed = 'Total Costs'):
    #getting new df
    df = df.loc[(df['NAME'] == hospital1) | (df['NAME'] == hospital2)]

    # getting choice of analysis
    if choice == 'Income':
        cats = ['Total Assets','Inpatient Revenue','Outpatient Revenue',
             'Net Income from Service to Patients','Total Other Income',
             'Total Income', 'Net Revenue from Medicaid']
    else:
        cats = COSTS

    amounts = []
    hospital = []
    if per_bed == 'Total Costs':
        # creating new df to graph
        for index, row in df.iterrows():
            for col in cats:
                amounts.append(df[col][index])
                hospital.append(df['NAME'][index])
        pie_df = pd.DataFrame()
        pie_df['Expense'] = cats * 2
        pie_df['Amount($)'] = amounts
        pie_df['Hospital'] = hospital
    else:
        # creating new df to graph
        for index, row in df.iterrows():
            num_bed = float(df['Number of Beds'][index])
            for col in cats:
                amount = float(df[col][index])
                amounts.append(amount/num_bed)
                hospital.append(df['NAME'][index])
        pie_df = pd.DataFrame()
        pie_df['Expense'] = cats * 2
        pie_df['Amount($)'] = amounts
        pie_df['Hospital'] = hospital


    #graphing the bar chart
    fig = px.bar(pie_df, y='Amount($)', x='Expense', color='Hospital', barmode='group')
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ))

    return fig

def scatter(df, y_ax):
    fig = px.scatter(df, x='Net Income', y=y_ax, hover_name='NAME')

    return fig
