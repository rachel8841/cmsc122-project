def clean_column_name(variable):
    '''
    This cleans the column name for the variable description
    We want to keep the string in parentheses if it tells us something
        about the units, for example "Age dependency ratio (% of working-age population)"
        but we want to discard the string in parentheses if it relates to 
        the data source, for example "Public expenditure on health %GDP (OWID extrapolated series)"
    '''
    inside = variable[variable.find("(")+1:variable.find(")")]
    if "%" in inside or "per" in inside:
        return variable
    else:
        return variable[0: variable.find("(")]