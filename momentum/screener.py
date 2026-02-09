# get SMA_50 for all stocks
def get_sma(universe, window=50):
    universe_close = universe["Close"]
    sma_50 = universe_close.rolling(window).mean()
    return sma_50


# get liquidity stats for stocks
def get_liquidity(universe, window=50):
    volume = universe["Volume"]
    vol_50 = volume.rolling(window).mean()
    return vol_50


# returns a dataframe with boolean values on whether a stock passes the screening on each day
def get_candidates(universe):
    sma_50 = get_sma(universe)
    vol_50 = get_liquidity(universe)
    # do screening
    candidates = (
        (universe["Close"] >= 3.0) & (vol_50 >= 300000) & (universe["Close"] > sma_50)
    )
    return candidates


if __name__ == "__main__":
    print("test")
