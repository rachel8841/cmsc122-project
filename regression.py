import pandas as pd
import numpy as np
import dataframes
import statsmodels.api as stat
import statsmodels.formula.api as stat_f

def get_model(x_var,y_var):
    '''
    Outputs a linear regression model given specific variables of interest.

    Inputs:
        var_list: list of independent variables (named as strings), maximum of 3
        y_var: string with name of dependent variable
    '''
    var_list = [x_var, y_var]
    df = dataframes.create_dataframes(var_list)
    header = ["Entity", "Code", "Year"]
    header.append(x_var)
    header.append(y_var)
    df.columns = header
    X = df[[x_var]]
    Y = df[[y_var]]

    X = stat.add_constant(X)
    model = stat.OLS(Y,X).fit()

    # not being used yet since we aren't doing t-tests
    #het_test = stat.stats.api.het_breuschpagan(model.resid,model.model.exog)
    #het = het_test[1] < 0.05

    return model