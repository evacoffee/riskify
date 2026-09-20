import yfinance as yf
import pandas as pd

def get_market_data(tickers, period="1y"):
    """
    download adjusted historical closing prices for the requested tickers.
    """
    tickers = [ticker.upper().strip() for ticker in tickers]
    data = yf.download(
        tickers=tickers,
        period=period,
        auto_adjust=True,
        progress=False
    )
    if data.empty:
        raise ValueError("no market data was found.")
    #yf retiurns dif stuctues depends on number of tickers
    if isinstance(data.columns, pd.MultiIndex):
        if "Close" in data.columns.get_level_values(0):
            prices = data["Close"]
        else: 
            prices = data
    else: 
        if "Close" in data.columns:
            prices = data[["Close"]]
            prices.columns = [tickers[0]]
        else: 
            prices = data
    #maker sure colums are ticker names
    if len(tickers) == 1:
        if isinstance(prices, pd.Series):
            prices = prices.to_frame(name=tickers[0])
        else:
            prices.columns = [tickers[0]]
    prices = prices.dropna(how="all")
    #checks if needed tickers exist
    missing = [
        tickers
        for ticker in tickers
        if ticker not in prices.columns
    ]
    if missing:
        raise ValueError(
            "couldn't find market data for: 0" 
            + ",".joing(missing)
        )
    prices = prices[tickers].dropna()
    if prices.empty:
        raise ValueError("there isn't enough market data.")
    return prices
def calculate_returns(prices):
    """
    convert historical prices into daily percentage returns.
    """
    returns = prices.pct_change().dropna()
    if returns.empty:
        raise ValueError("not enough data to calculate rturns.")
    return returns