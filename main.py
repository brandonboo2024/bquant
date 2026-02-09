from momentum.data import load_universe
from momentum.screener import get_candidates

# from momentum.signaller import generate_signals
# from momentum.executor import execute

print("hello world!")


def main():
    stocks = load_universe()
    print(stocks)
    candidates = get_candidates(stocks)
    print(candidates)
    # signals = generate_signals(candidates)
    # trade = execute(signals)


main()
