import plotly.graph_objects as go
import numpy as np


def create_function(x_range, var_list=[], regression_results={}):
    '''
    '''

    x = np.linspace(x_range[0], x_range[1], 100)

    '''
    func_type = regression_results['Model Spec']
    a = regression_results['Intercept']['Estimate']
    b = regression_results[var_list[0]]['Estimate']
    if func_type == 'quad':
        c = regression_results['Square']['Estimate']
    else:
        c = 0
    '''
    func_type = 'log'
    a = 1
    b = 2
    c = 3

    func_dict = {'base': a+b*x, 'quad': a+b*x+c*(x**2), 'log': a+b*np.log(x)}
    y = func_dict[func_type]

    return go.Scatter(x=x, y=y,
                     mode="lines",
                     line=dict(width=2, color="blue"))