## Files
* visualization.py
* R_regression.py
* R_interpret.py
* dataframes.py
* line.py
* webscraping.py
    
## How to run

    Simply load visualization.py into ipython3 and run visualization.setup() to launch the Dash web application that houses the interactive data visualization.
    Once the application is launched, there are three dropdowns: the first selects the x variable, the second selects the y variable, and the third selects the variable that will be represented by the size of the bubble markers on the plot. 
    Additionally, there are two checkboxes: the first is to include the third variable as a control in the regression analysis, and the second checkbox is to superimpose a curve of best fit on top of the data visualization.
    Below the interactive menu are a couple of read outs: one describes each of the variables with information pulled from ourworldindata.org and the second is a statistical summary generated in R. 