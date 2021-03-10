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


def regression_in_R(x_var,y_var,control=None,year=None):
    '''
    Uses the rpy2 package to perform data analysis in R using specified X and
    Y variables.

    Inputs:
        x_var: the main explanatory variable of interest, as a string
        y_var: the dependent variable, as a string
        control: a covariate to control for, as a string
        year: (str) year of data that we're interesting in, None by default

    Output: dictionary of 'Intercept', x_var, and control, each mapping to a
    dictionary of 'Estimate', 'SEs', 't-value', and 'p-value' (ints) 
    '''
    data = make_dataframe(x_var,y_var,control)
    if year is not None:
        data = data[data["Year"]==year]

    with localconverter(robjects.default_converter+pandas2ri.converter):
        r_df = robjects.conversion.py2rpy(data)
        robjects.globalenv['py_df'] = r_df
            
    
    r_call = '''
    do_reg = function(df,control=F){
        df$log = log(df[,4])
        if (control){
            base_model = lm(df[,6] ~ df[,4] + df[,5])
            quad_model = lm(df[,6] ~ df[,4] + df[,4]^2 + df[,5])
            log_model = lm(df[,6] ~ df$log + df[,5])
        } else{
            base_model = lm(df[,5] ~ df[,4])
            quad_model = lm(df[,5] ~ df[,4] + df[,4]^2)
            log_model = lm(df[,5] ~ df$log)
        }
        if (summary(base_model)$adj.r.squared >= summary(quad_model)$adj.r.squared){
            if (summary(base_model)$adj.r.squared >= summary(log_model)$adj.r.squared){
                model = base_model
                type = "base"
            } else{
                model = log_model
                type = "log"
            }
        } else if (summary(quad_model)$adj.r.squared >= summary(log_model)$adj.r.squared){
            model = quad_model
            type = "quad"
        } else{
            model = log_model
            type = "log"
        }
        test = bptest(model)
        p_val = unname(test$p.value)
        if (p_val > 0.1){
            SE = "normal"
            l0 = list(as.character(summary(model)$coefficients),type,SE)
            return(l0)
        } else{
            SE = "robust"
            l0 = list(as.character(summary(model,robust=T)$coefficients),type,SE)
            return(l0)
        }
    }
    do_reg(py_df,(ncol(py_df)==6))
    '''
    
    output = list(robjects.r(r_call))
    values = [float(x) for x in output[0]]

    reg_results = {}
    reg_results["Model Spec"] = str(output[1]).split("\"")[1]
    reg_results["SE Type"] = str(output[2]).split("\"")[1]
    reg_results["Intercept"] = {}
    reg_results[x_var] = {}
    if control is None and output[1]!="quad":
        reg_results["Intercept"]["Estimate"] = values[0]
        reg_results[x_var]["Estimate"] = values[1]
        reg_results["Intercept"]["SE"] = values[2]
        reg_results[x_var]["SE"] = values[3]
        reg_results["Intercept"]["t-value"] = values[4]
        reg_results[x_var]["t-value"] = values[5]
        reg_results["Intercept"]["p-value"] = values[6]
        reg_results[x_var]["p-value"] = values[7]
    elif output[1]!="quad":
        reg_results[control] = {}
        reg_results["Intercept"]["Estimate"] = values[0]
        reg_results[x_var]["Estimate"] = values[1]
        reg_results[control]["Estimate"] = values[2]
        reg_results["Intercept"]["SE"] = values[3]
        reg_results[x_var]["SE"] = values[4]
        reg_results[control]["SE"] = values[5]
        reg_results["Intercept"]["t-value"] = values[6]
        reg_results[x_var]["t-value"] = values[7]
        reg_results[control]["t-value"] = values[8]
        reg_results["Intercept"]["p-value"] = values[9]
        reg_results[x_var]["p-value"] = values[10]
        reg_results[control]["p-value"] = values[11]
    elif control is None:
        reg_results["Square"] = {}
        reg_results["Intercept"]["Estimate"] = values[0]
        reg_results[x_var]["Estimate"] = values[1]
        reg_results["Square"]["Estimate"] = values[2]
        reg_results["Intercept"]["SE"] = values[3]
        reg_results[x_var]["SE"] = values[4]
        reg_results["Square"]["SE"] = values[5]
        reg_results["Intercept"]["t-value"] = values[6]
        reg_results[x_var]["t-value"] = values[7]
        reg_results["Square"]["t-value"] = values[8]
        reg_results["Intercept"]["p-value"] = values[9]
        reg_results[x_var]["p-value"] = values[10]
        reg_results["Square"]["p-value"] = values[11]
    else:
        reg_results[control] = {}
        reg_results["Square"] = {}
        reg_results["Intercept"]["Estimate"] = values[0]
        reg_results[x_var]["Estimate"] = values[1]
        reg_results["Square"]["Estimate"] = values[2]
        reg_results[control]["Estimate"] = values[3]
        reg_results["Intercept"]["SE"] = values[4]
        reg_results[x_var]["SE"] = values[5]
        reg_results["Square"]["SE"] = values[6]
        reg_results[control]["SE"] = values[7]
        reg_results["Intercept"]["t-value"] = values[8]
        reg_results[x_var]["t-value"] = values[9]
        reg_results["Square"]["t-value"] = values[10]
        reg_results[control]["t-value"] = values[11]
        reg_results["Intercept"]["p-value"] = values[12]
        reg_results[x_var]["p-value"] = values[13]
        reg_results["Square"]["p-value"] = values[14]
        reg_results[control]["p-value"] = values[15]

    return reg_results