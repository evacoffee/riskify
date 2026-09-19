import yfinance as yf
import pandas as pd

def get_market_data(tickers, period="1y");
    """
    download adjusted historical closing prices for the requested tickers.
    """
    tickers = [ticker.upper]