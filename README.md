## Files
* visualization.py
* R_regression.py
* R_interpret.py
* dataframes.py
* line.py
* webscraping.py

## Project Description
We wanted to create an interactive web application for users to explore trends in international development over time and over one hundred countries. 
Our application allows the user to select any combination of three development indicators from over twenty variables using data collected by the World Bank and other sources.
We were able to create an interative simulation that allows users to observe countries' development paths over time and to observe the broader trends between various indicators, for example, the relationship between public health expenditure, child mortality, and GDP per capita.
Additionally, users have the option to show a line of best fit on top of the graph. Our code performs statistical analysis in R and chooses from a linear, quadratic, or logarithmic model to match the data. 
    
## How to run

Simply load visualization.py into ipython3 and run visualization.setup() to launch the Dash web application that houses the interactive data visualization.
Once the application is launched, there are three dropdowns: the first selects the x variable, the second selects the y variable, and the third selects the variable that will be represented by the size of the bubble markers on the plot. 
Additionally, there are two checkboxes: the first is to include the third variable as a control in the regression analysis, and the second checkbox is to superimpose a curve of best fit on top of the data visualization.
Below the interactive menu are a couple of read outs: one describes each of the variables with information pulled from ourworldindata.org and the second is a statistical summary generated in R. 