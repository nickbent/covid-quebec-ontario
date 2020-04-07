#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 19:48:30 2020

@author: ortmann_j
"""


import pandas as pd


JHU_LINKS = {"cases":"https://github.com/CSSEGISandData/COVID-19/raw/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv",
             "deaths":"https://github.com/CSSEGISandData/COVID-19/raw/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv",
             "recovered":"https://github.com/CSSEGISandData/COVID-19/raw/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv"}

URL_GC = "https://health-infobase.canada.ca/src/data/covidLive/covid19.csv"


URL_UOFT = "https://docs.google.com/spreadsheets/d/1D6okqtBS3S2NRC7GFVHzaZ67DuTw7LX49-fqSLwJyeo/export?format=xlsx"

DATA_FOLDER="../data/Canada/"

JHU_LOCAL_LINKS = {s : DATA_FOLDER+"JHU_{}.csv".format(s) for s in ["cases","deaths","recovered"]}

GC_LOCAL_LINK = DATA_FOLDER+"GC.csv"

UOFT_LOCAL_LINKS = {s : DATA_FOLDER + "UofT_{}.csv".format(s) for s in ["cases","deaths","recovered","testing"]}




PROVINCES = ['Alberta', 'British Columbia', 'Manitoba',
       'New Brunswick', 'Newfoundland and Labrador', 'Nova Scotia',
       'Ontario', 'Prince Edward Island', 'Quebec', 'Saskatchewan','Northwest Territories', 'Yukon']



def pull_JHU_data(link_dict=JHU_LINKS,kind="cases",province_list=PROVINCES,keep_LatLong=False,transpose=True):
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
    transpose : boolean
        Whether to transpose the data set (so the dates are rows). Default is true
    
    
    Returns
    -------
    df: pandas DataFrame 
        DataFrame with the Johns Hopkins data for Canada
    """

    df= pd.read_csv(JHU_LOCAL_LINKS[kind])
    df = df[df["Country/Region"]=="Canada"]
    df = df[df['Province/State'].isin( province_list)].set_index("Province/State")
    df.drop("Country/Region",axis=1,inplace=True)
    if keep_LatLong is False:
        df.drop(["Lat","Long"],axis=1,inplace=True)
        df.columns = pd.to_datetime(df.columns)
    if transpose:
        df = df.T
    return df



def pull_UofT_data(kind="cases",drop_repatriated=True):
    """
    Pull the data from the University of Toronto project

    Parameters
    ----------
    
    kind : string
        "cases", "deaths", "recovered" or "testing. The default is "cases" 
        
    drop_repatriated :
        The data contains a few values where Province is Repatriated. If drop_repatriated is True (default), these are deleted.

    Returns
    -------
    data : pandas DataFrame
        DataFrame with the UofT data

    """
    data = pd.read_csv(UOFT_LOCAL_LINKS[kind],index_col=0)
    date_columns = ["date_report","report_week","date_death_report","date_recovered","date_testing"]
    for col in data.columns:
        if col in date_columns:
            data[col] = pd.to_datetime(data[col],dayfirst=True)
    province_d = {"BC":"British Columbia","NL":"Newfoundland and Labrador",
                  "NWT":"Northwest Territories", "PEI":"Prince Edward Island"
                  }      
    data["province"].replace(province_d,inplace=True)
    if drop_repatriated is True:
        data = data[data.province != "Repatriated"]
    return data


def pull_GC (url = GC_LOCAL_LINK):
    data = pd.read_csv(url)
    data.date = pd.to_datetime(data.date,dayfirst=True)
    return data



def aggregate_UofT(df,by="province"):
    """
    Takes data in the UofT format and aggregates it to have cases per day.

    Parameters
    ----------
    df : pandas DataFrame
        The DataFrame to be aggregated
    by : string
        by what unit to aggregate. Can be "health_region" or "province"

    Returns
    -------
    agg : 
        A data frame reporting new cases by province (column) and date (row)
    agg2 : 
        A data frame reporting cumulative cases by province (column) and date (row)
    """

    agg=pd.pivot_table(df,columns=by,index="date_report",values="provincial_case_id",aggfunc="count")    
    agg=agg.fillna(0)
    agg2=agg.cumsum()
    return agg,agg2
    


def update_data_locally():
    """
    pulls all the data from the online sources and saves them locally.

    Returns
    -------
    None.

    """
    d = {"cases":"Cases","deaths":"Mortality","recovered":"Recovered","testing":"Testing"}
    
    for kind, name in d.items():
        data = pd.read_excel(URL_UOFT, index_col=0, header=3,sheet_name = name)
        data.to_csv(UOFT_LOCAL_LINKS[kind])
        
    for kind, filename in JHU_LOCAL_LINKS.items():
        df = pd.read_csv(JHU_LINKS[kind])
        df.to_csv(filename)
    
    pd.read_csv(URL_GC).to_csv(GC_LOCAL_LINK)
        
        
    
if __name__=="__main__":
    update_data_locally()
    
## TODO
        
    
    