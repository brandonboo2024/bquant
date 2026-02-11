# Systematic Momentum Trading System 

This repository implements a simple end-of-day (EOD) systematic momentum strategy in Python, split into four core components:

- **Data/Universe**: Downloads data via yfinance API for 20 highly liquid US stocks
- **Screener**: liquidity + trend filter
- **Signaller**: Riser + Tread + Breakout entry signal
- **Executor**: risk-based position sizing + SMA(10) trailing-stop exit

The goal is to find stocks that:
1) made a strong move recently (**Riser**),
2) consolidated without deep retracement (**Tread**),
3) then break above the prior peak (**Breakout**).

## Project Structure
├── flake.lock
├── flake.nix
├── LICENSE
├── main.py
├── Makefile
├── momentum
│   ├── data.py
│   ├── executor.py
│   ├── screener.py
│   └── signaller.py
├── pyproject.toml
├── README.md
└── uv.lock

**Core Components**:
- `data.py` — loads historical OHLCV data for a fixed universe of 20 US large caps using `yfinance`.
- `screener.py` — filters to liquid, trending stocks (price, avg volume, above SMA(50)).
- `signaller.py` — generates buy signals using:
  - Riser: +30% over ~63 trading days
  - Tread: stabilizes 4–40 days without >25% retracement from peak
  - Breakout: close > prior peak (shifted to avoid lookahead)
- `executor.py` — simulates trades:
  - entry next-day open after signal
  - stop = low of signal day
  - constraint: stop distance ≤ 1.0 × ATR(14)
  - risk sizing: 2% of capital
  - exit when close < SMA(10), at next-day open

## Output
When the program is run, it will:
1. Download data for the universe via `yfinance`
2. Filters candidates using screener rules
3. Generates breakout signals
4. Simulates trades using executor rules ($100,000 capital)

It will output:
- Preview of detected signal events
- Preview of executed trades
- Total PnL over the backtesting period (2015-2025)

It will additional export CSVs under `outputs/`
- `events.csv` - all signal events generated
- `trades.csv` - executed trades with PnL and returns
- `trade_summary_by_ticker` - per-ticker aggregates (count, total PnL, avg returns)

## Setup

### Nix Flake (Recommended if using Nix)

From repo root:
```bash
nix develop
```

### Using `uv`
```bash
pip install uv
uv sync
```

### Manual (`pip`)
```bash
pip install requirements.txt
```

## Running the program

### Makefile
```
make
```

### With `uv`
```
uv run python main.py
```

### manual
```
python3 main.py
```


