import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

from .utils import *
import math
import json

import numpy as np
import pandas as pd

from itertools import islice


POPULATION = [197385, 276368, 729997, 266112, 319004, 1942044, 382604, 146717, 92518, 44561, 90311, 420082, 422993, 494796, 589400, 1507070, 242399]

DENSITY = [8.9, 2.8, 38.8, 7.4, 31.2, 3889.8, 12.4, 2.5, 0.4, 0.1, 4.4, 27.9, 1710.9, 39.8, 28.4, 135.4, 35.0]
ICU_CAP = 1000
HEADERS= ["Region",  "Total Number of Cases", "Date of Infection"]

NHOOD_MAP = {
    'Côte-des-Neiges–Notre-Dame-de-Grâce' : 'Côte-des-Neiges-Notre-Dame-de-Grâce',
    'Plateau-Mont-Royal' : 'Le Plateau-Mont-Royal',
    "Baie-D'Urfé" : "Baie-d'Urfé",
    'Mercier–Hochelaga-Maisonneuve' : 'Mercier-Hochelaga-Maisonneuve',
    'Côte-Saint-Luc' : 'Côte-Saint-Luc',
    'Kirkland' : 'Kirkland',
    "L'Île-Bizard–Sainte-Geneviève" :"L'Île-Bizard-Sainte-Geneviève",
    'Pierrefonds–Roxboro' :'Pierrefonds-Roxboro',
    'Rivière-des-Prairies–Pointe-aux-Trembles' : 'Rivière-des-Prairies-Pointe-aux-Trembles',
    'Rosemont–La Petite Patrie' : 'Rosemont-La Petite-Patrie',
    'Saint-Léonard' : 'Saint-Léonard',
    'Senneville' : 'Senneville',
    'Ahuntsic–Cartierville' :'Ahuntsic-Cartierville',
    'Sud-Ouest' : 'Le Sud-Ouest',
    'Villeray–Saint-Michel–Parc-Extension' :'Villeray-Saint-Michel-Parc-Extension' 
    
}

def plot_total_cases(stacked_df, df, dates):
    total_cases = list(df.iloc[19])[1:]

    fig = px.bar(stacked_df, x="Date of Infection", y="Total Number of Cases", color = "Region", color_discrete_sequence= px.colors.qualitative.Light24)
    fig.add_trace(go.Scatter(x=dates, y=total_cases,
                        mode='lines',
                        name='Total'))
    fig.update_layout(legend_orientation="h",  xaxis = {"dtick" : 10})
    fig.update_layout(legend=dict( y=-0.45))

    fig.show()
    with open('plotly/total_cases.json', 'w') as f:
        f.write(fig.to_json())

def plot_region_cases(stacked_df, dates ):
    all_regions = stacked_df.Region.unique()
    regions_cases = [stacked_df.loc[stacked_df['Region'] == r]["Total Number of Cases"].to_list() for r in all_regions]

    fig = make_subplots(rows=9, cols=2, subplot_titles=tuple(all_regions[:17]), shared_xaxes=True, shared_yaxes = True)
    for  i,m in enumerate(regions_cases[:17]) :

        r = i//2+1
        c = i%2+1

        fig.add_trace(
        go.Scatter(x=dates, y=m, mode = "lines"),
        row=r, col=c
    )
        
    fig.update_layout(showlegend=False, title_text="Infection over time by Region", height=1000)
    fig.show()

    with open('plotly/infections_by_region.json', 'w') as f:
        f.write(fig.to_json())


def plot_hospitilazation(df, dates):
    hospitalization = list(df.loc[[28]].values)[0][31:]
    icu = list(df.loc[[29]].values)[0][31:]

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(x= dates[30:], y=hospitalization, name="Hospitalized"),

    )

    fig.add_trace(
        go.Scatter(x=dates[30:], y=icu, name="ICU"),
    )


    fig.add_trace(
        go.Scatter(x=dates[30:], y=[ICU_CAP]*len(dates[30:]), name="ICU Capacity" , mode='lines',),
    )
    fig.update_layout(title='Hospitalization',
                    xaxis_title='Date',
                    yaxis_title='Number of Patients')

    fig.show()

    with open('plotly/hospitilization.json', 'w') as f:
        f.write(fig.to_json())

def plot_new_cases(df, dates):
    new_cases = list(df.iloc[20])[2:]
    fiveday_avg = nday_avg(new_cases, 5)

    fig = go.Figure(data=go.Scatter(x=dates[1:], y=new_cases,
                        mode='lines',
                        name='New Cases'))

    fig.add_trace(go.Scatter(x=dates[8:], y=fiveday_avg,
                        mode='lines',
                        name='Five Day Average', visible = False))


    fig.update_layout(
        updatemenus=[
            dict(
                #type="buttons",
                direction="down",
                showactive = True,
                #active = 0,
                x=1,
                y=1.2,
                buttons=list([
                    dict(label="New Cases",
                        method="update",
                        args=[{"visible": [True,False ]},
                            {"title": 'New Cases', 
                                "xaxis.title" : 'Date',
                                "yaxis.title" : 'Number of Cases',
                                "yaxis.type": "linear",
                                #"xaxis.type": "linear",
                                "annotations" : [],
                            }]   ),
                    dict(label="5 day average",
                        method="update",
                        args=[{"visible": [False,True]},
                            {"title": 'Average Cases in Last 5 days', 
                                "xaxis.title" : 'Date',
                                "yaxis.title" : 'Number of Cases',
                                "yaxis.type": "linear",
                                #"xaxis.type": "linear",
                                "annotations" : [],
                            }]   ),

                ]),
            )
        ])

    fig.update_layout(title='New Cases Each Day',
                    xaxis_title='Date',
                    yaxis_title='Number of New Cases',  xaxis = {"dtick" : 10})
    fig.show()
    with open('plotly/new_cases.json', 'w') as f:
        f.write(fig.to_json())


def plot_testing(df, dates):
    positive = list(df.iloc[20])[3:]
    negative = list(df.iloc[22])[3:] 

    total_negative = list(np.cumsum(negative))
    total_positive = list(np.cumsum(positive))
    total_tests = total_negative+total_positive
    positive_per_test = [ pos/total for pos, total in zip(total_positive, total_tests)]  

    fig = go.Figure(data=[
        go.Bar(name='Negative', x=dates[2:], y=negative[2:] ,visible = False),
        go.Bar(name='Positive', x=dates[2:], y=positive[2:],  visible = False)])

    fig.update_layout(barmode='stack')

    fig.add_trace(go.Scatter(x=dates[3:], y=positive_per_test[3:],
                        mode='lines',
                        name='Positive Tests per Total Tests (Cumulative Average)'))

    fig.add_trace(go.Scatter(x=dates[3:], y=total_tests[3:],
                        mode='lines',
                        name='Total Tests',  visible = False))

    fig.update_layout(
                    xaxis_title='Date',
                    yaxis_title='Positive Tests per Total Test',  xaxis = {"dtick" : 10})

    fig.update_layout(
        updatemenus=[
            dict(
                #type="buttons",
                direction="down",
                showactive = True,
                #active = 0,
                x=1,
                y=1.2,
                buttons=list([
                    dict(label="Positive Tests Per",
                        method="update",
                        args=[{"visible": [False,False, True, False]},
                            {"title": 'Positive Tests per Total Tests (Cumulative Average)', 
                                "xaxis.title" : 'Date',
                                "yaxis.title" : 'Positive Tests per Total Test',
                                "yaxis.type": "linear",
                                #"xaxis.type": "linear",
                                "annotations" : [],
                            }]   ),
                    dict(label="Test",
                        method="update",
                        args=[{"visible": [True,True, False, False]},
                            {"title": 'Total Tests', 
                                "xaxis.title" : 'Date',
                                "yaxis.title" : 'Number of Tests',
                                "yaxis.type": "linear",
                                #"xaxis.type": "linear",
                                "annotations" : [],
                            }]   ),

                ]),
            )
        ])

    fig.show()
    with open('plotly/tested.json', 'w') as f:
        f.write(fig.to_json()) 


def plot_breakdown(df, dates):
    total = list(df.iloc[19][1:])
    dead = list(df.iloc[24])[1:]
    recovered = list(df.iloc[25])[1:]
    active = [ t-r-d for t,r,d in zip(total, recovered, dead)]

    dead_percent = [d/t*100 for d,t in zip(dead, total)]
    recovered_percent = [r/t*100 for r,t in zip(recovered, total)]
    active_percent = [a/t*100 for a,t in zip(active, total)]


    fig = go.Figure()

    fig.add_trace(
        go.Scatter(x= dates, y=dead, name="Deceased", visible = True),

    )
    fig.add_trace(
        go.Scatter(x=dates, y=dead_percent, name="Deceased Percent", visible = False),
    )
    fig.add_trace(
        go.Scatter(x= dates, y=recovered, name="Recovered", visible = True),
    )
    fig.add_trace(
        go.Scatter(x=dates, y=recovered_percent, name="Recovered Percent", visible = False),
    )
    fig.add_trace(
        go.Scatter(x= dates, y=active, name="Active"),
    )
    fig.add_trace(
        go.Scatter(x=dates, y=active_percent, name="Active Percent", visible = False),
    )
    fig.update_layout(
        updatemenus=[
            dict(
                #type="buttons",
                direction="down",
                showactive = True,
                #active = 0,
                x=1,
                y=1.5,
                buttons=list([
                    dict(label="Current Active",
                        method="update",
                        args=[{"visible": [True,False,True, False, True, False]},
                            {"title": 'Active, Deceased and Recovered Cases', 
                                "xaxis.title" : 'Date',
                                "yaxis.title" : 'Number of Cases',
                                "yaxis.type": "linear",
                                #"xaxis.type": "linear",
                                "annotations" : [],
                            }]   ),
                    dict(label="Percentage Active",
                        method="update",
                        args=[{"visible": [False,True,False, True, False, True]},
                            {"title": 'Percentage of Active, Deceased and Recovered Cases', 
                                "xaxis.title" : 'Date',
                                "yaxis.title" : 'Percentage of Cases',
                                "yaxis.type": "linear",
                                #"xaxis.type": "linear",
                                "annotations" : [],
                            }]   ),

                ]),
            )
        ])


    fig.update_layout(
        title_text="Active Cases",
    )
    fig.update_layout(legend_orientation="h")
    fig.update_layout(legend=dict( y=-0.4),  xaxis = {"dtick" : 10})
    fig.show()

    with open('plotly/cases.json', 'w') as f:
        f.write(fig.to_json())

def plot_map_per100k(lastday_df, quebec):

    fig = px.choropleth(lastday_df, geojson=quebec, color="Cases per 100k", locations="res_nm_reg", 
                    featureidkey= "properties.res_nm_reg", color_continuous_scale='Blues',
                    projection='conic equidistant'
                   )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(title='Total Cases per 100k')
    fig.show()
    with open('../plotly/map_population.json', 'w') as f:
        f.write(fig.to_json())

def plot_exponential(df, stacked_df):

    total = list(df.iloc[19][1:])

    region_cases = []
    for i in range(17):
        temp = list(df.iloc[i][1:])
        ix_0 = [i for i, t in enumerate(temp) if t >0]
        if len(ix_0) >0 : 
            temp = temp[ix_0[0]:]
        else : 
            temp = []
        region_cases.append(temp)

    region_cases_per_100k = []
    for i, r in enumerate(region_cases): 
        if r : 
            region_cases_per_100k.append( [ 100000*x/POPULATION[i] for x in r ])
        else:
            region_cases_per_100k.append([])

    total_cases_per_100k = [ 100000*x/8164361 for x in total ]
    regions = stacked_df.Region.unique()

    past_week = []
    for i,_ in enumerate(total[7:]):
        past_week.append(total[i:i+7]) 
    past_week_sum = [100000*(w[-1]-w[0])/8164361 for w in past_week]

    region_week = []
    for i, r in enumerate(region_cases): 
        if len(r)>=7 :
            temp = []
            for r0,r7 in zip(r,r[7:]):
                temp.append(100000*(r7-r0)/POPULATION[i])
            region_week.append( temp)
        else:
            region_week.append([])   

    fig = go.Figure()

    color = ['#EB89B5', '#5b7bd6','#ff6960', '#d11411', '#00b159', '#00aedb', '#f37735', '#ffc425',
            '#a200ff', '#f47835', '#d41243', '#8ec127', '#feda75', '#fa7e1e', '#962fbf', '#fa9e1e', 
            '#800000', '#FFFF00', '#7D3C98']

    fig.add_trace(go.Scatter(y=total_cases_per_100k,name = "All Quebec", mode = 'lines+markers'))

    for r_c, r in zip(region_cases_per_100k, regions):
        fig.add_trace(go.Scatter(y=r_c, name = r, mode = 'lines+markers'))

    # fig.update_layout(
    #     title_text='Exponential Growth since First Infection', # title of plot
    #     xaxis_title_text='Date since first infection', # xaxis label
    #     yaxis_title_text='Cases per 100k (log scale)', # yaxis label

    # )


    fig.add_trace(go.Scatter(x=total_cases_per_100k[7:], y=past_week_sum,name = "All Quebec", mode = 'lines+markers', visible=False,))


    for r_100, r_c, r in zip(region_cases_per_100k, region_week, regions):
        fig.add_trace(go.Scatter(x =r_100[7:] , y=r_c, name = r, mode = 'lines+markers', visible=False))

    fig.update_layout(
        xaxis_title_text='Date since 1st infection', # xaxis label
        yaxis_title_text='Cases per 100k (log scale)', # yaxis label

    )
    fig.update_layout(
        updatemenus=[
            dict(
                #type="buttons",
                direction="down",
                showactive = True,
                #active = 0,
                x=1,
                y=1.5,
                buttons=list([
                    dict(label="Growth per Date",
                        method="update",
                        args=[{"visible": [True]*18+ [False]*18},
                            {"title": 'Exponential Growth since First Infection', 
                                "xaxis.title" : 'Days since first infection',
                                "yaxis.title" : 'Cases per 100k (log scale)',
                                "yaxis.type": "linear",
                                "xaxis.type": "linear",
                                "annotations" : [],
                            }]   ),
                    dict(label="Growth per total Cases",
                        method="update",
                        args=[{"visible":  [False]*18+ [True]*18},
                            {"title": 'Exponential Growth per total cases',
                                "xaxis.title" : 'Cases per 100k ',
                                "yaxis.title" : 'New Cases per 100k in last week',
                                "yaxis.type": "linear",
                                "xaxis.type": "linear",
                            }]),
                                    dict(label="Growth per Date Log Scale",
                        method="update",
                        args=[{"visible": [True]*18+ [False]*18},
                            {"title": 'Exponential Growth since First Infection', 
                                "xaxis.title" : 'Days since first infection',
                                "yaxis.title" : 'Cases per 100k (log scale)',
                                "yaxis.type": "log",
                                "xaxis.type": "linear",
                                "annotations" : [],
                            }]   ),
                    dict(label="Growth per total Cases Log Scale",
                        method="update",
                        args=[{"visible":  [False]*18+ [True]*18},
                            {"title": 'Exponential Growth per total cases',
                                "xaxis.title" : 'Cases per 100k (log scale)',
                                "yaxis.title" : 'New Cases per 100k in last week(log scale)',
                                "yaxis.type": "log",
                                "xaxis.type": "log",
                            }]),
                ]),
            )
        ])


    fig.update_layout(
        title_text="Exponential",
    )
    fig.update_layout(legend_orientation="h")
    fig.update_layout(legend=dict( y=-0.4))


    fig.show()

    with open('plotly/exponential.json', 'w') as f:
        f.write(fig.to_json())


def plot_montreal_nhood(montreal_nhood, montreal_nhood_geojson):

    keys = list(montreal_nhood.keys())

    montreal_map_nhood = {}
    # montreal_rates = {}

    for key,val in montreal_nhood.items() :
        stripped = key.strip()
        if stripped in NHOOD_MAP: 
            montreal_map_nhood[nhood_map[stripped]] = int(val[0].replace(",","").replace("< ","").replace("<","").replace(" ",""))
        else : 
            montreal_map_nhood[stripped] = int(val[0].replace(",","").replace("< ","").replace("<","").replace(" ",""))
    # del montreal_map_nhood['Total à Montréal']
    # del montreal_map_nhood['Territoire à confirmer²']
    del montreal_map_nhood['Total for Montréal']
    del montreal_map_nhood['Territory to be confirmed2']
        #montreal_rates[key] = float(val[1].replace(",",""))

    montreal_df = pd.DataFrame(montreal_map_nhood.items(), columns=['Neighbourhoods', 'Cases'])

    fig = px.choropleth(montreal_df, geojson=montreal_nhood_geojson , color="Cases", locations='Neighbourhoods', 
                    featureidkey= "properties.NOM",
                    projection="mercator"
                    )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(title='Cases per Neighbourhood')
    fig.show()
    with open('plotly/map_montreal_nhood.json', 'w') as f:
        f.write(fig.to_json())

def plot_age(age_deaths, age_case):
    del age_deaths["Âge à déterminer"]
    age_deaths_map = {}
    for age, deaths in age_deaths.items():
        if age == 'Moins de 30 ans':
            key = '<30'
        elif age == '90 ans et plus': 
            key = '>90'
        else :
            key = age.strip(" ans")
        age_deaths_map[key] = string_to_float(deaths)
    deaths_ages_df = pd.DataFrame(age_deaths_map.items(), columns=['Ages', 'Deaths (%)'])

    del age_case['Âge à déterminer']
    age_cases_map = {}
    for age, deaths in age_case.items():
        if age == '90 ans ou plus': 
            key = '>90'
        else :
            key = age.strip(" ans")
        age_cases_map[key] = float(deaths.replace(",","."))
    ages_df = pd.DataFrame(age_cases_map.items(), columns=['Ages', 'Cases (%)'])


    fig = go.Figure([go.Bar(x=deaths_ages_df["Ages"], y=deaths_ages_df['Deaths (%)'])])

    fig.add_trace(
        go.Bar(x=ages_df["Ages"], y=ages_df['Cases (%)'], visible = False),
    )

    fig.update_layout(
        xaxis_title_text='Age ranges', # xaxis label
        yaxis_title_text='Percentage', # yaxis label

    )

    fig.update_layout(
        updatemenus=[
            dict(
                #type="buttons",
                direction="down",
                showactive = True,
                #active = 0,
                x=1,
                y=1.5,
                buttons=list([
                    dict(label="Deaths Age",
                        method="update",
                        args=[{"visible": [True,False]},
                            {"title": 'Deaths by Age', 
                                "xaxis.title" : 'Age',
                                "yaxis.title" : 'Percentage',
                                "yaxis.type": "linear",
                                #"xaxis.type": "linear",
                                "annotations" : [],
                            }]   ),
                    dict(label="Cases Age",
                        method="update",
                        args=[{"visible": [False,True]},
                            {"title": 'Cases by Age', 
                                "xaxis.title" : 'Ages',
                                "yaxis.title" : 'Percentage of Cases',
                                "yaxis.type": "linear",
                                #"xaxis.type": "linear",
                                "annotations" : [],
                            }]   ),

                ]),
            )
        ])


    fig.update_layout(
        title_text="Deaths by Age",
    )
    fig.update_layout(legend_orientation="h")
    fig.update_layout(legend=dict( y=-0.4))

    fig.show()

    with open('plotly/age.json', 'w') as f:
        f.write(fig.to_json())