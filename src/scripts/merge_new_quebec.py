import pandas as pd
import json
import os
import datetime
import argparse

QUEBEC_PATH = "data/quebec/Quebec_.csv"
DATA_PATH = "data/quebec/"

MAP_CASES = {2:21, 6 :28, 7 : 29}


def string_to_float(string):
    return float(string.replace(" ", ""))

def add_cases(today, yesterday, cases_path):
    with open(cases_path, 'r') as outfile:
        cases = outfile.read()
    
    for ix, case in enumerate(cases.split("\n")):
        if ix in MAP_CASES:
            today[MAP_CASES[ix]] = string_to_float(case.split(":")[-1])
    today[22] = today[21] -yesterday[21]
    today[23] = string_to_float(cases.split("\n")[1].split(":")[-1])- string_to_float(cases.split("\n")[0].split(":")[-1])

def add_cases_region(today, yesterday, cases_region_path):
    with open(cases_region_path, 'r') as outfile:
        cases_region = json.load( outfile)
    values = list(cases_region.values())

    for ix, num_cases in enumerate(values[:16]):
        today[ix] = string_to_float(num_cases)
    today[16] = string_to_float(values[16])+string_to_float(values[17])
    today[17] = string_to_float(values[18])
    today[18] = string_to_float(values[19])
    today[19] = string_to_float(values[20])
    today[20] = today[19] - yesterday[19]

def add_deaths_region(today, yesterday, deaths_region_path):
    with open(deaths_region_path, 'r') as outfile:
        deaths = json.load( outfile)
    today[24] = string_to_float(deaths['Total'])


def main(date):

    df = pd.read_csv(QUEBEC_PATH)
    yesterday = list(df[list(df)[-1]])
    today = [0]*30

    data_files = os.listdir(DATA_PATH)

    cases_path = 'data/quebec/'+[d for d in data_files if "cases_total" in d][0]
    cases_region_path = 'data/quebec/'+[d for d in data_files if "cases_region" in d][0]
    deaths_region = 'data/quebec/'+[d for d in data_files if "deaths_region" in d][0]
    
    add_cases(today, yesterday, cases_path)
    add_cases_region(today,yesterday, cases_region_path)
    add_deaths_region(today, yesterday, deaths_region)

    today[26] = yesterday[26]+.11
    today[25] = 17336				
    today[27] = yesterday[27] +1

    df[date] = today
    df.to_csv(QUEBEC_PATH, index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "date", type=str, help="Todays date in Month Day i.e. May 21st"
    )

    main(**vars(parser.parse_args()))
