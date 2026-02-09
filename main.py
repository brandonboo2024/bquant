from momentum.data import load_universe
from momentum.screener import get_candidates
from momentum.signaller import generate_signals

# from momentum.executor import execute


def main():
    # load in universe
    stocks = load_universe()
    print(stocks)
    # go through the screening filter
    candidates = get_candidates(stocks)
    print(candidates)
    signals = generate_signals(candidates, stocks)
    print(signals)
    # trade = execute(signals)


main()
