import numpy as np
import pandas as pd

TRADING_DAYS = 252
RISK_FREE_RATE = 0.04

def portfolio_returns(asset_returns, weights):
    """
    calcuate daily portfolio returns.
    """
    weights = np.array(weights)
    return asset_returns.dot(weights)

def expected_return(daily_returns):
    """
    annualized expected return.
    """
    daily_mean = daily_returns.mean()
    return (1 + daily_mean) ** TRADING_DAYS - 1

def volatility(daily_returns):
    """
    annualized portfolio volatility.
    """
    return daily_returns.std() * np.sqrt(TRADING_DAYS)

def sharpe_ratio(annual_return, annual_volatility):
    """
    annualized sharpe ratio.
    """
    if annual_volatility == 0:
        return 0
    return (
        annual_return - RISK_FREE_RATE
    ) / annual_volatility

def historical_var(daily_returns, portfolio_value):
    """
    historical 95% value at risk
    
    returns the estimated dollar loss at the 
    5th percentile of historical daily returns.
    """
    percentile = np.percentile(
        daily_returns,
        5
    )
    return abs(percentile * portfolio_value)

def maximum_drawdown(daily_returns):
    """
    calculate maximum portfolio drawdown
    """
    cumulative = (
        1 + daily_returns
    ).cumprod()
    running_max = cumulative.cummax()
    drawdown = (
        cumulative - running_max
    ) / running_max
    return drawdown.min()

def beta(asset_returns, market_returns):
    """
    calcualte portfolio beta against a market benchmark.
    """
    combined = pd.concat(
        [asset_returns, market_returns],
        axis=1
    ).dropna()
    if combined.shape[0] < 2:
        return 0
    portfolio = combined.iloc[:, 0]
    market = combined.iloc[:, 1]
    convariance = np.cov(
        portfolio,
        market
    )[0][1]
    market_variance = np.var(
        market,
        ddof=1
    )
    if market_variance == 0:
        return 0
    return convariance / market_variance

def correlation_matrix(asset_returns):
    """
    asset correlation matrix.
    """
    return asset_returns.corr()

def covariance_matrix(asset_returns):
    """
    annualized covariance matrix.
    """
    return asset_returns.cov() * TRADING_DAYS

def portfolio_history(daily_returns, starting_value):
    """
    convert daily returns into a portfolio value history.
    """
    cumulative = (
        1 + daily_returns
    ).cumprod()
    return cumulative * starting_value

def drawdown_series(daily_returns):
    """
    return the full drawdown series.
    """
    cumulative = (
        1 + daily_returns
    ).cumprod()
    running_max = cumulative.cummax()
    return (
        cumulative - running_max
    ) / running_max