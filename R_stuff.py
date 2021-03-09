import pandas as pd
import numpy as np
import dataframes

import rpy2 # https://rpy2.github.io/doc/v2.9.x/html/introduction.html
import rpy2.robjects as robjects
from rpy2.robjects import r, pandas2ri
from rpy2.robjects.conversion import localconverter
import rpy2.robjects.packages as rpackages

base = rpackages.importr('base')
utils = rpackages.importr('utils')
utils.chooseCRANmirror(ind=1)
utils.install_packages('lmtest')
rpackages.importr('lmtest')
utils.install_packages('RCurl')
rpackages.importr('RCurl')
pandas2ri.activate()

# list of country codes
codes = ['AFG', 'ALB', 'DZA', 'AND', 'AGO', 'AIA', 'ATG', 'ARG', 'ARM', 'ABW',
'AUS', 'AUT', 'AZE', 'BHS', 'BHR', 'BGD', 'BRB', 'BLR', 'BEL', 'BLZ', 'BEN',
'BTN', 'BOL', 'BIH', 'BWA', 'BRA', 'BRN', 'BGR', 'BFA', 'BDI', 'KHM', 'CMR',
'CAN', 'CPV', 'CAF', 'TCD', 'CHL', 'CHM', 'COL', 'COM', 'COG', 'COK', 'CRI',
'CIV', 'HRV', 'CUB', 'CUW', 'CYP', 'CZE', 'COD', 'DNK', 'DJI', 'DMA', 'DOM',
'ECU', 'EGY', 'SLV', 'GNQ', 'ERI', 'EST', 'SWZ', 'ETH', 'FJI', 'FIN', 'FRA',
'GUF', 'GAB', 'GMB', 'GEO', 'DEU', 'GHA', 'GRC', 'GRD', 'GUM', 'GTM', 'GIN',
'GNM', 'GUY', 'HTI', 'HND', 'HKG', 'HUN', 'ISL', 'IND', 'IDN', 'IRN', 'IRQ',
'IRL', 'ISR', 'ITA', 'JAM', 'JPN', 'JOR', 'KAZ', 'KEN', 'KIR', 'KWT', 'KGZ',
'LAO', 'LVA', 'LBN', 'LSO', 'LBR', 'LBY', 'LTU', 'LUX', 'MAC', 'MDG', 'MWI',
'MYS', 'MDV', 'MLI', 'MLT', 'MHL', 'MTQ', 'MRT', 'MUS', 'MYT', 'MEX', 'FSM',
'MDA', 'MCO', 'MNG', 'MNE', 'MAR', 'MOZ', 'MMR', 'NAM', 'NRU', 'NPL', 'NLD',
'NCL', 'NZL', 'NIC', 'NER', 'NGA', 'NIU', 'PRK', 'MKD', 'OMN', 'PAK', 'PLW',
'PSE', 'PAN', 'PNG', 'PRY', 'PER', 'PHL', 'POL', 'PRT', 'PRI', 'QAT', 'ROU',
'RUS', 'RWA', 'KNA', 'LCA', 'VCT', 'WSM', 'SMR', 'STP', 'SAU', 'SEN', 'SRB',
'SYC', 'SLE', 'SGP', 'SVK', 'SVN', 'SLB', 'SOM', 'ZAF', 'KOR', 'SSD', 'ESP',
'LKA', 'SDN', 'SUR', 'CHE', 'SYR', 'TJK', 'TZA', 'TJK', 'THA', 'TLS', 'TGO',
'TON', 'TTO', 'TUN', 'TUR', 'TKM', 'TUV', 'UGA', 'UKR', 'ARE', 'GBR', 'USA',
'UZB', 'VUT', 'VEN', 'VNM', 'YEM', 'ZMB', 'ZWE']

# add summary() function with robust SEs to R session from
# economictheoryblog.com/2016/08/07/robust-standard-errors-in-r-function/
robjects.r('''
url_robust = "https://raw.githubusercontent.com/IsidoreBeautrelet/economictheoryblog/master/robust_summary.R"
eval(parse(text=getURL(url_robust,ssl.verifypeer=FALSE)),envir=.GlobalEnv)
''')

def make_x_var_list(x_var,control=None):
    '''
    Makes a list of explanatory variables being used.
    '''
    var_list = []
    var_list.append(x_var)
    if control is not None:
        var_list.append(control)

    return var_list


def make_dataframe(x_var,y_var,control=None):
    '''
    Loads csvs and creates a dataframe with the specified variables to later
    use in R. No more than 2 x_vars.

    Inputs:
        x_vars: string of name of main explanatory variable of interest
        y_var: string of name of dependent variable
        control: string of name of variable to control for (None by default)

    Output: a pandas df
    '''
    x_var_list = make_x_var_list(x_var,control)
    df = dataframes.create_dataframes(x_var_list+[y_var],codes)

    header = ["Entity", "Code", "Year"]
    header += x_var_list + [y_var]
    df.columns = header

    return df


def regression_in_R(x_var,y_var,control=None):
    '''
    Uses the rpy2 package to perform data analysis in R using specified X and
    Y variables.

    Inputs:
        x_var: the main explanatory variable of interest, as a string
        y_var: the dependent variable, as a string
        control: a covariate to control for, as a string

    Output: regression results from R as a string 
    '''
    data = make_dataframe(x_var,y_var,control)

    with localconverter(robjects.default_converter+pandas2ri.converter):
        r_df = robjects.conversion.py2rpy(data)
    robjects.globalenv['py_df'] = r_df
    
    r_call = '''
    do_reg = function(df,control=F){
        if (control){
            model = lm(df[,3] ~ df[,1] + df[,2])
        } else{
            model = lm(df[,2] ~ df[,1])
        }
        test = bptest(model)
        p_val = unname(test$p.value)
        if (p_val > 0.10){
            return(summary(model))
        } else{
            return(summary(model,robust=T))
        }
    }
    sum = do_reg(py_df,(ncol(py_df)>2))
    as.character(sum$coefficients)
    '''
    output = list(robjects.r(r_call))

    reg_results = {}
    reg_results["Intercept"] = {}
    reg_results[x_var] = {}
    if control is None:
        reg_results["Intercept"]["Estimate"] = output[0]
        reg_results[x_var]["Estimate"] = output[1]
        reg_results["Intercept"]["SE"] = output[2]
        reg_results[x_var]["SE"] = output[3]
        reg_results["Intercept"]["t-value"] = output[4]
        reg_results[x_var]["t-value"] = output[5]
        reg_results["Intercept"]["p-value"] = output[6]
        reg_results[x_var]["p-value"] = output[7]
    else:
        reg_results[control] = {}
        reg_results["Intercept"]["Estimate"] = output[0]
        reg_results[x_var]["Estimate"] = output[1]
        reg_results[control]["Estimate"] = output[2]
        reg_results["Intercept"]["SE"] = output[3]
        reg_results[x_var]["SE"] = output[4]
        reg_results[control]["SE"] = output[5]
        reg_results["Intercept"]["t-value"] = output[6]
        reg_results[x_var]["t-value"] = output[7]
        reg_results[control]["t-value"] = output[8]
        reg_results["Intercept"]["p-value"] = output[9]
        reg_results[x_var]["p-value"] = output[10]
        reg_results[control]["p-value"] = output[11]

    return reg_results