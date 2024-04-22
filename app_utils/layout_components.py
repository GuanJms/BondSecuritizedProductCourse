from dash import html, dcc, Input, Output, State
from app_utils import styles_dictionary

# layout = html.Div([
#     html.H1('Mortgage Payment Schedule', style={'textAlign': 'center'}),
#
#     # User input fields for loan parameters.
#     html.Div([
#         html.Div([
#             html.Label('Initial Principal ($):'),
#             dcc.Input(id='loan-amount', type='text', value='100000', style=styles_dictionary['input']),
#         ], style={'padding': 10, 'flex': 1}),
#
#         html.Div([
#             html.Label('Annual Coupon (%) :'),
#             dcc.Input(id='annual-coupon', type='text', value='4.0', style=styles_dictionary['input']),
#         ], style={'padding': 10, 'flex': 1}),
#
#         html.Div([
#             html.Label('Maturity (months):'),
#             dcc.Input(id='loan-term', type='text', value='180', style=styles_dictionary['input']),
#         ], style={'padding': 10, 'flex': 1}),
#
#         html.Button('Calculate', id='calculate-button', n_clicks=0, style=styles_dictionary['button']),
#     ], style={'display': 'flex'}),
#
#     # Output boxes for WAL and Monthly Payment.
#     html.Div(id='output-container', children=[
#         html.Div(id='wal-output', style={'padding': 10}),
#         html.Div(id='monthly-payment-output', style={'padding': 10})
#     ]),
#
#     # Placeholder for the data table.
#     html.Div(id='table-container'),
#     # Placeholder for the WAL graph.
#     html.H2('Scenario Analyses(Part1)', style={'textAlign': 'center'}),
#     html.H3('WAL(at time 0) vs Maturity', style={'textAlign': 'center'}),
#     # Add a button to trigger the calculation for the scenario analyses graph
#     html.Button('Generate Scenario Analyses Graph - Part 1', id='scenario-button', n_clicks=0,
#                 style=styles_dictionary['button']),
#     dcc.Graph(id='scenario-analyses-graph'),
#     html.H2('Scenario Analyses(Part2)', style={'textAlign': 'center'}),
#     html.H3(
#         'Accumulative Interest Payment vs Annual Coupon Rate Across Different Maturities',
#         style={'textAlign': 'center'}),
#     html.Button('Generate Scenario Analyses Graph -Part 2', id='scenario-button-interest-payment', n_clicks=0,
#                 style=styles_dictionary['button']),
#     dcc.Graph(id='cumulative-interest-chart')
# ])


layout = html.Div([
    html.H1('Mortgage Payment Schedule', style=styles_dictionary['header']),
    html.Div([
        html.Div([
            html.Label('Initial Principal ($):', style=styles_dictionary['label']),
            dcc.Input(id='loan-amount', type='text', value='100000', style=styles_dictionary['input']),
        ], style=styles_dictionary['flexItem']),

        html.Div([
            html.Label('Annual Coupon (%):', style=styles_dictionary['label']),
            dcc.Input(id='annual-coupon', type='text', value='4.0', style=styles_dictionary['input']),
        ], style=styles_dictionary['flexItem']),

        html.Div([
            html.Label('Maturity (months):', style=styles_dictionary['label']),
            dcc.Input(id='loan-term', type='text', value='180', style=styles_dictionary['input']),
        ], style=styles_dictionary['flexItem']),

        html.Button('Calculate', id='calculate-button', n_clicks=0, style=styles_dictionary['button']),
    ], style=styles_dictionary['flexContainer']),

    html.Div(id='output-container', children=[
        html.Div(id='wal-output', style=styles_dictionary['output']),
        html.Div(id='monthly-payment-output', style=styles_dictionary['output'])
    ], style=styles_dictionary['div']),

    html.Div(id='table-container', style=styles_dictionary['div']),

    html.H2('Scenario Analyses (Part 1)', style=styles_dictionary['H2']),
    html.H3('WAL (at time 0) vs Maturity', style=styles_dictionary['subHeader']),

    html.Button('Generate Scenario Analyses Graph - Part 1', id='scenario-button', n_clicks=0, style=styles_dictionary['button']),

    dcc.Graph(id='scenario-analyses-graph', style=styles_dictionary['div']),

    html.H2('Scenario Analyses (Part 2)', style=styles_dictionary['H2']),
    html.H3('Accumulative Interest Payment vs Annual Coupon Rate Across Different Maturities', style=styles_dictionary['subHeader']),

    html.Button('Generate Scenario Analyses Graph - Part 2', id='scenario-button-interest-payment', n_clicks=0, style=styles_dictionary['button']),

    dcc.Graph(id='cumulative-interest-chart', style=styles_dictionary['div']),
], style=styles_dictionary['container'])
