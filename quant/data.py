import yfinance as yf

def get_data(ticker, start, end):
    data = yf.download(
        ticker, start=start, end=end, auto_adjust=True
    )

    if data.empty: 
        raise ValueError("no market data found.")
    return data