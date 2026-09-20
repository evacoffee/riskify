def moving_average_strategy(data, short_window=20, long_window=50):

    data = data.copy()

    # Calculate moving averages
    data["Short_MA"] = data["Close"].rolling(short_window).mean()
    data["Long_MA"] = data["Close"].rolling(long_window).mean()

    # Start with no position
    data["Signal"] = 0

    # Buy when short moving average is above long moving average
    data.loc[
        data["Short_MA"] > data["Long_MA"],
        "Signal"
    ] = 1

    # Sell when short moving average is below long moving average
    data.loc[
        data["Short_MA"] < data["Long_MA"],
        "Signal"
    ] = 0

    return data