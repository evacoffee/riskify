def moving_average_strategy(data, short_window=20, long_window=50):
    data = data.copy()
    data["Short_MA"] = (
        data["Close"].rolling(short_window).mean()
    )
    data["Long_MA"] = (
        data["Close"].rolling(long_window).mean()
    )
    data["Signal"] = 0
    data.loc[
        data["Short_MA"] > data["Long_MA"], "Signal"
    ] = 1
    data.loc[
        data["Short_MA"] < data["Long_MA"], "Signal"
    ] = 0
    return data

def momentum_strategy(data, window=20):
    data = data.copy()
    data["Momentum"] = data["Close"].pct_change(window)
    data["Signal"] = 0
    data.loc[
        data["Momentum"] > 0, "Signal"
    ] = 1
    return data
