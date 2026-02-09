import pandas as pd
import numpy as np


def add_sma(universe, window=50):
    universe_clean = universe["Close"]
    sma_50 = universe_clean.rolling(window).mean()
    return sma_50


def liquidity_filter(universe):

    return


def trend_filter(universe):
    sma_50 = add_sma(universe)
    trending_stocks = universe[t]
    return


def get_candidates(universe):
    return


if __name__ == "__main__":
    print("test")
