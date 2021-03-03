import plotly.graph_objects as go
from functools import reduce 
import pandas as pd
from math import log
import dash
import dash_core_components as dcc
import dash_html_components as html
import dataframes

def setup():

    savings = pd.read_csv("data/savings.csv")
    co2 = pd.read_csv("data/co2.csv")
    drug_deaths = pd.read_csv("data/drug-deaths.csv")
    continents = pd.read_csv("data/continents.csv")

    merged = reduce(lambda left, right: pd.merge(left,right,on=['Code','Year', 'Entity']), [savings,co2, drug_deaths])
    merged = reduce(lambda left, right: pd.merge(left,right,on=['Code', 'Entity']), [merged, continents])
    years = list(set(merged['Year']))
    continents = list(set(merged["Continent"]))

    # make figure
    fig_dict = {
        "data": [],
        "layout": {},
        "frames": []
    }

    # fill in most of layout
    fig_dict["layout"]["xaxis"] = {"title": "Savings"}
    fig_dict["layout"]["yaxis"] = {"title": "CO2", "type": "log"}
    fig_dict["layout"]["hovermode"] = "closest"
    fig_dict["layout"]["updatemenus"] = [
        {
            "buttons": [
                {
                    "args": [None, {"frame": {"duration": 500, "redraw": False},
                                    "fromcurrent": True, "transition": {"duration": 300,
                                                                        "easing": "quadratic-in-out"}}],
                    "label": "Play",
                    "method": "animate"
                },
                {
                    "args": [[None], {"frame": {"duration": 0, "redraw": False},
                                    "mode": "immediate",
                                    "transition": {"duration": 0}}],
                    "label": "Pause",
                    "method": "animate"
                }
            ],
            "direction": "left",
            "pad": {"r": 10, "t": 87},
            "showactive": False,
            "type": "buttons",
            "x": 0.1,
            "xanchor": "right",
            "y": 0,
            "yanchor": "top"
        }
    ]

    sliders_dict = {
        "active": 0,
        "yanchor": "top",
        "xanchor": "left",
        "currentvalue": {
            "font": {"size": 20},
            "prefix": "Year:",
            "visible": True,
            "xanchor": "right"
        },
        "transition": {"duration": 300, "easing": "cubic-in-out"},
        "pad": {"b": 10, "t": 50},
        "len": 0.9,
        "x": 0.1,
        "y": 0,
        "steps": []
    }

    # make data
    year = years[0]
    for continent in continents:
        dataset_by_year = merged[merged["Year"] == year]
        dataset_by_year_and_cont = dataset_by_year[
            dataset_by_year["Continent"] == continent]

        data_dict = {
            "x": list(dataset_by_year_and_cont["Adjusted net savings per capita (World Bank (2017))"]),
            "y": list(dataset_by_year_and_cont["Annual CO2 emissions"]),
            "mode": "markers",
            "text": list(dataset_by_year_and_cont["Entity"]),
            "marker": {
                "sizemode": "area",
                "sizeref": 200000,
                "size": list(dataset_by_year_and_cont["Deaths - Alcohol and substance use disorders"])
            },
            "name": continent
        }
        fig_dict["data"].append(data_dict)

    # make frames
    for year in years:
        frame = {"data": [], "name": str(year)}
        for continent in continents:
            dataset_by_year = merged[merged["Year"] == int(year)]
            dataset_by_year_and_cont = dataset_by_year[
                dataset_by_year["Continent"] == continent]

            data_dict = {
                "x": list(dataset_by_year_and_cont["Adjusted net savings per capita (World Bank (2017))"]),
                "y": list(dataset_by_year_and_cont["Annual CO2 emissions"]),
                "mode": "markers",
                "text": list(dataset_by_year_and_cont["Entity"]),
                "marker": {
                    "sizemode": "area",
                    "sizeref": 2*max(merged["Deaths - Alcohol and substance use disorders"]) / (50000),
                    "size": list(dataset_by_year_and_cont["Deaths - Alcohol and substance use disorders"])
                },
                "name": continent
            }
            frame["data"].append(data_dict)

        fig_dict["frames"].append(frame)
        slider_step = {"args": [
            [year],
            {"frame": {"duration": 300, "redraw": False},
            "mode": "immediate",
            "transition": {"duration": 300}}
        ],
            "label": year,
            "method": "animate"}
        sliders_dict["steps"].append(slider_step)


    fig_dict["layout"]["sliders"] = [sliders_dict]
    
    fig = go.Figure(fig_dict)

    app = dash.Dash()
    app.layout = html.Div([
        dcc.Dropdown(
            id = 'city_dropdown',
            options = [
                {'label': 'New York City', 'value': 'NYC'},
                {'label': 'Los Angeles', 'value': 'LA'}
            ],
            value = 'NYC'
        ),
        html.Div(id='city-output-container'),
        '''
        dcc.Dropdown(
            id = 'state_dropdown',
            options = [
                {'label': 'New York', 'value': 'NY'},
                {'label': 'California', 'value': 'CA'}
            ],
            value = 'NY'
        ),
        html.Div(id='state-output-container'),
        '''
        dcc.Graph(figure=fig)
    ])
    @app.callback(
        dash.dependencies.Output('city-output-container', 'children'),
        #dash.dependencies.Output('state-output-container', 'children'),
        [dash.dependencies.Input('city_dropdown', 'value')],
        #[dash.dependencies.Input('state_dropdown', 'value2')],
        )
    def update_output1(value):
        return 'You have selected "{}"'.format(value)

    if __name__ == '__main__':
        app.run_server(debug=True)
    app.run_server(debug=True, use_reloader=False)