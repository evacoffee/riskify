import numpy as np

def run_backtest(data):
    data = data.copy()
    data["Market_Return"] = data["Close"].pct_change()
    data["Strategy_Return"] = (
        data["Market_Return"] * data["Signal"].shift(1)
    )
    data["Strategy_Value"] = (
        1 + data["Strategy_Return"]
    ).cumprod()
    data["Buy_Hold_Value"] = (
        1 + data["Market_Return"]
    ).cumprod()
    return data

def calculate_metrics(data):
    returns = data["Strategy_Return"].dropna()
    total_return = data["Strategy_Value"].iloc[-1] - 1
    volatility = returns.std() * np.sqrt(252)
    if volatility != 0:
        sharpe = (
            returns.mean() / returns.std()
        ) * np.sqrt(252)
    else:
        sharpe = 0
    drawdown = (
        data["Strategy_Value"]
        / data["Strategy_Value"].cummax()
    ) - 1
    max_drawdown = drawdown.min()
    return {
        "total_return": total_return,
        "volatility": volatility,
        "sharpe": sharpe,
        "max_drawdown": max_drawdown
    }