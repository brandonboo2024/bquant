def get_riser(universe, window=63, min=0.30):
    close = universe["Close"]
    # get df of stocks whose price increased 30%
    riser = (close / close.shift(window) - 1.0) >= min
    return riser


def get_peak(universe, window=63):
    close = universe["Close"]
    peak = close.rolling(window).max()
    return peak


def get_tread(universe, peak, min_days=4, max_days=40, max_retracement=0.25):
    close = universe["Close"]
    floor = (1.0 - max_retracement) * peak

    tread_any = None
    for n in range(min_days, max_days + 1):
        # take min value within the window
        min_n = close.rolling(n).min()
        # considered stabilised if still greater than the floor
        tread_n = min_n >= floor
        # considered true for any window 4 - 40
        tread_any = tread_n if tread_any is None else (tread_any | tread_n)

    return tread_any


def get_breakout(universe, peak):
    close = universe["Close"]
    # shift 1 to prevent lookahead
    breakout_level = peak.shift(1)
    breakout = close > breakout_level

    return breakout, breakout_level


def generate_signals(candidates, universe):
    riser = get_riser(universe)
    peak63 = get_peak(universe)
    tread = get_tread(universe, peak63)
    breakout, breakout_level = get_breakout(universe, peak63)

    # return boolean df of stocks whether they meet the criteria to be bought
    signal_bool = candidates & riser & tread.shift(1) & breakout

    return signal_bool, breakout_level


# to convert our current boolean dataframe into a log of trade events to occur
def to_trade_events(signal_bool, breakout_level):

    # turn df into a series, and give series name signal
    events = signal_bool.stack().rename("signal").reset_index()
    # keep entries where a trade is supposed to happen
    events = events[events["signal"]].copy()
    # for format
    events["side"] = "BUY"

    if breakout_level is not None:
        # turn breakout level into a series as well
        lvl = breakout_level.stack().rename("breakout_level").reset_index()
        # merge the breakout_level values into events df
        events = events.merge(lvl, on=["Date", "Ticker"], how="left")

    return events.sort_values(["Date", "Ticker"]).reset_index(drop=True)


if __name__ == "__main__":
    print()
