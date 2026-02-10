from momentum.data import load_universe
from momentum.screener import get_candidates
from momentum.signaller import generate_signals, to_trade_events

from momentum.executor import execute


def main():
    # load in universe
    stocks = load_universe()
    # print(stocks)
    # go through the screening filter
    candidates = get_candidates(stocks)
    # print(candidates)
    signals, breakout_level = generate_signals(candidates, stocks)
    events = to_trade_events(signals, breakout_level)
    print(events)
    trade = execute(stocks, signals)
    # print(trade)


main()
