import pandas as pd
from functools import reduce

def create_dataframes(variable_list, countries):
    '''
    variable_list (list): list of strings
    options for variables are: "broadband-subscriptions", "child-mortality", "co2", "dalys",
    "dependency", "drug-deaths", "expected-schooling", "female-labor", "fertility", "gov-expenditure",
    "happiness", "homicides", "life-expectancy", "pollution-deaths", "savings"]
    variable_list has a maximum of three variables
    '''
    df_list = []
    for var in variable_list:
        csv_name = "data/" + var + ".csv"
        df_list.append(pd.read_csv(csv_name))

    merged = reduce(lambda left, right: pd.merge(left,right,on=['Code','Year', 'Entity']), df_list)
    merged = merged[merged["Code"].isin(countries)]

    return merged

def read_covid_data(variable_list):
    '''
    possible variables: new_cases_per_million, new_deaths_per_million, weekly_icu_patients_per_million, new_tests_per_thousand, new_vaccinations_smoothed_per_million
    '''
    url = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv"
    df = pd.read_csv(url,index_col=0,parse_dates=[0])

    merged = df[variable_list]

    return merged





