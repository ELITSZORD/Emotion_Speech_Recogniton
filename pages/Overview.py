
# Import Library
import dash
from dash import Dash
from dash import dcc
from dash import html, dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from dash import callback, ctx, State
from dash import register_page, page_container

import PIL.Image as Image
import plotly.express as px 


import librosa
import librosa.display


import matplotlib
import matplotlib.axes
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import os

import io
import base64
from dash.exceptions import PreventUpdate


# Register
dash.register_page(__name__, path='/overview1')

# Style
hstyle2 = {"background": "#50596E", "color": "white", "font-size": "30px",'width': '100%', 'text-align':'center'}
hstyle3 = {"background": "#55936D", "color": "blue", "font-size": "20px"}

hstyle4 = {"background": "#339288", "color": "white", "font-size": "19px",'width': '20%'}

hstyle5 = {"color": "black", "font-size": "14px",'width': '22%', 'text-align':'center'}
hstyle6 = {"color": "black", "font-size": "20px",'width': '20%', 'text-align':'center'}

layout = html.Div()

## Overview
@callback(Output('over1', 'children'),
              [Input('overview', 'n_clicks')])

def overv1(n_clicks):
    if n_clicks is not None:
        return html.Div([
            # Left Column           
            dbc.Col(
                    dbc.Row([
                        html.Div(id='sos1'),                        
                        html.Div(id='drop1'),
                        html.Div(id='butt1'),
                        html.Div(id='tabl1'),
                    ])
                ),
            # Right Column
            dbc.Col(
                    dbc.Row([
                        html.Div(id='sos2'),
                        html.Div(id='drop2'),
                        html.Div(id='butt2'),
                        html.Div(id='tabl2'),
                    ])
                )
        ])                  
    
    else:
        return html.Div()

# Left Column--------------------------------------------------------------------------------------------------------------------------------------------
## HeadLine 1 Callback
@callback(Output('sos1', 'children'),
              [Input('overview', 'n_clicks')])

def hdl1(n_clicks):
    if n_clicks is not None:
        return dbc.Row([            
            html.H1("Pre-Survey Emotional Response", style=hstyle2)    
                        
        ])           
    
    else:
        return html.Div()

## Drop down 1 Callback 
@callback(
    Output('drop1', 'children'),
    [Input('overview', 'n_clicks')]
)
def dropd1(n_clicks):
    if n_clicks is not None:
        return dbc.Row([            
            dcc.Dropdown(
                            ['Product', 'Campaign', 'Specific Survey/Questionnaire Question No. 1','Specific Survey/Questionnaire Question No. 2'],
                            searchable=False, placeholder="Choose an Observed",style=hstyle3)    
                        
        ])           
    
    else:
        return html.Div()

## Button 1 Callback
@callback(
    Output('butt1', 'children'),
    [Input('overview', 'n_clicks')]
)
def but1(n_clicks):
    if n_clicks is not None:
        return dbc.Row([
            html.Div([
                            html.Button('Anger', id='btn-11',style=hstyle4),
                            html.Button('Happiness', id='btn-21',style=hstyle4),
                            html.Button('Neutral', id='btn-31',style=hstyle4),
                            html.Button('Sadness', id='btn-41',style=hstyle4),
                            html.Button('Reset', id='btn-51',style=hstyle4),
                            html.Div(id='container1')
                        ])                        
        ])           
    
    else:
        return html.Div()

@callback(Output('container1', 'children'),
              Input('btn-11', 'n_clicks'),
              Input('btn-21', 'n_clicks'),
              Input('btn-31', 'n_clicks'),
              Input('btn-41', 'n_clicks')
              ) 

def display1(btn1, btn2, btn3, btn4):
    button_id1 = ctx.triggered_id if not None else 'No clicks yet'
    return dbc.Row([html.Div([
        html.Table([
            html.Tr([html.Th('Anger (y0)',style=hstyle5),
                     html.Th('Happiness (y1)',style=hstyle5),
                     html.Th('Neutral (y2)',style=hstyle5),
                     html.Th('Sadness (y3)',style=hstyle5),                     
                     html.Th('Most Recent Click')]),
            html.Tr([html.Td(btn1 or 0,style=hstyle6), 
                     html.Td(btn2 or 0,style=hstyle6), 
                     html.Td(btn3 or 0,style=hstyle6), 
                     html.Td(btn4 or 0,style=hstyle6), 
                     html.Td(button_id1,style=hstyle6)])
        ])
    ])])

## Reset Button 1 Call back
@callback(Output('btn-11', 'n_clicks'), Output('btn-21', 'n_clicks'), Output('btn-31', 'n_clicks'), Output('btn-41', 'n_clicks'),
              Input('btn-51', 'n_clicks'))
def update1(reset):
    return 0,0,0,0

# Table 1 Left

@callback(
    Output('tabl1', 'children'),
    [Input('overview', 'n_clicks')]
)
def tab1(n_clicks):
    if n_clicks is not None:
        return html.Div([html.Div([            
                    dcc.Input(
                        id='editing-columns-name',
                        placeholder='Enter a column name...',
                        value='',
                        style={'padding': 10}
                    ),
                    html.Button('Add Column', id='editing-columns-button', n_clicks=0)
                    ], style={'height': 50}),
                         
                dash_table.DataTable(
                    id='editing-columns',
                    columns=[{
                        'name': 'Column {}'.format(i),
                        'id': 'column-{}'.format(i),
                        'deletable': True,
                        'renamable': True
                    } for i in range(1, 4)],
                    data=[
                        {'column-{}'.format(i): (j + (i-1)*4) for i in range(1, 4)}
                        for j in range(4)
                    ],
                    editable=True,export_format='xlsx',
                ),
                dcc.Graph(id='editing-columns-graph')         
        ])                  
    
    else:
        return html.Div()
    
    
@callback(
    Output('editing-columns', 'columns'),
    Input('editing-columns-button', 'n_clicks'),
    State('editing-columns-name', 'value'),
    State('editing-columns', 'columns'))
def update_columns(n_clicks, value, existing_columns):
    if n_clicks > 0:
        existing_columns.append({
            'id': value, 'name': value,
            'renamable': True, 'deletable': True
        })
    return existing_columns


@callback(
    Output('editing-columns-graph', 'figure'),
    Input('editing-columns', 'data'),
    Input('editing-columns', 'columns'))
def display_output(rows, columns):
    return {
        'data': [{
            'type': 'heatmap',
            'z': [[row.get(c['id'], None) for c in columns] for row in rows],
            'x': [c['name'] for c in columns]
        }]
    }


# Right Column--------------------------------------------------------------------------------------------------------------------------------------------
## HeadLine 2 Callback
@callback(
    Output('sos2', 'children'),
    [Input('overview', 'n_clicks')]
)
def hdl2(n_clicks):
    if n_clicks is not None:
        return dbc.Row([            
            html.H1("Post-Survey Sentiment", style=hstyle2)    
                        
        ])           
    
    else:
        return html.Div()

## Drop down 2 Callback 
@callback(
    Output('drop2', 'children'),
    [Input('overview', 'n_clicks')]
)
def dropd2(n_clicks):
    if n_clicks is not None:
        return dbc.Row([            
            dcc.Dropdown(
                            ['Product', 'Campaign', 'Specific Survey/Questionnaire Question No. 1','Specific Survey/Questionnaire Question No. 2'],
                            searchable=False, placeholder="Choose an Observed",style=hstyle3)    
                        
        ])           
    
    else:
        return html.Div()

## Button 2 Callback
@callback(
    Output('butt2', 'children'),
    [Input('overview', 'n_clicks')]
)
def but2(n_clicks):
    if n_clicks is not None:
        return dbc.Row([
            html.Div([
                            html.Button('Anger', id='btn-1',style=hstyle4),
                            html.Button('Happiness', id='btn-2',style=hstyle4),
                            html.Button('Neutral', id='btn-3',style=hstyle4),
                            html.Button('Sadness', id='btn-4',style=hstyle4),
                            html.Button('Reset', id='btn-5',style=hstyle4),
                            html.Div(id='container')
                        ])                        
        ])           
    
    else:
        return html.Div()


@callback(Output('container', 'children'),
              Input('btn-1', 'n_clicks'),
              Input('btn-2', 'n_clicks'),
              Input('btn-3', 'n_clicks'),
              Input('btn-4', 'n_clicks'),Input('btn-5', 'n_clicks'))

def display3(btn1, btn2, btn3, btn4, btn5):
    button_id2 = ctx.triggered_id if not None else 'No clicks yet'
    
    return dbc.Row([html.Div([
        html.Table([
            html.Tr([html.Th('Anger (y0)',style=hstyle5),
                     html.Th('Happiness (y1)',style=hstyle5),
                     html.Th('Neutral (y2)',style=hstyle5),
                     html.Th('Sadness (y3)',style=hstyle5),
                     html.Th('Most Recent Click')]),
            html.Tr([html.Td(btn1 or 0,style=hstyle6), 
                     html.Td(btn2 or 0,style=hstyle6), 
                     html.Td(btn3 or 0,style=hstyle6), 
                     html.Td(btn4 or 0,style=hstyle6), 
                     html.Td(button_id2,style=hstyle6)])
        ])
    ])])

## Reset Button 1 Call back        
@callback(Output('btn-1', 'n_clicks'), Output('btn-2', 'n_clicks'), Output('btn-3', 'n_clicks'), Output('btn-4', 'n_clicks'),
              Input('btn-5', 'n_clicks'))
def update2(reset):
    return 0,0,0,0


# Table 2 Right
@callback(
    Output('tabl2', 'children'),
    [Input('overview', 'n_clicks')]
)
def tab2(n_clicks):
    if n_clicks is not None:
        return html.Div([html.Div([            
                    dcc.Input(
                        id='editing-columns-name2',
                        placeholder='Enter a column name...',
                        value='',
                        style={'padding': 10}
                    ),
                    html.Button('Add Column', id='editing-columns-button2', n_clicks=0)
                    ], style={'height': 50}),
                         
                dash_table.DataTable(
                    id='editing-columns2',
                    columns=[{
                        'name': 'Column {}'.format(i),
                        'id': 'column-{}'.format(i),
                        'deletable': True,
                        'renamable': True
                    } for i in range(1, 4)],
                    data=[
                        {'column-{}'.format(i): (j + (i-1)*4) for i in range(1, 4)}
                        for j in range(4)
                    ],
                    editable=True,export_format='xlsx',
                ),
                dcc.Graph(id='editing-columns-graph2')         
        ])                  
    
    else:
        return html.Div()

    
@callback(
    Output('editing-columns2', 'columns'),
    Input('editing-columns-button2', 'n_clicks'),
    State('editing-columns-name2', 'value'),
    State('editing-columns2', 'columns'))
def update_columns(n_clicks, value, existing_columns):
    if n_clicks > 0:
        existing_columns.append({
            'id': value, 'name': value,
            'renamable': True, 'deletable': True
        })
    return existing_columns


@callback(
    Output('editing-columns-graph2', 'figure'),
    Input('editing-columns2', 'data'),
    Input('editing-columns2', 'columns'))
def display_output(rows, columns):
    return {
        'data': [{
            'type': 'heatmap',
            'z': [[row.get(c['id'], None) for c in columns] for row in rows],
            'x': [c['name'] for c in columns]
        }]
    }


