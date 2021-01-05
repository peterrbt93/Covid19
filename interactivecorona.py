# -*- coding: utf-8 -*-
"""
Created on Wed Jun 17 12:14:09 2020

@author: pete_
"""

import plotly
import plotly.express as px
from plotly.offline import plot
import numpy as np
import pandas as pd
import math

#url for dataset
url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'

#create pandas dataframe from csv
df = pd.read_csv(url, delimiter=',', header='infer')

#selecting out countries of interest and removing countries with provinces
#find a way to add provinces together!!!!???

country_pop_dict = {'Colombia':51,'Mexico':129.2,'Peru':33,'United Kingdom':66.65, 'Denmark':5.8,'Germany': 83.02,'Russia':144.5, 'Netherlands':17.28, 'France':66.99,'Sweden': 10.23,'Spain': 46.94, 'Belgium':11.46,'US' :328.2,'Italy' :60.36,'Brazil': 209.5,'India': 1353}
country_list = list(country_pop_dict.keys())



df_interest = df.loc[
    df['Country/Region'].isin(country_list)
    & df['Province/State'].isna()]

#changing the location labels to be the countries
df_interest.rename(
    index=lambda x: df_interest.at[x, 'Country/Region'], inplace=True)

#transposing so that coloumns are countries and rows are dates
df1 = df_interest.transpose()

#remove uniteresting rows
df1 = df1.drop(['Province/State', 'Country/Region', 'Lat', 'Long'])

#remove dates where all have zero deaths
df1 = df1.loc[(df1 != 0).any(1)]

#Normalise wrt. population
pop_list = [country_pop_dict[i] for i in df1.columns]
df1 = df1/pop_list

#make new set which is shifted wrt 1 death per million
df2 = df1[df1>1]

#Set indices to be number of days
df2 = df2.set_index([pd.Series(range(0,len(df2['Italy'])))])

#Perform the shift
for country in country_list:
    df2[country] = list(df2[country].shift(-df2[country][df2[country]>1].index[0]))


#remove dates where all have NaN by checking if its equal to itself (Nan==Nan is false)
df2 = df2.loc[(df2 == df2).any(1)]

#Sorting dataframe coloumns after value
sort = list(pd.Series.sort_values(df2.max(),ascending=False).index)
df2 = df2[sort]

df1.index = pd.to_datetime(df1.index)

#un-comment if we want differences only
#df1 = df1.diff() #day on day changes
#df2 = df2.diff()

#%%


# =============================================================================
# #Plotting as function of date
# 
# #Create line plot
# fig = px.line()
# #Loop and add countries
# for i,n in enumerate(df1.columns):
#     fig.add_scatter(x=df1.index, y= df1[df1.columns[i]], name= df1.columns[i])
# #Add points at data
# fig.update_traces(mode='markers+lines')
# #Change layout
# fig.update_layout(
#     title = 'Deaths per million due to COVID-19'
#     ,xaxis_title = 'Dates'
#     ,yaxis_title = 'Number of Deaths per million'
#     ,font = dict(size = 15)
#     ,template = 'plotly_dark' #"plotly", "plotly_white", "plotly_dark", "ggplot2", "seaborn", "simple_white", "none"
# )
# #Add adjustable range on x-axis
# fig.update_xaxes(rangeslider_visible=True)
# 
# # =============================================================================
# # #Add drop-down menu
# # fig.update_layout(
# #     updatemenus=[
# #         dict(
# #            # type="buttons", #uncomment to get individual buttons
# #             direction="right",
# #             active=0,
# #             x=0.5,
# #             y=1.03,
# #             buttons=list([
# #                 dict(label=df1.columns[0],
# #                      method="update",
# #                      args=[ {"visible": [True, False, False, False, False]},
# #                             {'showlegend' : True}
# #                         ]),
# #                 dict(label=df1.columns[1],
# #                      method="update",
# #                      args=[ {"visible": [False, True, False, False, False]},
# #                             {'showlegend' : True}
# #                      ]),
# #                 dict(label=df1.columns[2],
# #                      method="update",
# #                      args=[ {"visible": [False, False, True, False, False]},
# #                             {'showlegend' : True}
# #                         ]),
# #                 dict(label=df1.columns[3],
# #                      method="update",
# #                      args=[ {"visible": [False, False, False, True, False]},
# #                             {'showlegend' : True}
# #                      ]),
# #                 dict(label=df1.columns[4],
# #                      method="update",
# #                      args=[ {"visible": [False, False, False, False, True]},
# #                             {'showlegend' : True}
# #                            ]),
# #                 dict(label='All',
# #                      method="update",
# #                      args=[ {"visible": [True, True, True, True, True]},
# #                             {'showlegend' : True}
# #                            ]),
# #             ]),
# #         )
# #     ]
# # )
# # 
# # =============================================================================
# #Plot figure
# plot(fig)
# =============================================================================

#Create list of symbol colors
symbol_col = ['white',
              'orange',
              'darkred',
              'darkgreen',
              'burlywood',
              'cyan',
              'lime',
              'darkorange',
              'deeppink',
              'grey',
              'gold',
              'red',
              'magenta',
              'blue',
              'peru',
              'steelblue',
              'tomato',
              'mistyrose']
#Plotting as function of days after 1 dead

#Create line plot
fig = px.line()
#Loop and add countries
for i,n in enumerate(df2.columns):
    fig.add_scatter(x=df2.index, y= df2[df2.columns[i]], name= df2.columns[i],marker_color=symbol_col[i],line_width=3, marker_size=5)
#Add points at data
fig.update_traces(mode='markers+lines')
#Change plot layout
fig.update_layout(
    title = dict(text ='Deaths due to COVID-19 (linear scale)', x =0.45)
    ,xaxis_title = 'Days since 1 dead per millon'
    ,yaxis_title = 'Deaths per million'
    ,font = dict(size = 24, family='Raleway')
    ,template = 'plotly_dark' #"plotly", "plotly_white", "plotly_dark", "ggplot2", "seaborn", "simple_white", "none"
)

#Change legend layout
fig.update_layout(
    legend=dict(
        traceorder="normal",
        font=dict(
            family="Raleway",
            size=16,
            color="white"
        ),
        bgcolor="Black",
        bordercolor="LightSteelBlue",
        borderwidth=2
    )
)


#Add adjustable range on x-axis
#fig.update_xaxes(rangeslider_visible=True)

# =============================================================================
# #Add drop-down menu
# fig.update_layout(
#     updatemenus=[
#         dict(
#            # type="buttons", #uncomment to get individual buttons
#             direction="right",
#             active=0,
#             x=0.5,
#             y=1.03,
#             buttons=list([
#                 dict(label=df1.columns[0],
#                      method="update",
#                      args=[ {"visible": [True, False, False, False, False]},
#                             {'showlegend' : True}
#                         ]),
#                 dict(label=df1.columns[1],
#                      method="update",
#                      args=[ {"visible": [False, True, False, False, False]},
#                             {'showlegend' : True}
#                      ]),
#                 dict(label=df1.columns[2],
#                      method="update",
#                      args=[ {"visible": [False, False, True, False, False]},
#                             {'showlegend' : True}
#                         ]),
#                 dict(label=df1.columns[3],
#                      method="update",
#                      args=[ {"visible": [False, False, False, True, False]},
#                             {'showlegend' : True}
#                      ]),
#                 dict(label=df1.columns[4],
#                      method="update",
#                      args=[ {"visible": [False, False, False, False, True]},
#                             {'showlegend' : True}
#                            ]),
#                 dict(label='All',
#                      method="update",
#                      args=[ {"visible": [True, True, True, True, True]},
#                             {'showlegend' : True}
#                            ]),
#             ]),
#         )
#     ]
# )
# =============================================================================

#Adjust layout and margins
fig.update_layout(
    autosize=False,
    width=1000,
    height=570,
    margin=dict(
        l=80,
        r=50,
        b=50,
        t=80,
        pad=4
    )
)
#Adjust x-axis
fig.update_xaxes(range=[0, len(df2['Italy'])])


#Plot figure
fig.write_image(r"C:\Users\pete_\Documents\Coding\git\Covid19\fig1.pdf")
fig.write_image(r"C:\Users\pete_\Documents\Coding\git\Covid19\fig1.jpeg", scale=8)
plot(fig)
