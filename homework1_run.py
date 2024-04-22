from typing import Optional

# install the required packages
# pip install dash dash-bootstrap-components pandas plotly
import subprocess
import sys

import dash
from dash import html, dcc, Input, Output, State
import pandas as pd
from decimal import Decimal, InvalidOperation

from utils.assets import *
from utils.calculator.mortgage.no_prepayment import FixedCouponRateMortgageCalculator
from utils.core import *
from plotly import graph_objs as go
from app_utils.layout_components import layout

from threading import Thread
import webbrowser

# Initialize the Dash app.
app = dash.Dash(__name__)

user_mortgage: Optional[Mortgage] = None
prev_user_loan_amount_input = None
prev_user_interest_rate_input = None
prev_user_loan_term_input = None

# Define the layout of the app.
app.layout = layout

app_url = ""


# Helper functions to calculate payments and amortization schedule.
def generate_amortization_schedule(mortgage: Mortgage):
    FixedCouponRateMortgageCalculator.calculate_lifecycle_payment_schedule(mortgage)
    periods = mortgage.payment_periods
    remaining_principals = [x.value for x in mortgage.remaining_principals]

    monthly_payment = mortgage.payment.value
    interest_payments = [x.value for x in mortgage.interest_payments]
    principal_payments = [x.value for x in mortgage.principal_payments]
    initial_principal = mortgage.principal.value

    begin_principals = [initial_principal] + remaining_principals[:-1]
    end_principals = remaining_principals

    cumulative_interest = 0
    schedule = []
    for i in range(periods):
        month = i + 1
        cumulative_interest += interest_payments[i]
        schedule.append([
            month,
            begin_principals[i],  # Begin Principal
            monthly_payment,  # Monthly Payment
            interest_payments[i],  # Interest Payment
            principal_payments[i],  # Principal Payment
            end_principals[i],  # End Principal
            cumulative_interest  # Cumulative Interest Paid (ensure this is calculated as intended)
        ])

    return schedule


# Callback to update the amortization schedule, WAL, and Monthly Payment.
@app.callback(
    [
        Output('table-container', 'children'),
        Output('wal-output', 'children'),
        Output('monthly-payment-output', 'children'),
    ],
    Input('calculate-button', 'n_clicks'),
    State('loan-amount', 'value'),
    State('annual-coupon', 'value'),
    State('loan-term', 'value'),
)
def update_output(n_clicks, loan_amount, interest_rate, loan_term):
    global user_mortgage
    if n_clicks < 1:
        # Don't update if the button hasn't been clicked
        return [html.Div(), html.Div(), html.Div()]
    refresh_user_mortgage(loan_amount, interest_rate, loan_term)
    FixedCouponRateMortgageCalculator.calculate_payment(user_mortgage)

    monthly_payment = user_mortgage.payment.value
    schedule = generate_amortization_schedule(user_mortgage)

    # Calculate WAL (Weighted Average Life)

    wal = FixedCouponRateMortgageCalculator.calculate_weighted_average_life(user_mortgage, 0).convert_to(TimeUnit.YEAR)
    wal_output = f"Weighted Average Life (WAL): {wal}"

    # Format monthly payment for display
    monthly_payment_output = f"Monthly Payment: ${monthly_payment:,.2f}"

    # Convert to DataFrame for the table
    df = pd.DataFrame(schedule, columns=[
        'Month', 'Begin Principal', 'Monthly Payment', 'Interest Payment',
        'Scheduled Principal Payment', 'End Principal', 'Cumulative Interest Paid'
    ])

    # Convert Decimal values to strings for display
    for col in ['Begin Principal', 'Monthly Payment', 'Interest Payment', 'Scheduled Principal Payment',
                'End Principal',
                'Cumulative Interest Paid']:
        df[col] = df[col].apply(lambda x: "${:,.2f}".format(x))

    # Return the updated table, WAL output, and Monthly Payment output
    return [
        dcc.Graph(
            id='payment-schedule-table',
            figure={
                'data': [
                    {
                        'type': 'table',
                        'header': {
                            'values': [['<b>Month</b>'], ['<b>Begin Principal</b>'], ['<b>Monthly Payment</b>'],
                                       ['<b>Interest Payment</b>'], ['<b>Scheduled Principal Payment</b>'],
                                       ['<b>End Principal</b>'], ['<b>Cumulative Interest Paid</b>']],
                            'align': 'center',
                            'fill': {'color': '#c1d9ff'},
                        },
                        'cells': {
                            'values': df.T.values,
                            'align': 'center',
                            'fill': {'color': ['#f5f5f5', 'white']},
                        }
                    }
                ],
                'layout': {
                    'height': '60vh',
                    'margin': {'l': 10, 'r': 10, 't': 10, 'b': 10}
                }
            },
            config={"displayModeBar": False},
            style={"height": "60vh"}
        ),
        html.Div(wal_output, style={'padding': 10, 'fontWeight': 'bold'}),
        html.Div(monthly_payment_output, style={'padding': 10, 'fontWeight': 'bold'}),
    ]


def refresh_user_mortgage(loan_amount, interest_rate, loan_term):
    global user_mortgage
    global prev_user_loan_amount_input
    global prev_user_interest_rate_input
    global prev_user_loan_term_input
    # check if any input has changed
    if loan_amount == prev_user_loan_amount_input and interest_rate == prev_user_interest_rate_input and loan_term == prev_user_loan_term_input:
        return
    prev_user_loan_amount_input = loan_amount
    prev_user_interest_rate_input = interest_rate
    prev_user_loan_term_input = loan_term

    try:
        loan_amount = Decimal(loan_amount.replace(',', ''))
        interest_rate = Decimal(interest_rate.replace(',', ''))
        loan_term = int(loan_term.replace(',', ''))
    except (InvalidOperation, ValueError):
        return [html.Div('Invalid input. Please enter the correct numeric values.'), html.Div(), html.Div()]

    principal = ValueFactory.create_value(value=loan_amount, currency_type=CurrencyType.USD)
    interest_rate = str(interest_rate / 100)
    rate = RateFactory.create_rate(value=interest_rate, rate_type=RateType.FIXED, frequency=FrequencyType.ANNUALLY)
    user_mortgage = MortgageFactory.create_mortgage(principal=principal, rate=rate,
                                                    maturity=Time(loan_term, TimeUnit.MONTH),
                                                    payment_frequency=FrequencyType.MONTHLY,
                                                    mortgage_type=MortgageType.FIXED_RATE)

    update_graph(0, prev_user_loan_amount_input, 1)
    update_scenario_analyses_graph(1, prev_user_loan_amount_input, prev_user_interest_rate_input,
                                   prev_user_loan_term_input)


def copy_set_helper_maturity(mortgage_to_copy: Mortgage, maturity: int):
    new_mortgage = mortgage_to_copy.copy()
    new_mortgage.set_maturity(maturity=Time(maturity, mortgage_to_copy.payment_frequency.get_time_unit()))
    return new_mortgage


@app.callback(
    Output('scenario-analyses-graph', 'figure'),
    Input('scenario-button', 'n_clicks'),
    State('loan-amount', 'value'),
    State('annual-coupon', 'value'),
    State('loan-term', 'value'),
    prevent_initial_call=True
)
def update_scenario_analyses_graph(n_clicks, loan_amount, interest_rate, loan_term):
    global user_mortgage
    if n_clicks < 1:
        # Don't update if the button hasn't been clicked
        return go.Figure()

    refresh_user_mortgage(loan_amount, interest_rate, loan_term)

    # Example: Calculate WAL for different maturities (this is simplified and should be replaced with actual logic)
    maturities = list(range(1, 361))  # Maturity from 1 to 360 months
    mortgages = [copy_set_helper_maturity(user_mortgage, maturity) for maturity in maturities]
    wal_values = [
        FixedCouponRateMortgageCalculator.calculate_weighted_average_life(loan, 0).convert_to(TimeUnit.MONTH).value
        for
        loan in mortgages]

    # Create the graph
    figure = {
        'data': [go.Scatter(x=maturities, y=wal_values, mode='lines', name='WAL')],
        'layout': go.Layout(
            title='WAL as a Function of Maturity (Initial Principal, Annual Coupon stay fixed from above)',
            xaxis={'title': 'Maturity (Months)'}, yaxis={'title': 'Value (Month)'})
    }
    return figure


def generate_accum_interest_data_list(loan_amount, interest_rates, loan_term):
    principal = ValueFactory.create_value(value=loan_amount, currency_type=CurrencyType.USD)
    mortgages = []
    for interest_rate in interest_rates:
        interest_rate = RateFactory.create_rate(value=interest_rate, rate_type=RateType.FIXED,
                                                frequency=FrequencyType.ANNUALLY)

        mortgage = MortgageFactory.create_mortgage(principal=principal, rate=interest_rate,
                                                   maturity=Time(loan_term, TimeUnit.YEAR),
                                                   payment_frequency=FrequencyType.MONTHLY,
                                                   mortgage_type=MortgageType.FIXED_RATE)
        mortgages.append(mortgage)

    mortgages = sorted(mortgages, key=lambda x: x.rate.value)

    accum_interest_data_list = []
    for mortgage in mortgages:
        FixedCouponRateMortgageCalculator.calculate_lifecycle_payment_schedule(mortgage)
        acc_interst_loan = sum([x.value for x in mortgage.interest_payments])
        accum_interest_data_list.append(acc_interst_loan)
    return accum_interest_data_list


# Generate coupon rates and maturities


@app.callback(
    Output('cumulative-interest-chart', 'figure'),
    [Input('cumulative-interest-chart', 'id'),
     State('loan-amount', 'value'),
     Input('scenario-button-interest-payment', 'n_clicks')]
)
def update_graph(_, loan_amount, n_clicks):
    if n_clicks < 1:
        # Don't update if the button hasn't been clicked
        return go.Figure()
    coupon_rates = ['0.04', '0.05', '0.06', '0.07', '0.08', '0.09']
    maturities = [10, 15, 30]
    data = []
    cum_interest_data = {}
    for maturity in maturities:
        cum_interest_data[maturity] = generate_accum_interest_data_list(loan_amount, coupon_rates, maturity)

    for maturity, cum_interest in cum_interest_data.items():
        data.append(go.Bar(x=coupon_rates, y=cum_interest, name=f"{maturity} Years"))

    layout = go.Layout(
        title='Cumulative Interest Paid by Coupon Rate and Maturity',
        xaxis=dict(title='Annual Coupon Rate'),
        yaxis=dict(title='Cumulative Interest Paid'),
        barmode='group'
    )

    return {'data': data, 'layout': layout}


import socket


def find_free_port():
    """Find a system-assigned free port."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))  # Bind to a free port provided by the host.
        return s.getsockname()[1]  # Return the port number assigned.


def open_browser(port):
    """Open a browser at a specified port."""
    webbrowser.open_new(f'http://127.0.0.1:{port}')


# Run the app.
if __name__ == '__main__':
    port = find_free_port()
    Thread(target=lambda: open_browser(port)).start()
    app.run_server(port=port)
