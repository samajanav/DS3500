"""Defines functions to fetch monthly closing stock prices for the last 5 years, fetch ticker
symbols for companies, and retrieve stock recommendations."""

import yfinance as yf
import requests
from datetime import date


def fetch_monthly_data(company_name):
    """
    Fetch monthly closing stock prices for the last 5 years for a given company.
    """
    stock_data = yf.download(company_name, period="5y", interval="1mo")
    closing_prices = stock_data["Close"].reset_index().values.tolist()
    closing_prices_last_5_years = closing_prices[-60:]
    return closing_prices_last_5_years


def fetch_ticker_symbol(ticker):
    """
    Fetch the ticker symbol for a given company ticker.
    """
    yfinance_url = "https://query2.finance.yahoo.com/v1/finance/search"
    params = {"q": ticker, "quotes_count": 1, "region": "US"}
    headers = {'User-Agent': 'Mozilla/5.0'}
    res = requests.get(url=yfinance_url, params=params, headers=headers)
    if res.status_code == 200:
        data = res.json()
        if 'quotes' in data and len(data['quotes']) > 0:
            return data['quotes'][0]['symbol']
    raise ValueError("Failed to fetch ticker symbol.")


def stock_rec(ticker):
    """Returns stock recommendations for the given ticker"""
    stock = yf.Ticker(ticker)
    rec = stock.recommendations
    return rec
