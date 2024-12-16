"""Defines functions to create graphs representing stock price changes and general
recommendations for selected stocks."""

import plotly.graph_objs as go
import pandas as pd


def create_price_graph(company_name, stock_df):
    """"Creates a graph based on the stock price change for the selected stock"""
    fig = go.Figure(data=go.Scatter(x=stock_df.index, y=stock_df["Close"], mode='lines+markers'))
    fig.update_layout(title=f'Monthly Stock Prices for {company_name}', xaxis_title='Date',
                      yaxis_title='Stock Price')
    return fig


def create_recommendation_graph(rec):
    """"Creates a general recommendation graph for the selected stock"""
    x_data = rec['period']
    y_data_strong_buy = rec['strongBuy']
    y_data_buy = rec['buy']
    y_data_hold = rec['hold']
    y_data_sell = rec['sell']
    y_data_strong_sell = rec['strongSell']

    fig = go.Figure(data=[
        go.Bar(name='Strong Buy', marker_color='green', x=x_data, y=y_data_strong_buy),
        go.Bar(name='Buy', marker_color='lightgreen', x=x_data, y=y_data_buy),
        go.Bar(name='Hold', marker_color='yellow', x=x_data, y=y_data_hold),
        go.Bar(name='Sell', marker_color='orange', x=x_data, y=y_data_sell),
        go.Bar(name='Strong Sell', marker_color='red', x=x_data, y=y_data_strong_sell)
    ])
    fig.update_layout(barmode='stack', title='Generalised recommendation on whether to buy,sell or hold '
                                             'onto a stock', xaxis_title='Month (0 represents this month)',
                      yaxis_title='Recommendation')
    return fig
