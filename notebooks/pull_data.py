#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 19:48:30 2020

@author: ortmann_j
"""


import pandas as pd


JHU_LINKS = {"cases":"https://github.com/CSSEGISandData/COVID-19/raw/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv",
             "deaths":"https://github.com/CSSEGISandData/COVID-19/blob/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv",
             "recovered":"https://github.com/CSSEGISandData/COVID-19/blob/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv"}

UofT_LINKS = {"cases":"https://docs.google.com/spreadsheets/d/1D6okqtBS3S2NRC7GFVHzaZ67DuTw7LX49-fqSLwJyeo/export?format=csv",
              "deaths":"https://docs.google.com/spreadsheets/d/1D6okqtBS3S2NRC7GFVHzaZ67DuTw7LX49-fqSLwJyeo/export?format=xlsx"
              }

PROVINCES = ['Alberta', 'British Columbia', 'Manitoba',
       'New Brunswick', 'Newfoundland and Labrador', 'Nova Scotia',
       'Ontario', 'Prince Edward Island', 'Quebec', 'Saskatchewan','Northwest Territories', 'Yukon']

URL_UOFT = "https://docs.google.com/spreadsheets/d/1D6okqtBS3S2NRC7GFVHzaZ67DuTw7LX49-fqSLwJyeo/export?format=csv"

def pull_JHU_data(kind="cases",link_dict=JHU_LINKS,province_list=PROVINCES):
    url = link_dict[kind]
    df= pd.read_csv(url)
    df = df[df["Country/Region"]=="Canada"]
    df = df[df['Province/State'].isin( province_list)].set_index("Province/State")
    return df



def pull_UofT_data(url=URL_UOFT):
    data = pd.read_csv(url, index_col=0, header=3)
    return data


if(__name__=="__main__"):


    df_JHU = pull_JHU_data()
    df_JHU.columns
    
    df_JHU["Lat"].value_counts()
    
    
    df_JHU.drop(["Lat","Long"],axis=1).sum(axis=1)
    
    df_UofT = pull_UofT_data()
    
    df_UofT.groupby("province").agg({"provincial_case_id":"count"})
    
    df_UofT.date_report.value_counts()
    
    print(df_JHU.sum(axis=0))
