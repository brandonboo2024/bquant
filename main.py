from momentum.data import load_universe
from momentum.screener import get_candidates
from momentum.signaller import generate_signals, to_trade_events
from momentum.executor import execute
from pathlib import Path


def main():
    # load in universe
    stocks = load_universe()
    candidates = get_candidates(stocks)
    signals, breakout_level = generate_signals(candidates, stocks)
    events = to_trade_events(signals, breakout_level)
    trade = execute(stocks, signals)

    print(events.head(10))
    print(trade.head(10))
    print("Total PnL:", trade["pnl"].sum())

    # csv outputs
    out_dir = Path("outputs")
    print(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    events.to_csv(out_dir / "events.csv", index=False)
    events.to_csv(out_dir / "trades.csv", index=False)

    if not trade.empty:
        summary = (
            trade.groupby("ticker")
            .agg(
                num_trades=("ticker", "count"),
                total_pnl=("pnl", "sum"),
                avg_return=("return", "mean"),
            )
            .reset_index()
        )
        summary.to_csv(out_dir / "trade_summary_by_ticker.csv", index=False)

    print(f"csvs saved to {out_dir}")


main()
