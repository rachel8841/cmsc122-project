import pandas as pd
import numpy as np
import dataframes
import R_regression

def make_x_var_list(reg_results,x_var,y_var,control=None,year=None): #countries=codes
    '''
    Takes the reg_results dictionary returned when a linear regression is run 
    and outputs a string interpreting various attributes of the regression
    '''
    model_type = reg_results["Model Spec"] # base, quad, or log
    SE_type = reg_results["SE Type"] # normal, robust
    r2 = reg_results["Adj. R-squared"]
    intercept = reg_results["Intercept"]
    x_coeff = reg_results[x_var]

    control_on = False
    if 'control' in reg_results:
        control_on = True
        control_dict = reg_results['control']
    
    # sentence for introducing
    #{For the given year {},} 
    #{For the given countries {},}
    intro = 'The best fitting model for the relationship between {y} versus \
      {x}'.format(y=y_var, x=x_var)
    if control_on: 
        intro += ', with the controlled variable {ctrl},'.format(ctrl=control)
    intro += ' is {mod}, chosen from either a linear, quadratic, or \
      logarithmic model.'.format(mod=model_type)
    
    # sentence for r2
    r2_text = 'The model has an adjusted R-squared value of {r2}. The adjusted \
     R-squared value is a measure of relative predictive power, adjusted for \
     the number of variables used. '
    if model_type == 'base':
        r2_text += 'Here, it means that {r}% of the variation in {y} can be \
          explained by the variation in {x}'.format(r=r2, y=y_var, x=x_var)
    elif model_type == 'log':
        r2_text += 'Here, it means that {r}% of the variation in {y} can be \
          explained by the variation in the logarithm of {x}'.format(r=r2, \
          y=y_var, x=x_var)
    elif model_type == 'quad':
        r2_text += 'Here, it means that {r}% of the variation in {y} can be \
          explained by the variation in the square of {x}'.format(r=r2, \
          y=y_var, x=x_var)
    if control_on:
        r2_text += ' and {ctrl}'.format(ctrl=control)
    r2_text += '.'
    
    # sentence for estimations
    est_text = 'The model gives estimates of the intercepts and coefficients, \
      as well as their standard errors and p-values, from which we \
      can calculate confidence intervals.'
    if SE_type == 'robust':
        est_text += ' The standard errors here are robust to account for \
          heteroscedasticity, so they are larger than normal standard errors. \
          Under these conditions, our current method of regression is not the \
          most precise, and we inflate our standard errors to account for that.'

    # sentence for intercept
    int_intro = 'The y-intercept {yint} is the expected value of {y} when {x} \
      is zero'.format(yint=intercept['Estimate'], y=y_var, x=x_var)
    if control_on:
        int_intro += 'and {ctrl} is zero'.format(ctrl=control)
    int_intro += '.'
    
    # sentence for intercept's confidence interval
    int_ci = (intercept['Estimate'] - 1.66 * intercept['SE'], \
      intercept['Estimate'] + 1.66 * intercept['SE'])
    int_ci_text = ' Based on the standard error, we are 90% confident that the \
      true value of the intercept lies between ' + str(int_ci[0]) + ' and ' + \
      str(int_ci[1]) + '.'
    if 0 > int_ci[0] and 0 < int_ci[1]:
        int_ci_text += ' Since zero lies in this interval, there is no \
          statistical evidence that the y-intercept is nonzero.'
    
    # sentence for coeff
    
    # sentence for coeff's confidence interval
    
    output = intro + '\n' + r2_text + '\n' + est_text + '\n' + int_intro + \
      int_ci_text + '\n' + coeff_text + coeff_ci_text
    
    return output
