import pandas as pd
import math


def get_sma(universe, window=10):
    close = universe["Close"]
    return close.rolling(window).mean()


# calculate average true range
def get_atr(universe, window=14):
    high = universe["High"]
    low = universe["Low"]
    close = universe["Close"]
    prev_close = close.shift(1)

    # turn the following dataframes into a series
    true_range = (
        pd.DataFrame(
            {
                "range1": (high - low).stack(),
                "range2": (high - prev_close).abs().stack(),
                "range3": (low - prev_close).abs().stack(),
            }
        )
        .max(axis=1)
        .unstack()
    )

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
    opening = universe["Open"]
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
                entry_price = float(opening[ticker].iloc[i + 1])
                stop_price = float(low[ticker].iloc[i])  # low of signal day

                # sanity checks
                if math.isnan(entry_price) or math.isnan(stop_price):
                    continue
                if entry_price <= stop_price:
                    continue

                atr_f = float(atr[ticker].iloc[i])

                if math.isnan(atr_f) or atr_f <= 0:
                    continue

                # stop distance
                if (entry_price - stop_price) > atr_f:
                    continue

                risk_per_share = entry_price - stop_price
                qty = int(risk_amt // risk_per_share)
                if qty <= 0:
                    continue

                # if reach here, passes checks and call into position
                in_pos = True
                trades.append(
                    {
                        "ticker": ticker,
                        "entry_date": next_date,  # use current day for next day position
                        "entry_price": entry_price,
                        "stop_price": stop_price,
                        "qty": qty,
                    }
                )
            else:
                # set exit
                c = float(close[ticker].iloc[i])
                s = float(sma10[ticker].iloc[i])
                if math.isnan(c) or math.isnan(s):
                    continue

                if c < s:
                    exit_price = float(opening[ticker].iloc[i + 1])

                    trades[-1].update(
                        {
                            "exit_date": next_date,
                            "exit_price": exit_price,
                            "pnl": (exit_price - entry_price) * qty,
                            "return": (exit_price - entry_price) / entry_price,
                        }
                    )

                    in_pos = False
                    entry_price = None
                    qty = 0

        if in_pos:
            last_close = float(close[ticker].iloc[-1])
            trades[-1].update(
                {
                    "exit_date": signal.index[-1],
                    "exit_price": last_close,
                    "pnl": (last_close - entry_price) * qty,
                    "return": (last_close - entry_price) / entry_price,
                }
            )

    return pd.DataFrame(trades)


if __name__ == "__main__":
    print("")
