import pandas as pd
import numpy as np
import dataframes
import R_regression

def write_interpretation(reg_results,x_var,y_var,control=None,year=None): #countries=codes
    '''
    Takes the reg_results dictionary returned when a linear regression is run 
    and outputs a string interpreting various attributes of the regression
    '''
    model_type = reg_results["Model Spec"] # base, quad, or log
    if model_type == 'base':
        model_type == 'linear'
    elif model_type == 'log':
        model_type == 'logarithmic'
    else:
        model_type == 'quadratic'
    SE_type = reg_results["SE Type"] # normal, robust
    r2 = reg_results["Adj. R-squared"]
    intercept = reg_results["Intercept"]
    x_coeff = reg_results[x_var]

    control_on = False
    if 'control' in reg_results:
        control_on = True
        control_dict = reg_results['control']
    
    # sentence for introducing model
    #{For the given year {},} 
    #{For the given countries {},}
    intro = '''The best fitting model for the relationship between {y} versus
    {x}'''.format(y=y_var, x=x_var)
    if control_on: 
        intro += ', with the controlled variable {ctrl},'.format(ctrl=control)
    intro += ''' is a {mod} model, chosen from either a linear, quadratic, or 
    logarithmic model.'''.format(mod=model_type)
    
    # sentence for r2
    r2_text = '''The model has an adjusted R-squared value of {r:.4f}. The
    adjusted R-squared value is a measure of relative predictive power, 
    adjusted for the number of variables used. '''.format(r=r2)
    r2_per = 10 * r2
    if model_type == 'base':
        r2_text += '''Here, it means that {r:.2f}% of the variation in {y} can 
        be explained by the variation in {x}'''.format(r=r2_per,y=y_var,x=x_var)
    elif model_type == 'log':
        r2_text += '''Here, it means that {r:.2f}% of the variation in {y} can 
        be explained by the variation in the logarithm of {x}
        '''.format(r=r2_per, y=y_var, x=x_var)
    elif model_type == 'quad':
        r2_text += '''Here, it means that {r:.2f}% of the variation in {y} can 
        be explained by the variation in the square of {x}'''.format(r=r2_per,\
        y=y_var, x=x_var)
    if control_on:
        r2_text += ' and {ctrl}'.format(ctrl=control)
    r2_text += '.'
    
    # sentence for estimations
    est_text = '''The model gives estimates of the intercepts and coefficients, 
    as well as their standard errors and p-values, from which we can calculate 
    confidence intervals.'''
    if SE_type == 'robust':
        est_text += ''' 
        The standard errors here are robust to account for 
        heteroscedasticity, so they are larger than normal standard errors. 
        Under these conditions, our current method of regression is not the 
        most precise, and we inflate our standard errors to account for that.'''

    # sentence for intercept
    int_intro = '''The y-intercept {yint:.2f} is the expected value of {y} when 
    {x} is zero'''.format(yint=intercept['Estimate'], y=y_var, x=x_var)
    if control_on:
        int_intro += 'and {ctrl} is zero'.format(ctrl=control)
    int_intro += '.'
    
    # sentence for intercept's confidence interval
    int_ci = (intercept['Estimate'] - 1.66 * intercept['SE'], \
    intercept['Estimate'] + 1.66 * intercept['SE'])
    int_ci_text = ''' Based on the standard error, we are 90% confident that the
     true value of the intercept lies between ''' + '{:.2f}'.format(int_ci[0]) +
     ' and ' + '{:.2f}'.format(int_ci[1]) + '.'
    if 0 > int_ci[0] and 0 < int_ci[1]:
        int_ci_text += ''' Since zero lies in this interval, there is no 
        statistical evidence that the y-intercept is nonzero.'''
    
    # sentence for coeff (not quad)
    if model_type != 'quad':
        if model_type == 'base':
            coeff_text = '''The coefficient {c:.2f} represents the change in {y}
             for a one unit increase in {x}'''.format(c=x_coeff['Estimate'],\
            y=y_var, x=x_var)
        elif model_type == 'log':
            coeff_text = '''The coefficient {c:.2f} represents the change in {y}
             for a one percent increase in {x}'''.format(c=x_coeff['Estimate'],\
            y=y_var, x=x_var)
        if control_on:
            coeff_text += ', when {ctrl} is held constant'.format(ctrl=control)
        coeff_text += '.'
        
        # sentence for coeff's confidence interval
        coeff_ci = (x_coeff['Estimate'] - 1.66 * x_coeff['SE'], \
          x_coeff['Estimate'] + 1.66 * x_coeff['SE'])
        coeff_ci_text = ''' We are 90% confident that the true value of this 
        coefficient lies between ''' + '{:.2f}'.format(coeff_ci[0]) + ' and ' +\
        '{:.2f}'.format(coeff_ci[1]) + '.'
        if 0 > coeff_ci[0] and 0 < coeff_ci[1]:
            int_ci_text += ''' Since zero lies in this interval, there is no 
            statistical evidence that this coefficient is nonzero.'''
    
    # sentence for coeffs (quad)
    else:
        coeff_text = '''There are no simple interpretations of the two 
        coefficients estimated for a quadratic model, but the estimated 
        values here are ''' + '{:.2f}'.format(x_coeff['Estimate']) + \
        ' on the linear term and ' + \
        '{:.2f}'.format(reg_results["Square"]['Estimate']) + \
        ' on the quadratic term.'
          
        coeff_ci = (x_coeff['Estimate'] - 1.66 * x_coeff['SE'], \
          x_coeff['Estimate'] + 1.66 * x_coeff['SE'])
        coeff_ci_2 = (reg_results["Square"]['Estimate'] - 1.66 * \
          reg_results["Square"]['SE'], reg_results["Square"]['Estimate'] + \
          1.66 * reg_results["Square"]['SE'])
        coeff_ci_text = ''' We are 90% confident that the true value of the 
        linear coefficient lies between ''' + '{:.2f}'.format(coeff_ci[0]) + \
        ' and ' + '{:.2f}'.format(coeff_ci_1[0]) + ''', and that the true value 
        of the quadratic coefficient lies between ''' \
        + '{:.2f}'.format(coeff_ci_2[0]) + ' and ' + \
        '{:.2f}'.format(coeff_ci_2[0]) + '.'
        #if 0 > coeff_ci[0] and 0 < coeff_ci[1]:
        #    int_ci_text += ' Since zero lies in the first interval, there is\
        #    no statistical evidence that this coefficient is nonzero.'
    
    #output = intro + '\n' + r2_text + '\n' + est_text + '\n' + int_intro + \
    #  int_ci_text + '\n' + coeff_text + coeff_ci_text
    output = '\n'.join([intro, r2_text, est_text, int_intro, int_ci_text, \
      coeff_text, coeff_ci_text])
    
    return output
