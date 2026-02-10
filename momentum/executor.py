import pandas as pd


def get_sma(universe, window=10):
    close = universe["Close"]
    return close.rolling(window).mean()


# calculate average true range
def get_atr(universe, window=14):
    high = universe["High"]
    low = universe["Low"]
    close = universe["Close"]
    prev_close = close.shift(1)

    range1 = high - low
    range2 = (high - prev_close).abs()
    range3 = (low - prev_close).abs()

    true_range = pd.concat([range1, range2, range3], axis=1).max(axis=1)
    atr = true_range.rolling(window).mean()
    return atr


"""
executor component
- stop-loss = low of signal day
- stop distance <= ATR(14)
- risk of up to 0.02
- exit when close < sma10

"""


def execute(universe, signals_bool, capital=100_000.0, risk=0.02):
    open = universe["Open"]
    low = universe["Low"]
    close = universe["Close"]

    atr = get_atr(universe)
    sma10 = get_sma(universe)
    print("printing atr")
    print(atr)

    risk_amt = capital * risk

    trades = []
    tickers = signals_bool.columns

    # implement for every stock
    for ticker in tickers:
        in_pos = False
        entry_price = None
        qty = 0
        # data wrangling, fill up any potential missing values
        signal = signals_bool[ticker].fillna(False)

        for i in range(len(signal) - 1):
            next_date = signal.index[i + 1]
            # check if in position
            if not in_pos:
                # check if
                if not signal.iloc[i]:
                    continue

                # if here, we are in position
                entry_price = float(open)

    return
