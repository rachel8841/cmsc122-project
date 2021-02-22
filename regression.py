import pandas as pd
import numpy as np
import datasets
import sklearn as sk
import statsmodels as stat
import matplotlib.pyplot as plt

def get_model(var_list,y_var):
    '''
    Outputs a linear regression model given specific variables of interest.

    Inputs:
        var_list: list of independent variables (named as strings), maximum of 3
        y_var: string with name of dependent variable
    '''
    df = create_dataframes(list(set(var_list+y_var)))
    X = df[[var in var_list if var != y_var]]
    Y = df[[y_var]]

    X = stat.add_constant(X)
    model = stat.OLS(Y,X).fit()

    return model.summary()