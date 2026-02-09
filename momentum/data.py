import yfinance as yf
import datetime as dt

# initialise universe for 20 liquid stocks
# chose from different industries for diversity


tickers = [
    "AAPL",
    "MSFT",
    "NVDA",
    "AMZN",
    "GOOGL",
    "META",
    "BRK-B",
    "LLY",
    "TSLA",
    "AVGO",
    "JPM",
    "V",
    "MA",
    "XOM",
    "UNH",
    "COST",
    "PG",
    "JNJ",
    "HD",
    "MRK",
]


def load_universe():
    # download data using yfinance
    # historical data is from 1/1/2015 - 12/31/2025
    universe = yf.download(
        tickers,
        start=dt.datetime(2015, 1, 1),
        end=dt.datetime(2025, 12, 31),
    )
    # print(universe)
    # use close price to prevent lookahead bias
    return universe


if __name__ == "__main__":
    df = load_universe()
