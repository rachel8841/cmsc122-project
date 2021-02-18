import pandas as pd
from functools import reduce

def create_dataframes(variable_list):
    '''
    variable_list (list): list of strings
    options for variables are: "broadband-subscriptions", "child-mortality", "co2", "dalys",
    "dependency", "drug-deaths", "expected-schooling", "female-labor", "fertility", "gov-expenditure",
    "happiness", "homicides", "life-expectancy", "pollution-deaths", "savings"]
    variable_list has a maximum of three variables
    '''
    df_list = []
    for var in variable_list:
        csv_name = var + ".csv"
        df_list.append(pd.read_csv(csv_name))

    merged = reduce(lambda left, right: pd.merge(left,right,on=['Code','Year', 'Entity']), df_list)

    return merged


