import plotly.graph_objects as go
from functools import reduce 
import pandas as pd
from math import log
import dash
import dash_core_components as dcc
import dash_html_components as html
import dataframes
import webscraping
import util
import R_regression
import line

top_ten = ["USA", "GBR", "BRA", "CHN", "IND", "RUS", "JPN", "SAU", "NGA", "ZAF"]
top_twenty = top_ten + ["DEU", "FRA", "NLD", "ARG", "MEX", "IDN", "IRN", "TUR", 
    "ARE", "EGY"]

custom_colors = {
        'Asia': 'rgb(137, 182, 51)',
        'Europe': 'rgb(249, 180, 15)',
        'Africa': 'rgb(180, 15, 249)',
        'South America': 'rgb(240, 107, 12)',
        'North America': 'rgb(244, 12, 13)',
        'Oceania': 'rgb(15, 84, 249)'
    }

codes = ['AFG', 'ALB', 'DZA', 'AND', 'AGO', 'AIA', 'ATG', 'ARG', 'ARM', 'ABW',
    'AUS', 'AUT', 'AZE', 'BHS', 'BHR', 'BGD', 'BRB', 'BLR', 'BEL', 'BLZ',
    'BEN', 'BTN', 'BOL', 'BIH', 'BWA', 'BRA', 'BRN', 'BGR', 'BFA', 'BDI',
    'KHM', 'CMR', 'CAN', 'CPV', 'CAF', 'TCD', 'CHL', 'CHM', 'COL', 'COM',
    'COG', 'COK', 'CRI', 'CIV', 'HRV', 'CUB', 'CUW', 'CYP', 'CZE', 'COD',
    'DNK', 'DJI', 'DMA', 'DOM', 'ECU', 'EGY', 'SLV', 'GNQ', 'ERI', 'EST',
    'SWZ', 'ETH', 'FJI', 'FIN', 'FRA', 'GUF', 'GAB', 'GMB', 'GEO', 'DEU',
    'GHA', 'GRC', 'GRD', 'GUM', 'GTM', 'GIN', 'GNM', 'GUY', 'HTI', 'HND',
    'HKG', 'HUN', 'ISL', 'IND', 'IDN', 'IRN', 'IRQ', 'IRL', 'ISR', 'ITA',
    'JAM', 'JPN', 'JOR', 'KAZ', 'KEN', 'KIR', 'KWT', 'KGZ', 'LAO', 'LVA',
    'LBN', 'LSO', 'LBR', 'LBY', 'LTU', 'LUX', 'MAC', 'MDG', 'MWI', 'MYS',
    'MDV', 'MLI', 'MLT', 'MHL', 'MTQ', 'MRT', 'MUS', 'MYT', 'MEX', 'FSM',
    'MDA', 'MCO', 'MNG', 'MNE', 'MAR', 'MOZ', 'MMR', 'NAM', 'NRU', 'NPL',
    'NLD', 'NCL', 'NZL', 'NIC', 'NER', 'NGA', 'NIU', 'PRK', 'MKD', 'OMN',
    'PAK', 'PLW', 'PSE', 'PAN', 'PNG', 'PRY', 'PER', 'PHL', 'POL', 'PRT',
    'PRI', 'QAT', 'ROU', 'RUS', 'RWA', 'KNA', 'LCA', 'VCT', 'WSM', 'SMR',
    'STP', 'SAU', 'SEN', 'SRB', 'SYC', 'SLE', 'SGP', 'SVK', 'SVN', 'SLB',
    'SOM', 'ZAF', 'KOR', 'SSD', 'ESP', 'LKA', 'SDN', 'SUR', 'CHE', 'SYR',
    'TJK', 'TZA', 'TJK', 'THA', 'TLS', 'TGO', 'TON', 'TTO', 'TUN', 'TUR',
    'TKM', 'TUV', 'UGA', 'UKR', 'ARE', 'GBR', 'USA', 'UZB', 'VUT', 'VEN',
    'VNM', 'YEM', 'ZMB', 'ZWE']

variable_dict_list = [
    {'label': 'Broadband Subscriptions', 'value': 'fixed-broadband-subscriptions-per-100-people'},
    {'label': 'Child Mortality', 'value': 'child-mortality'},
    {'label': 'CO2 Emissions', 'value': 'annual-co2-emissions-per-country'},
    {'label': 'Disability Adjusted Life Years', 'value': 'dalys-rate-from-all-causes'},
    {'label': 'Age Dependency Ratio', 'value': 'age-dependency-ratio-of-working-age-population'},
    {'label': 'Deaths from Drugs and Alcohol', 'value': 'deaths-from-alcohol-and-drug-use-disorders'},
    {'label': 'Years of Expected Schooling', 'value': 'expected-years-of-schooling'},
    {'label': 'Female Labor Force Participation Rate', 'value': 'oecd-female-labour-force-participation-rate-15-64'},
    {'label': 'Government Expenditure per Capita', 'value': 'total-gov-expenditure-gdp-wdi'},
    {'label': 'Happiness', 'value': 'happiness-cantril-ladder'},
    {'label': 'Homicides', 'value': 'intentional-homicides-per-100000-people'},
    {'label': 'Savings', 'value': 'adjusted-net-savings-per-person'},
    {'label': 'Life Expectancy', 'value': 'life-expectancy'},
    {'label': 'Working Hours', 'value': 'annual-working-hours-per-worker'},
    {'label': 'Contraceptive Prevalence', 'value': 'contraceptive-prevalence-any-methods-vs-modern-methods'},
    {'label': 'Military Expenditure', 'value': 'military-expenditure-as-share-of-gdp'},
    {'label': 'Public Health Expenditure', 'value': 'public-health-expenditure-share-gdp-owid'},
    {'label': 'GDP per capita', 'value': 'average-real-gdp-per-capita-across-countries-and-regions'},
    {'label': 'Access to Electricity', 'value': 'Share-of-the-population-with-access-to-electricity'},
    {'label': 'Education Expenditure', 'value': 'total-government-expenditure-on-eduation-gdp'},
    {'label': 'Out of Pocket Healthcare Expenditure', 'value': 'out-of-pocket-expenditure-per-capita-on-healthcare'},
    {'label': 'Trade', 'value': 'trade-as-share-of-gdp'}
]
'''
same as variable_dict_list, but excludes some variables that wouldn't make
sense when represented as a marker bubble
for example, savings (which sometimes has negative values) or military 
expenditure as a % of gdp, since this doesn't vary much between countries
'''
bub_dict_list = [
    {'label': 'Broadband Subscriptions', 'value': 'fixed-broadband-subscriptions-per-100-people'},
    {'label': 'Child Mortality', 'value': 'child-mortality'},
    {'label': 'CO2 Emissions', 'value': 'annual-co2-emissions-per-country'},
    {'label': 'Deaths from Drugs and Alcohol', 'value': 'deaths-from-alcohol-and-drug-use-disorders'},
    {'label': 'Female Labor Force Participation Rate', 'value': 'oecd-female-labour-force-participation-rate-15-64'},
    {'label': 'Government Expenditure per Capita', 'value': 'total-gov-expenditure-gdp-wdi'},
    {'label': 'Homicides', 'value': 'intentional-homicides-per-100000-people'},
    {'label': 'Savings', 'value': 'adjusted-net-savings-per-person'},
    {'label': 'Inequality', 'value': 'economic-inequality-gini-index'},
    {'label': 'Working Hours', 'value': 'annual-working-hours-per-worker'},
    {'label': 'Military Expenditure', 'value': 'military-expenditure-as-share-of-gdp'},
    {'label': 'Public Health Expenditure', 'value': 'public-health-expenditure-share-gdp-owid'},
    {'label': 'GDP per capita', 'value': 'average-real-gdp-per-capita-across-countries-and-regions'},
    {'label': 'Access to Electricity', 'value': 'Share-of-the-population-with-access-to-electricity'},
    {'label': 'Education Expenditure', 'value': 'total-government-expenditure-on-eduation-gdp'},
    {'label': 'Out of Pocket Healthcare Expenditure', 'value': 'out-of-pocket-expenditure-per-capita-on-healthcare'},
    {'label': 'Trade', 'value': 'trade-as-share-of-gdp'}
]
country_dict_list = [
                {'label': 'All countries', 'value': 'ALL'},
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
            ]

def plot(var_list, countries, control):
    '''
    var_list: list of strings
    var_list[0] is x variable
    var_list[1] is y variable
    var_list[2] is bubble size
    '''

    merged = dataframes.create_dataframes(var_list, countries)

    #list of the names of the columns
    col_list = [merged.columns[3], merged.columns[4], merged.columns[5]]
    continents_df = pd.read_csv("data/continents.csv")

    merged = reduce(lambda left, right: pd.merge(left,right,on=['Code', 'Entity']), [merged, continents_df])
    years = list(set(merged['Year']))
    continents = list(set(merged["Continent"]))

    # make figure
    fig_dict = {
        "data": [],
        "layout": {},
        "frames": []
    }

    # fill in most of layout
    fig_dict["layout"]["xaxis"] = {"title": col_list[0]}
    fig_dict["layout"]["yaxis"] = {"title": col_list[1]}
    fig_dict["layout"]["hovermode"] = "closest"
    fig_dict["layout"]["updatemenus"] = [
        {
            "buttons": [
                {
                    "args": [None, {"frame": {"duration": 500},
                                    "fromcurrent": True, "transition": {"duration": 300,
                                                                        "easing": "quadratic-in-out"}}],
                    "label": "Play",
                    "method": "animate"
                },
                {
                    "args": [[None], {"frame": {"duration": 0},
                                    "mode": "immediate"}],
                    "label": "Pause",
                    "method": "animate"
                }
            ],
            "direction": "left",
            "pad": {"r": 10, "t": 87},
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

    #makes the first frame of data for the first year
    year = years[0]
    for continent in continents:
        dataset_by_year = merged[merged["Year"] == year]
        dataset_by_year_and_cont = dataset_by_year[
            dataset_by_year["Continent"] == continent]

        data_dict = {
            "x": list(dataset_by_year_and_cont[col_list[0]]),
            "y": list(dataset_by_year_and_cont[col_list[1]]),
            "mode": "markers",
            "text": list(dataset_by_year_and_cont["Entity"]),
            "marker": {
                "sizemode": "area",
                "sizeref": 15000,
                "size": list(dataset_by_year_and_cont[col_list[2]])
            },
            "name": continent
        }
        fig_dict["data"].append(data_dict)


    #makes the frames of the animation
    for year in years:
        frame = {"data": [], "name": str(year)}
        for continent in continents:
            dataset_by_year = merged[merged["Year"] == int(year)]
            dataset_by_year_and_cont = dataset_by_year[
                dataset_by_year["Continent"] == continent]

            data_dict = {
                "x": list(dataset_by_year_and_cont[col_list[0]]),
                "y": list(dataset_by_year_and_cont[col_list[1]]),
                "mode": "markers",
                "text": list(dataset_by_year_and_cont["Entity"]),
                "marker": {
                    "sizemode": "area",
                    "sizeref": 2*max(merged[col_list[2]]) / (15000),
                    "size": [abs(item) for item in list(dataset_by_year_and_cont[col_list[2]])],
                    "color": custom_colors[continent]
                },
                "name": continent
            }
            frame["data"].append(data_dict)

        #regression line
        control_var = None
        if control == 'True':
            control_var = var_list[2]

        x_range = [merged[col_list[0]].min(), merged[col_list[0]].max()]

        frame["data"].append(line.create_function(x_range, var_list, R_stuff.regression_in_R(var_list[0], var_list[1], year, control_var)))
        fig_dict["frames"].append(frame)

        slider_step = {"args": [
            [year],
            {"frame": {"duration": 300},
            "mode": "immediate",
            "transition": {"duration": 300}}
        ],
            "label": year,
            "method": "animate"}
        sliders_dict["steps"].append(slider_step)


    fig_dict["layout"]["sliders"] = [sliders_dict]
    
    fig = go.Figure(fig_dict)

    #rescales the axes to include the maximum and mininum values of the variables
    fig.update_xaxes(range=[merged[col_list[0]].min() - 
        .2*merged[col_list[0]].max(),
        merged[col_list[0]].max() + .2*merged[col_list[0]].max()])
    fig.update_yaxes(range=[merged[col_list[1]].min() - 
        .2*merged[col_list[1]].max(),
        merged[col_list[1]].max() + .2*merged[col_list[1]].max()])

    #sets size of scatter plot
    fig.update_layout(
        autosize=True,
        width=1000,
        height=600,
        showlegend = True,
        legend = {
            'itemsizing': 'constant',
            'traceorder': 'normal'
        }
    )
    return fig, col_list

def setup():
    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

    app.layout = html.Div([
        dcc.Dropdown(
            id='xvar-dropdown',
            options=variable_dict_list,
            value='fixed-broadband-subscriptions-per-100-people'
        ),
        dcc.Dropdown(
            id='yvar-dropdown',
            options=variable_dict_list,
            value="child-mortality"
        ),
        dcc.Dropdown(
            id='bubblevar-dropdown',
            options=variable_dict_list,
            value='annual-co2-emissions-per-country'
        ),
        dcc.Dropdown(
            id='country-dropdown',
            options=country_dict_list,
            value=top_twenty,
            multi=True
        ),
        dcc.Checklist(
            id='control-check',
            options=[
                {'label': 'Use third variable as control', 'value': 'True'}
            ],
            value = []
        ),
        html.H4("Description of variables:"),
        html.Br(),
        html.Div(id='x-description'),
        html.Br(),
        html.Div(id='y-description'),
        html.Br(),
        html.Div(id='bub-description'),
        html.H4("Statistics summary:"),
        html.Br(),
        html.Div(id='stat-summary'),
        dcc.Graph(id='graph-court'),
    ])
    @app.callback(
        [dash.dependencies.Output('graph-court', 'figure'), 
            dash.dependencies.Output(component_id='x-description', component_property='children'),
            dash.dependencies.Output(component_id='y-description', component_property='children'),
            dash.dependencies.Output(component_id='bub-description', component_property='children'),
            dash.dependencies.Output(component_id='stat-summary', component_property='children')],
        [dash.dependencies.Input('xvar-dropdown', 'value'), 
            dash.dependencies.Input('yvar-dropdown', 'value'), 
            dash.dependencies.Input('bubblevar-dropdown', 'value'), 
            dash.dependencies.Input('country-dropdown', 'value'),
            dash.dependencies.Input('control-check', 'value')
            ]
        )
    
    #creates graph based on the selections on the drop down menus
    def create_graph(xval, yval, bubval, countries, control):
        if 'ALL' in countries:
            countries = codes
        var_list = [xval, yval, bubval]

        fig, col_list = plot(var_list, countries, control)

        descriptions = webscraping.scrape(var_list)

        label_names = [dataframes.clean_column_name(item) for item in col_list]
        x_desc = label_names[0] + ": " + descriptions[0]
        y_desc = label_names[1] + ": " + descriptions[1]
        bub_desc = label_names[2] + ": " + descriptions[2]
        stat_summary = ""

        return (fig, x_desc, y_desc, bub_desc, stat_summary)

    if __name__ == '__main__':
        app.run_server(debug=True)
    app.run_server(debug=True, use_reloader=False)
