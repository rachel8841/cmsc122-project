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


def clean_column_name(variable):
    '''
    This cleans the column name for the variable description
    We want to keep the string in parentheses if it tells us something
        about the units, for example "Age dependency ratio (% of working-age population)"
        but we want to discard the string in parentheses if it relates to 
        the data source, for example "Public expenditure on health %GDP (OWID extrapolated series)"
    '''

    inside = variable[variable.find("(")+1:variable.find(")")]
    if "%" in inside or "per" in inside:
        return variable
    else:
        return variable[0: variable.find("(")]



