"""Creates a Dash application for a Stock Market Dashboard, allowing users to input a company name and date range to
display monthly stock prices or recommendations, utilizing an API file and graphs file to perform functions."""

import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
from datetime import date
import yfinance as yf
from stock_API import fetch_ticker_symbol, fetch_monthly_data, stock_rec
from stock_graphs import create_price_graph, create_recommendation_graph

# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])

# Define reusable styles
label_style = {'margin-right': '10px', 'text-align': 'center'}
input_style = {'margin-right': '10px', 'margin-top': '20px', 'text-align': 'left'}
button_style = {'margin-right': '10px', 'text-align': 'left'}
output_style = {'text-align': 'center', 'margin-bottom': '10px', 'margin-top': '40px'}
tab_style = {'margin-top': '20px'}

# Define layout
app.layout = html.Div([
    html.Div([
        html.H1('Stock Market Dashboard', style={'text-align': 'center', 'margin-top': '20px',
                                                 'margin-bottom': '20px'}),
    ]),
    html.Div([
        html.Label('Enter Company Name:', style=label_style),
        dcc.Input(
            id='company-input',
            type='text',
            value='',
            placeholder='Enter company name...',
            style=input_style
        ),
        html.Button('Get Ticker', id='submit-button', n_clicks=0, style=button_style),
        html.Div(id='ticker-output', style=output_style),
    ], style={'text-align': 'center', 'margin-bottom': '20px', 'margin-top': '20px'}),
    html.Div([
        html.Label('Enter the date range:', style=label_style),
        html.Div(
            dcc.DatePickerRange(
                id='investment-date-picker-range',
                min_date_allowed=date(2019, 3, 1),
                max_date_allowed=date(2024, 2, 1),
                initial_visible_month=date(2019, 3, 1),
                end_date=date(2024, 2, 1),
                start_date_placeholder_text="Start Period",
                end_date_placeholder_text="End Period",
                calendar_orientation='vertical',
                style=input_style,
            ),
            style={'display': 'inline-block', 'text-align': 'center'}
        ),
        html.Div(id='output-container-date-picker-range')
    ]),
    dcc.Tabs(id="graphs", value='price-graph', children=[
        dcc.Tab(label='Monthly Stock Prices', value='price-graph', style=tab_style),
        dcc.Tab(label='Recommendations', value='rec-graph', style=tab_style),
    ]),
    html.Div(id='graphs-display', style={'margin-top': '20px'})
])


# Callback to update ticker info
@app.callback(
    Output('ticker-output', 'children'),
    [Input('submit-button', 'n_clicks')],
    [State('company-input', 'value')]
)
def update_ticker_info(n_clicks, company_name):
    """Fetches the ticker information of a company based on input"""
    if n_clicks > 0 and company_name:
        try:
            ticker_symbol = fetch_ticker_symbol(company_name)
            ticker = yf.Ticker(ticker_symbol)
            company_name = ticker.info.get('longName', 'N/A')
            sector = ticker.info.get('sector', 'N/A')
            industry = ticker.info.get('industry', 'N/A')
            return html.Div([
                html.H3(f"Company: {company_name}"),
                html.P(f"Ticker Symbol: {ticker_symbol}"),
                html.P(f"Sector: {sector}"),
                html.P(f"Industry: {industry}")
            ])
        except Exception as e:
            return html.Div(f"Error fetching ticker information: {str(e)}")
    else:
        return ''


# Callback to update monthly stock prices or recommendations based on selected tab
@app.callback(
    Output('graphs-display', 'children'),
    [Input('graphs', 'value')],
    [State('company-input', 'value'),
     State('investment-date-picker-range', 'start_date'),
     State('investment-date-picker-range', 'end_date')]
)
def update_content(tab, company_name, start_date, end_date):
    """Updates the dashboard with price change and recommendation graphs"""
    if company_name and start_date and end_date:
        try:
            ticker = fetch_ticker_symbol(company_name)
            if tab == 'price-graph':
                stock_df = fetch_monthly_data(ticker)
                stock_df = pd.DataFrame(stock_df, columns=["Date", "Close"])
                stock_df["Date"] = pd.to_datetime(stock_df["Date"])
                stock_df.set_index("Date", inplace=True)
                stock_df["Price Difference"] = stock_df["Close"].diff()
                stock_df.dropna(inplace=True)

                # Convert start_date and end_date to datetime objects
                start_date = pd.to_datetime(start_date)
                end_date = pd.to_datetime(end_date)

                # Slice the DataFrame based on the date range
                position_df = stock_df.loc[start_date:end_date]

                fig = create_price_graph(company_name, position_df)
                return dcc.Graph(figure=fig)

            elif tab == 'rec-graph':
                rec = stock_rec(ticker)
                fig = create_recommendation_graph(rec)
                return dcc.Graph(figure=fig)

        except Exception as e:
            return html.Div(f'Error: {str(e)}')
    else:
        return html.Div("")


if __name__ == '__main__':
    app.run_server(debug=True)
