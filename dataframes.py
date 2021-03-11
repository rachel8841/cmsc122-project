import pandas as pd
from functools import reduce

'''
This file deals with cleaning and creating elements of dataframes.
Citations:
    https://stackoverflow.com/questions/44327999/python-pandas-merge-multiple-dataframes
    for how to merge multiple dataframes
'''

def create_dataframes(variable_list, countries):
    '''
    Creates a merged dataframe for the variables and countries of interest
    Inputs:
        variable_list (list): list of strings
        countries (list): list of country codes
    Ouputs:
        merged (dataframe)
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
        about the units, for example 
        "Age dependency ratio (% of working-age population)"
        but we want to discard the string in parentheses if it relates to 
        the data source, for example 
        "Public expenditure on health %GDP (OWID extrapolated series)"
    Input:
        variable (str): column name for the variable of interest
    Ouput:
        cleaned column name
    '''

    inside = variable[variable.find("(")+1:variable.find(")")]
    if "%" in inside or "per" in inside:
        return variable
    else:
        return variable[0: variable.find("(")]