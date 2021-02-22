import pandas as pd
import numpy as np
import datasets
import statsmodels.api as stat
import statsmodels.formula.api as stat_f

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

    # not being used yet since we aren't doing t-tests
    het_test = stat.stats.api.het_breuschpagan(model.resid,model.model.exog)
    het = het_test[1] < 0.05

    return model