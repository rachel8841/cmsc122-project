name_dict = {'fixed-broadband-subscriptions-per-100-people': 'Broadband Subscriptions',
    'child-mortality': 'Child Mortality',
    'annual-co2-emissions-per-country': 'CO2 Emissions',
    'dalys-rate-from-all-causes': 'Disability Adjusted Life Years',
    'age-dependency-ratio-of-working-age-population': 'Age Dependency Ratio',
    'deaths-from-alcohol-and-drug-use-disorders': 'Deaths from Drugs and Alcohol',
    'expected-years-of-schooling': 'Years of Expected Schooling',
    'oecd-female-labour-force-participation-rate-15-64': 'Female Labor Force Participation Rate',
    'total-gov-expenditure-gdp-wdi': 'Government Expenditure per Capita',
    'happiness-cantril-ladder': 'Happiness',
    'intentional-homicides-per-100000-people': 'Homicides',
    'adjusted-net-savings-per-person': 'Savings',
    'life-expectancy': 'Life Expectancy',
    'annual-working-hours-per-worker': 'Working Hours',
    'contraceptive-prevalence-any-methods-vs-modern-methods': 'Contraceptive Prevalence',
    'military-expenditure-as-share-of-gdp': 'Military Expenditure',
    'public-health-expenditure-share-gdp-owid': 'Public Health Expenditure',
    'average-real-gdp-per-capita-across-countries-and-regions': 'GDP per capita',
    'Share-of-the-population-with-access-to-electricity': 'Access to Electricity',
    'total-government-expenditure-on-education-gdp': 'Education Expenditure',
    'out-of-pocket-expenditure-per-capita-on-healthcare': 'Out of Pocket Healthcare Expenditure',
    'trade-as-share-of-gdp': 'Trade',
    'projected-population-by-country': 'Population'}

def write_interpretation(reg_results,xvar,yvar,control=None,year=None): #countries=codes
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
    x_coeff = reg_results[xvar]

    control_on = False
    if 'control' in reg_results:
        control_on = True
        control_dict = reg_results['control']
    
    intro = '''
    The best fitting model for the relationship between {y} versus\
    {x}'''.format(y=name_dict[yvar], x=name_dict[xvar])
    if control_on: 
        intro += ', with the controlled variable {ctrl},'.format(ctrl=name_dict[control])
    intro += ''' is a {mod} model, chosen from either a linear, quadratic, or \
    logarithmic model.'''.format(mod=model_type)
    
    # sentence for r2
    r2_text = '''\
    The model has an adjusted R-squared value of {r:.4f}. The\
    adjusted R-squared value is a measure of relative predictive power, \
    adjusted for the number of variables used. '''.format(r=r2)
    r2_per = 100 * r2
    if model_type == 'base':
        r2_text += '''Here, it means that {r:.2f}% of the variation in {y} can \
        be explained by the variation in {x}'''.format(r=r2_per,y=yvar,x=xvar)
    elif model_type == 'log':
        r2_text += '''Here, it means that {r:.2f}% of the variation in {y} can \
        be explained by the variation in the logarithm of {x}'''.\
        format(r=r2_per, y=name_dict[yvar], x=name_dict[xvar])
    elif model_type == 'quad':
        r2_text += '''Here, it means that {r:.2f}% of the variation in {y} can \
        be explained by the variation in the square of {x}'''.format(r=r2_per,\
        y=name_dict[yvar], x=name_dict[xvar])
    if control_on:
        r2_text += ' and {ctrl}'.format(ctrl=name_dict[control])
    r2_text += '.'
    
    # sentence for estimations
    est_text = ''' The model gives estimates of the intercepts and \
    coefficients, as well as their standard errors and p-values, from which \
    we can calculate confidence intervals.'''
    if SE_type == 'robust':
        est_text += ''' \
        The standard errors here are robust to account for \
        heteroskedasticity, so they are larger than normal standard errors. \
        Under these conditions, our current method of regression is not the \
        most precise, and we inflate our standard errors to account for it.'''

    # sentence for intercept
    int_intro = ''' The y-intercept {yint:.2f} is the expected value of {y} \
    when {x} is zero'''.format(yint=intercept['Estimate'], y=name_dict[yvar], x=name_dict[xvar])
    if control_on:
        int_intro += 'and {ctrl} is zero'.format(ctrl=name_dict[control])
    int_intro += '.'
    
    # sentence for intercept's confidence interval
    int_ci = (intercept['Estimate'] - 1.66 * intercept['SE'], \
    intercept['Estimate'] + 1.66 * intercept['SE'])
    int_ci_text = ''' Based on the standard error, we are 90% confident that \
    the true value of the intercept lies between ''' + \
    '{:.2f}'.format(int_ci[0]) + ' and ' + '{:.2f}'.format(int_ci[1]) + '.'
    if 0 > int_ci[0] and 0 < int_ci[1]:
        int_ci_text += ''' Since zero lies in this interval, there is no \
        statistical evidence that the y-intercept is nonzero.'''
    
    # sentence for coeff (not quad)
    if model_type != 'quad':
        if model_type == 'base':
            coeff_text = ''' The coefficient {c:.2f} represents the change in \
            {y} for a one unit increase in {x}'''.\
                format(c=x_coeff['Estimate'],y=name_dict[yvar], x=name_dict[xvar])
        elif model_type == 'log':
            coeff_text = ''' The coefficient {c:.2f} represents the change in \
            {y} for a one percent increase in {x}'''.\
                format(c=x_coeff['Estimate'],y=name_dict[yvar], x=name_dict[xvar])
        if control_on:
            coeff_text += ', when {ctrl} is held constant'.format(ctrl=name_dict[control])
        coeff_text += '.'
        
        # sentence for coeff's confidence interval
        coeff_ci = (x_coeff['Estimate'] - 1.66 * x_coeff['SE'], \
          x_coeff['Estimate'] + 1.66 * x_coeff['SE'])
        coeff_ci_text = ''' We are 90% confident that the true value of this \
        coefficient lies between ''' + '{:.2f}'.format(coeff_ci[0]) + \
        ' and ' + '{:.2f}'.format(coeff_ci[1]) + '.'
        if 0 > coeff_ci[0] and 0 < coeff_ci[1]:
            int_ci_text += ''' Since zero lies in this interval, there is no \
            statistical evidence that this coefficient is nonzero.'''
    
    # sentence for coeffs (quad)
    else:
        coeff_text = ''' There are no simple interpretations of the two \
        coefficients estimated for a quadratic model, but the estimated \
        values here are ''' + '{:.2f}'.format(x_coeff['Estimate']) + \
        ' on the linear term and ' + \
        '{:.2f}'.format(reg_results["Square"]['Estimate']) + \
        ' on the quadratic term.'
          
        coeff_ci = (x_coeff['Estimate'] - 1.66 * x_coeff['SE'], \
          x_coeff['Estimate'] + 1.66 * x_coeff['SE'])
        coeff_ci_2 = (reg_results["Square"]['Estimate'] - 1.66 * \
          reg_results["Square"]['SE'], reg_results["Square"]['Estimate'] + \
          1.66 * reg_results["Square"]['SE'])
        coeff_ci_text = ''' We are 90% confident that the true value of the \
        linear coefficient lies between ''' + '{:.2f}'.format(coeff_ci[0]) + \
        ' and ' + '{:.2f}'.format(coeff_ci[1]) + ''', and that the true \
        value of the quadratic coefficient lies between ''' \
        + '{:.2f}'.format(coeff_ci_2[0]) + ' and ' + \
        '{:.2f}'.format(coeff_ci_2[1]) + '.'
        #if 0 > coeff_ci[0] and 0 < coeff_ci[1]:
        #    int_ci_text += ' Since zero lies in the first interval, there is\
        #    no statistical evidence that this coefficient is nonzero.'
    
    #output = intro + '\n' + r2_text + '\n' + est_text + '\n' + int_intro + \
    #  int_ci_text + '\n' + coeff_text + coeff_ci_text
    output = intro + r2_text + est_text + int_intro + \
      int_ci_text + coeff_text + coeff_ci_text
    #output = ''.join([intro, r2_text, est_text, int_intro, int_ci_text,
    #  coeff_text, coeff_ci_text])
    
    return output
