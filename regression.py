import pandas as pd
import numpy as np
import dataframes
import statsmodels.api as stat
import statsmodels.formula.api as stat_f

import rpy2 # https://rpy2.github.io/doc/v2.9.x/html/introduction.html
from rpy2.robjects.packages import importr # not sure if this is necessary?
base = importr('base')
utils = importr('utils')

from rpy2.robjects import r, pandas2ri
pandas2ri.activate()

#import subprocess
codes = ['AFG', 'ALB', 'DZA', 'AND', 'AGO', 'AIA', 'ATG', 'ARG', 'ARM', 'ABW', 'AUS', 'AUT', 'AZE', 'BHS', 'BHR', 'BGD', 'BRB', 'BLR', 'BEL', 'BLZ', 'BEN', 'BTN', 'BOL', 'BIH', 'BWA', 'BRA', 'BRN', 'BGR', 'BFA', 'BDI', 'KHM', 'CMR', 'CAN', 'CPV', 'CAF', 'TCD', 'CHL', 'CHM', 'COL', 'COM', 'COG', 'COK', 'CRI', 'CIV', 'HRV', 'CUB', 'CUW', 'CYP', 'CZE', 'COD', 'DNK', 'DJI', 'DMA', 'DOM', 'ECU', 'EGY', 'SLV', 'GNQ', 'ERI', 'EST', 'SWZ', 'ETH', 'FJI', 'FIN', 'FRA', 'GUF', 'GAB', 'GMB', 'GEO', 'DEU', 'GHA', 'GRC', 'GRD', 'GUM', 'GTM', 'GIN', 'GNM', 'GUY', 'HTI', 'HND', 'HKG', 'HUN', 'ISL', 'IND', 'IDN', 'IRN', 'IRQ', 'IRL', 'ISR', 'ITA', 'JAM', 'JPN', 'JOR', 'KAZ', 'KEN', 'KIR', 'KWT', 'KGZ', 'LAO', 'LVA', 'LBN', 'LSO', 'LBR', 'LBY', 'LTU', 'LUX', 'MAC', 'MDG', 'MWI', 'MYS', 'MDV', 'MLI', 'MLT', 'MHL', 'MTQ', 'MRT', 'MUS', 'MYT', 'MEX', 'FSM', 'MDA', 'MCO', 'MNG', 'MNE', 'MAR', 'MOZ', 'MMR', 'NAM', 'NRU', 'NPL', 'NLD', 'NCL', 'NZL', 'NIC', 'NER', 'NGA', 'NIU', 'PRK', 'MKD', 'OMN', 'PAK', 'PLW', 'PSE', 'PAN', 'PNG', 'PRY', 'PER', 'PHL', 'POL', 'PRT', 'PRI', 'QAT', 'ROU', 'RUS', 'RWA', 'KNA', 'LCA', 'VCT', 'WSM', 'SMR', 'STP', 'SAU', 'SEN', 'SRB', 'SYC', 'SLE', 'SGP', 'SVK', 'SVN', 'SLB', 'SOM', 'ZAF', 'KOR', 'SSD', 'ESP', 'LKA', 'SDN', 'SUR', 'CHE', 'SYR', 'TJK', 'TZA', 'TJK', 'THA', 'TLS', 'TGO', 'TON', 'TTO', 'TUN', 'TUR', 'TKM', 'TUV', 'UGA', 'UKR', 'ARE', 'GBR', 'USA', 'UZB', 'VUT', 'VEN', 'VNM', 'YEM', 'ZMB', 'ZWE']


def use_r_code(x_var,y_var):
    '''
    Executes R code for running a linear regression (and other things) 
    using the rpy2 library
    '''
    # blah rpy2 code - use the existing df and do regression (what else?)
    # i feel like we should try to do some fancier stuff than just regression
    # so that we can justify using rpy2 and being Ambitious
    
    # use this to convert relevant df so it's usable in R (need df as variable?)
    r_df = pandas2ri.py2ri(df)
    
    # see documentation for other ways to do R code here but could just do
    regression = robjects.r('''
        # write R code for doing a regression here (in a string)
        # call the code, it will be output to regression
        ''')
        
    return regression
    
    
def get_model(x_var,y_var):
    '''
    Outputs a linear regression model given specific variables of interest.

    Inputs:
        var_list: list of independent variables (named as strings), maximum of 3
        y_var: string with name of dependent variable
    '''
    var_list = [x_var, y_var]
    df = dataframes.create_dataframes(var_list, codes)
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
    

def compute_r(x_var,y_var):
    '''
    Does some kind of R code using the subprocess library 
    (https://docs.python.org/3/library/subprocess.html) and writes the results
    back to python
    '''
    # see https://www.kdnuggets.com/2015/10/integrating-python-r-executing-part2.html?fbclid=IwAR3IL1c51hFzVLWKI_i-Bd0UohaOnUym1guYGxjkKl0zR66nUDDy90xB2vo
    var_list = [x_var, y_var]
    
    # blah blah R code - need to actually write an R script
    command ='Rscript'
    path2script ='path/to your script/script.R'
    
    # check_output will run the command and store to result
    # write the r script so that result will be a bunch of text that tells us
    # things we want (regression values, etc)
    cmd = [command, path2script] + var_list
    #result = subprocess.check_output(cmd, universal_newlines=True)
    result = subprocess.run(cmd, capture_output=True)
    
    return result