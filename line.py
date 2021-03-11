import plotly.graph_objects as go
import numpy as np

def create_function(x_range, var_list=[], regression_results={}):
    '''
    This function takes in information from the regression analysis in R and
        returns a plotly Scatter object for the curve of best fit.
    Inputs:
        x_range (list): a list that contains integers [xmin, xmax]
        var_list (list): string list of variables of interest
        regression_results (dict): dictionary from R_regression.regression_in_R
    Ouput:
        plotly Scatter object
    '''

    x = np.linspace(x_range[0], x_range[1], 100)

    
    func_type = regression_results['Model Spec']
    a = regression_results['Intercept']['Estimate']
    b = regression_results[var_list[0]]['Estimate']
    if func_type == 'quad':
        c = regression_results['Square']['Estimate']
    else:
        c = 0
    
    func_dict = {'base': a+b*x, 'quad': a+b*x+c*(x**2), 'log': a+b*np.log(x)}
    y = func_dict[func_type]
    
    return go.Scatter(x=x, y=y,
                     mode="lines",
                     line=dict(width=2, color="black"),
                     name="Regression Line")
    