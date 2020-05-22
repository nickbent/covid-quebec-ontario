import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

from ..plot.plot_quebec import *
from ..plot.utils import per100k

import math
import json
import os

import numpy as np
import pandas as pd


QUEBEC_PATH = "data/quebec/Quebec_.csv"
QUEBEC_GEOJSON_PATH = "data/quebec/quebec.geojson"
MONTREAL_GEOJSON = "data/quebec/montreal.geojson"
CIUSS_GEOJSON = "data/quebec/montreal_ciuss.geojson"

POPULATION = [197385, 276368, 729997, 266112, 319004, 1942044, 382604, 146717, 92518, 44561, 90311, 420082, 422993, 494796, 589400, 1507070, 242399]

DENSITY = [8.9, 2.8, 38.8, 7.4, 31.2, 3889.8, 12.4, 2.5, 0.4, 0.1, 4.4, 27.9, 1710.9, 39.8, 28.4, 135.4, 35.0]
ICU_CAP = 1000
HEADERS= ["Region",  "Total Number of Cases", "Date of Infection"]

def stack_dataframe(regions, dates):
    stacked_df = pd.DataFrame(columns=HEADERS)
    for ix,row in regions.iterrows():
        region = [list(row)[0]]*(len(row)-1)
        num_cases = list(row)[1:]
        region_list = [region, num_cases, dates]
        temp = pd.DataFrame(list(map(list, zip(*region_list))), columns = HEADERS)
        stacked_df =stacked_df.append(temp,  ignore_index=True)

    return stacked_df

def create_lastday_df(stacked_df, dates):

    lastday_df = stacked_df.loc[stacked_df['Date of Infection'] == dates[-1]][:17]
    lastday_df = lastday_df.rename(columns = {"Region":"res_nm_reg"})
    total_cases = list(lastday_df["Total Number of Cases"])
    cases_per_density = [ total/d for total, d in zip(total_cases, DENSITY)]
    cases_per_population = per100k(total_cases, POPULATION)
    lastday_df["Cases per Density"] = cases_per_density
    lastday_df["Cases per 100k"] = cases_per_population

    return lastday_df

def get_data(name):
    path = 'data/quebec/'+ [  path for path in os.listdir("data") if name in path][0]
    with open(path, 'r') as infile:
        data= json.load( infile)
    return data

def main():

    df = pd.read_csv(QUEBEC_PATH)
    regions_df = df[:19]
    dates = list(regions_df)[1:]

    with open(QUEBEC_GEOJSON_PATH,"r") as infile:
        quebec = json.load(infile)
    
    with open(MONTREAL_GEOJSON ,"r") as infile:
        montreal_nhood_geojson = json.load(infile)

    # with open(CIUSS_GEOJSON,"r") as infile:
    #     ciuss_geojson = json.load(infile)

    stacked_df = stack_dataframe(regions_df, dates)
    lastday_df = create_lastday_df(stacked_df, dates)

    montreal_nhood = get_data('montreal_nhood2020')    
    age_deaths = get_data('age_death2020')
    age_cases = get_data('age_cases2020')
    
    plot_total_cases(stacked_df, df, dates)
    plot_region_cases(stacked_df,  dates)
    plot_hospitilazation(df,dates)
    plot_total_cases(df, dates)
    plot_breakdown(df, dates)
    plot_map_per100k(lastday_df, quebec)
    plot_exponential(df, stacked_df)
    plot_montreal_nhood(montreal_nhood, montreal_nhood_geojson)
    plot_age(age_deaths, age_cases)





