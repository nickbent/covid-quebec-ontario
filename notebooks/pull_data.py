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




URL_GC = "https://health-infobase.canada.ca/src/data/covidLive/covid19.csv"

PROVINCES = ['Alberta', 'British Columbia', 'Manitoba',
       'New Brunswick', 'Newfoundland and Labrador', 'Nova Scotia',
       'Ontario', 'Prince Edward Island', 'Quebec', 'Saskatchewan','Northwest Territories', 'Yukon']

URL_UOFT = "https://docs.google.com/spreadsheets/d/1D6okqtBS3S2NRC7GFVHzaZ67DuTw7LX49-fqSLwJyeo/export?format=xlsx"

def pull_JHU_data(link_dict=JHU_LINKS,kind="cases",province_list=PROVINCES,keep_LatLong=False):
    """
    Pull data about Canada from the Johns Hopkins data source
    
    Parameters
    ----------
    link_dict : dict
        Has keys "cases", "deaths", "recovered" and corresponding links to the data
    kind : string
        "cases", "deaths" or "recovered". The default is "cases"
    province_list : list
        Provinces of interest (there are `provinces` like Diamond Princess in the JHU data)
    keep_LatLong : boolean
        Whether to keep the Lat and Long columns. If False, the other columns are converted to date type
    
    
    Returns
    -------
    df: pandas DataFrame 
        DataFrame with the Johns Hopkins data for Canada
    """
    url = link_dict[kind]
    df= pd.read_csv(url)
    df = df[df["Country/Region"]=="Canada"]
    df = df[df['Province/State'].isin( province_list)].set_index("Province/State")
    df.drop("Country/Region",axis=1,inplace=True)
    if keep_LatLong is False:
        df.drop(["Lat","Long"],axis=1,inplace=True)
        df.columns = pd.to_datetime(df.columns)
    return df



def pull_UofT_data(url=URL_UOFT,kind="cases"):
    """
    Pull the data from the University of Toronto project

    Parameters
    ----------
    url : 
        Link to the data source.
    kind : string
        "cases", "deaths" or "recovered". The default is "cases"    

    Returns
    -------
    data : pandas DataFrame
        DataFrame with the UofT data

    """
    d = {"cases":"Cases","deaths":"Mortality","recovered":"Recovered"}
    data = pd.read_excel(url, index_col=0, header=3,sheet_name = d[kind])
    return data


def pull_GC (url = URL_GC):
    data = pd.read_csv(url)
    data.date = pd.to_datetime(data.date,dayfirst=True)
    return data


if(__name__=="__main__"):


    df_JHU = pull_JHU_data()
    df_JHU.columns
    
    
    df_UofT = pull_UofT_data()
    
    print(df_UofT.groupby("province").agg({"provincial_case_id":"count"}))
    
    df_UofT.date_report.value_counts()
    
    print(df_JHU.sum(axis=0))
    
    dft = pull_UofT_data(URL_UOFT,kind="deaths")
    
    print(dft.groupby("province").agg({"province_death_id":"count"}))
