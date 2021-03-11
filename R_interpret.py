import pandas as pd
import numpy as np
import dataframes
import R_regression

def make_x_var_list(reg_results,x_var,y_var,control=None,year=None): #countries=codes
    '''
    Takes the reg_results dictionary returned when a linear regression is run 
    and outputs a string interpreting various attributes of the regression
    '''
    output = ''
    model_type = reg_results["Model Spec"] # base, quad, log
    SE_type = reg_results["SE Type"] # normal, robust
    r2 = reg_results["Adj. R-squared"]
    intercept = reg_results["Intercept"]
    x_coeff = reg_results[x_var]

    control_on = False
    if 'control' in reg_results:
        control_on = True
        control_dict = reg_results['control']
    
    
        
    