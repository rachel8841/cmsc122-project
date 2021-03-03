import plotly.graph_objects as go
from functools import reduce 
import pandas as pd
from math import log
import dash
import dash_core_components as dcc
import dash_html_components as html

def plot():
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


    dcc.Dropdown(
        options=[
            {'label': 'Afghanistan', 'value': 'AFG'},
            {'label': 'Albania', 'value': 'ALB'},
            {'label': 'Algeria', 'value': 'DZA'},
            {'label': 'Andorra', 'value': 'AND'},
            {'label': 'Angola', 'value': 'AGO'},
            {'label': 'Anguilla', 'value': 'AIA'},
            {'label': 'Antigua and Barbuda', 'value': 'ATG'},
            {'label': 'Argentina', 'value': 'ARG'},
            {'label': 'Armenia', 'value': 'ARM'},
            {'label': 'Aruba', 'value': 'ABW'},
            {'label': 'Australia', 'value': 'AUS'},
            {'label': 'Austria', 'value': 'AUT'},
            {'label': 'Azerbaijan', 'value': 'AZE'},
            {'label': 'Bahamas', 'value': 'BHS'},
            {'label': 'Bahrain', 'value': 'BHR'},
            {'label': 'Bangladesh', 'value': 'BGD'},
            {'label': 'Barbados', 'value': 'BRB'},
            {'label': 'Belarus', 'value': 'BLR'},
            {'label': 'Belgium', 'value': 'BEL'},
            {'label': 'Belize', 'value': 'BLZ'},
            {'label': 'Benin', 'value': 'BEN'},
            {'label': 'Bhutan', 'value': 'BTN'},
            {'label': 'Bolivia', 'value': 'BOL'},
            {'label': 'Bosnia and Herzegovina', 'value': 'BIH'},
            {'label': 'Botswana', 'value': 'BWA'},
            {'label': 'Brazil', 'value': 'BRA'},
            {'label': 'Brunei', 'value': 'BRN'},
            {'label': 'Bulgaria', 'value': 'BGR'},
            {'label': 'Burkina Faso', 'value': 'BFA'},
            {'label': 'Burundi', 'value': 'BDI'},
            {'label': 'Cambodia', 'value': 'KHM'},
            {'label': 'Cameroon', 'value': 'CMR'},
            {'label': 'Canada', 'value': 'CAN'},
            {'label': 'Cape Verde', 'value': 'CPV'},
            {'label': 'Central African Republic', 'value': 'CAF'},
            {'label': 'Chad', 'value': 'TCD'},
            {'label': 'Chile', 'value': 'CHL'},
            {'label': 'China', 'value': 'CHM'},
            {'label': 'Colombia', 'value': 'COL'},
            {'label': 'Comoros', 'value': 'COM'},
            {'label': 'Congo', 'value': 'COG'},
            {'label': 'Cook Islands', 'value': 'COK'},
            {'label': 'Costa Rica', 'value': 'CRI'},
            {'label': "Cote d'Ivoire", 'value': 'CIV'},
            {'label': 'Croatia', 'value': 'HRV'},
            {'label': 'Cuba', 'value': 'CUB'},
            {'label': 'Curacao', 'value': 'CUW'},
            {'label': 'Cyprus', 'value': 'CYP'},
            {'label': 'Czechia', 'value': 'CZE'},
            {'label': 'Democratic Republic of Congo', 'value': 'COD'},
            {'label': 'Denmark', 'value': 'DNK'},
            {'label': 'Djibouti', 'value': 'DJI'},
            {'label': 'Dominica', 'value': 'DMA'},
            {'label': 'Dominican Republic', 'value': 'DOM'},
            {'label': 'Ecuador', 'value': 'ECU'},
            {'label': 'Egypt', 'value': 'EGY'},
            {'label': 'El Salvador', 'value': 'SLV'},
            {'label': 'Equatorial Guinea', 'value': 'GNQ'},
            {'label': 'Eritrea', 'value': 'ERI'},
            {'label': 'Estonia', 'value': 'EST'},
            {'label': 'Eswatini', 'value': 'SWZ'},
            {'label': 'Ethiopia', 'value': 'ETH'},
            {'label': 'Fiji', 'value': 'FJI'},
            {'label': 'Finland', 'value': 'FIN'},
            {'label': 'France', 'value': 'FRA'},
            {'label': 'French Guiana', 'value': 'GUF'},
            {'label': 'Gabon', 'value': 'GAB'},
            {'label': 'Gambia', 'value': 'GMB'},
            {'label': 'Georgia', 'value': 'GEO'},
            {'label': 'Germany', 'value': 'DEU'},
            {'label': 'Ghana', 'value': 'GHA'},
            {'label': 'Greece', 'value': 'GRC'},
            {'label': 'Grenada', 'value': 'GRD'},
            {'label': 'Guam', 'value': 'GUM'},
            {'label': 'Guatemala', 'value': 'GTM'},
            {'label': 'Guinea', 'value': 'GIN'},
            {'label': 'Guinea-Bissau', 'value': 'GNM'},
            {'label': 'Guyana', 'value': 'GUY'},
            {'label': 'Haiti', 'value': 'HTI'},
            {'label': 'Honduras', 'value': 'HND'},
            {'label': 'Hong Kong', 'value': 'HKG'},
            {'label': 'Hungary', 'value': 'HUN'},
            {'label': 'Iceland', 'value': 'ISL'},
            {'label': 'India', 'value': 'IND'},
            {'label': 'Indonesia', 'value': 'IDN'},
            {'label': 'Iran', 'value': 'IRN'},
            {'label': 'Iraq', 'value': 'IRQ'},
            {'label': 'Ireland', 'value': 'IRL'},
            {'label': 'Israel', 'value': 'ISR'},
            {'label': 'Italy', 'value': 'ITA'},
            {'label': 'Jamaica', 'value': 'JAM'},
            {'label': 'Japan', 'value': 'JPN'},
            {'label': 'Jordan', 'value': 'JOR'},
            {'label': 'Kazakhstan', 'value': 'KAZ'},
            {'label': 'Kenya', 'value': 'KEN'},
            {'label': 'Kiribati', 'value': 'KIR'},
            {'label': 'Kuwait', 'value': 'KWT'},
            {'label': 'Kyrgyzstan', 'value': 'KGZ'},
            {'label': 'Laos', 'value': 'LAO'},
            {'label': 'Latvia', 'value': 'LVA'},
            {'label': 'Lebanon', 'value': 'LBN'},
            {'label': 'Lesotho', 'value': 'LSO'},
            {'label': 'Liberia', 'value': 'LBR'},
            {'label': 'Libya', 'value': 'LBY'},
            {'label': 'Lithuania', 'value': 'LTU'},
            {'label': 'Luxembourg', 'value': 'LUX'},
            {'label': 'Macao', 'value': 'MAC'},
            {'label': 'Madagascar', 'value': 'MDG'},
            {'label': 'Malawi', 'value': 'MWI'},
            {'label': 'Malaysia', 'value': 'MYS'},
            {'label': 'Maldives', 'value': 'MDV'},
            {'label': 'Mali', 'value': 'MLI'},
            {'label': 'Malta', 'value': 'MLT'},
            {'label': 'Marshall Islands', 'value': 'MHL'},
            {'label': 'Martinique', 'value': 'MTQ'},
            {'label': 'Mauritania', 'value': 'MRT'},
            {'label': 'Mauritius', 'value': 'MUS'},
            {'label': 'Mayotte', 'value': 'MYT'},
            {'label': 'Mexico', 'value': 'MEX'},
            {'label': 'Micronesia', 'value': 'FSM'},
            {'label': 'Moldova', 'value': 'MDA'},
            {'label': 'Monaco', 'value': 'MCO'},
            {'label': 'Mongolia', 'value': 'MNG'},
            {'label': 'Montenegro', 'value': 'MNE'},
            {'label': 'Morocco', 'value': 'MAR'},
            {'label': 'Mozambique', 'value': 'MOZ'},
            {'label': 'Myanmar', 'value': 'MMR'},
            {'label': 'Namibia', 'value': 'NAM'},
            {'label': 'Nauru', 'value': 'NRU'},
            {'label': 'Nepal', 'value': 'NPL'},
            {'label': 'Netherlands', 'value': 'NLD'},
            {'label': 'New Caledonia', 'value': 'NCL'},
            {'label': 'New Zealand', 'value': 'NZL'},
            {'label': 'Nicaragua', 'value': 'NIC'},
            {'label': 'Niger', 'value': 'NER'},
            {'label': 'Nigeria', 'value': 'NGA'},
            {'label': 'Niue', 'value': 'NIU'},
            {'label': 'North Korea', 'value': 'PRK'},
            {'label': 'North Macedonia', 'value': 'MKD'},
            {'label': 'Oman', 'value': 'OMN'},
            {'label': 'Pakistan', 'value': 'PAK'},
            {'label': 'Palau', 'value': 'PLW'},
            {'label': 'Palestine', 'value': 'PSE'},
            {'label': 'Panama', 'value': 'PAN'},
            {'label': 'Papua New Guinea', 'value': 'PNG'},
            {'label': 'Paraguay', 'value': 'PRY'},
            {'label': 'Peru', 'value': 'PER'},
            {'label': 'Philippines', 'value': 'PHL'},
            {'label': 'Poland', 'value': 'POL'},
            {'label': 'Portugal', 'value': 'PRT'},
            {'label': 'Puerto Rico', 'value': 'PRI'},
            {'label': 'Qatar', 'value': 'QAT'},
            {'label': 'Romania', 'value': 'ROU'},
            {'label': 'Russia', 'value': 'RUS'},
            {'label': 'Rwanda', 'value': 'RWA'},
            {'label': 'Saint Kitts and Nevis', 'value': 'KNA'},
            {'label': 'Saint Lucia', 'value': 'LCA'},
            {'label': 'Saint Vincent and the Grenadines', 'value': 'VCT'},
            {'label': 'Samoa', 'value': 'WSM'},
            {'label': 'San Marino', 'value': 'SMR'},
            {'label': 'Sao Tome and Principe', 'value': 'STP'},
            {'label': 'Saudi Arabia', 'value': 'SAU'},
            {'label': 'Senegal', 'value': 'SEN'},
            {'label': 'Serbia', 'value': 'SRB'},
            {'label': 'Seychelles', 'value': 'SYC'},
            {'label': 'Sierra Leone', 'value': 'SLE'},
            {'label': 'Singapore', 'value': 'SGP'},
            {'label': 'Slovakia', 'value': 'SVK'},
            {'label': 'Slovenia', 'value': 'SVN'},
            {'label': 'Solomon Islands', 'value': 'SLB'},
            {'label': 'Somalia', 'value': 'SOM'},
            {'label': 'South Africa', 'value': 'ZAF'},
            {'label': 'South Korea', 'value': 'KOR'},
            {'label': 'South Sudan', 'value': 'SSD'},
            {'label': 'Spain', 'value': 'ESP'},
            {'label': 'Sri Lanka', 'value': 'LKA'},
            {'label': 'Sudan', 'value': 'SDN'},
            {'label': 'Suriname', 'value': 'SUR'},
            {'label': 'Switzerland', 'value': 'CHE'},
            {'label': 'Syria', 'value': 'SYR'},
            {'label': 'Tajikistan', 'value': 'TJK'},
            {'label': 'Tanzania', 'value': 'TZA'},
            {'label': 'Tajikistan', 'value': 'TJK'},
            {'label': 'Thailand', 'value': 'THA'},
            {'label': 'Timor', 'value': 'TLS'},
            {'label': 'Togo', 'value': 'TGO'},
            {'label': 'Tonga', 'value': 'TON'},
            {'label': 'Trinidad and Tobago', 'value': 'TTO'},
            {'label': 'Tunisia', 'value': 'TUN'},
            {'label': 'Turkey', 'value': 'TUR'},
            {'label': 'Turkmenistan', 'value': 'TKM'},
            {'label': 'Tuvalu', 'value': 'TUV'},
            {'label': 'Uganda', 'value': 'UGA'},
            {'label': 'Ukraine', 'value': 'UKR'},
            {'label': 'United Arab Emirates', 'value': 'ARE'},
            {'label': 'United Kingdom', 'value': 'GBR'},
            {'label': 'United States', 'value': 'USA'},
            {'label': 'Uzbekistan', 'value': 'UZB'},
            {'label': 'Vanuatu', 'value': 'VUT'},
            {'label': 'Venezuela', 'value': 'VEN'},
            {'label': 'Vietnam', 'value': 'VNM'},
            {'label': 'Yemen', 'value': 'YEM'},
            {'label': 'Zambia', 'value': 'ZMB'},
            {'label': 'Zimbabwe', 'value': 'ZWE'}
        ],
        value=['MTL', 'NYC'],
        multi=True
    )  

    fig = go.Figure(fig_dict)
    fig.show()