#show title: set align(center)
#show title: set text(size: 20pt)

#set page(
  margin: (
    top: 1cm,
    bottom: 1cm,
    x: 1cm,
  ),
)

#title[
  Momentum Trading System in Python
]

#line(length: 100%)

= API / Data Log

== Data Source
*Yahoo Finance* accessed via the Python library `yfinance`.

=== Why chosen
- free and fast to prototype
- supports OHLCV history for US equities
- easy to pull multiple tickers in one call
- sufficient for an EOD technical test / backtest prototype

=== What data is used
- Daily OHLCV bars: `Open`, `High`, `Low`, `Close`, `Volume`
- Date range: 2015-01-01 to 2025-12-31
- Universe: fixed list of 20 large, liquid US stocks

== Known limitations / issues

=== 1. Rate limiting / throttling
Yahoo Finance is not an official public API; requests may be throttled or fail intermittently.

=== 2. Data quality / vendor differences
Yahoo data can differ from vendor-grade datasets (cleaning rules, corporate actions handling, etc.).

#line(length: 100%)

= System Review

== What is good?

=== 1. Clear modular architecture (SRP Approach)
- The code is separated into *Data*, *Screener*, *Signaller*, and *Executor*. Each module has a single responsibility and can be tested independently.
  - Separation makes it easy to extend the system (e.g. new signals, new exits, etc.) without touching unrelated code

=== 2. Lookahead-bias awareness
- Breakout uses a shifted peak (`peak.shift(1)`), so today’s signal cannot “see” today’s peak.
- Entry/exit are executed at the next-day open after a condition is observed.

=== 3. Readability and maintainability (Pythonic Style)
- Implementation prioritised clarity, trading rules was expressed in code clearly using reliable and fast libraries
- Screening and signal generation are mostly vectorised using Pandas, reducing boilerplate loops and makes logic easier to see

=== 4. Appropriate simplicity for scope
- Given the task constraints, the design remains lightweight and not over-engineered
- Backtest is fast to fun, easy to modify and suitable as a reference implementation for the given task

== Trade-offs made for the deadline
- used `yfinance` for speed instead of building a full data pipeline
- ignores slippage/commissions and assumes fills at next open
- stop-loss is not simulated as an intraday trigger (stop is used for sizing/validation only)
- portfolio constraints (max positions, correlation/risk budgeting) are not included

== What can be improved?

=== 1. More realistic execution model
- add transaction costs (spread + commissions)
- simulate stop-loss execution intraday (gap logic / stop fills)
- handle partial fills / market impact assumptions

=== 2. More robust data layer
- cache downloaded data to disk (CSV/parquet) to avoid repeated calls
  - Could also be downloaded to a database like PostGreSQL for more robust database management
- explicitly handle corporate actions and adjustments
- validate data (missing bars, NaNs, unexpected ticker issues)

=== 3. Testing and reproducibility
- unit tests for SMA/ATR correctness
- unit tests for Riser/Tread/Breakout logic and lookahead checks
- pin dependency versions and add a deterministic run mode

== Latency bottleneck + optimization

=== 1. Primary bottleneck: data download (`yfinance`)
- The slowest step in the program is downloading data from the `yfinance` API
  - Due to network latency, rate limiting etc.
  - When the data scale / universe grows or with constant real-time updating, the runtime will reduce drastically

=== 2. Secondary bottleneck: Executor component loop / DataFrame Indexing
- The `executor.py` component uses Python-level loops with `.iloc` access
- Not a very efficient way to traverse the data

=== Optimisation 1: Caching
- We can cache the data from `yfinance` to disk as a CSV or to a database like PostGreSQL
- On each run, only fetch missing dates or refresh latest *N* trading days
- Add a refresh mode:
  - default: read from cache
  - optional: re-fetch latest *N* days and update cache

=== Optimisation 2: More efficient operations in Python
- Convert key per-ticker series to Numpy arrays and operate on the arrays
- Reduce python loops, or use `numba` library for JIT compilation and accelerate the per-ticker simulations
- Avoid `.iloc` calls unless necesssary

== What is lacking for live trading?

The most critical missing component is an *Order Management / Live Execution & Monitoring* layer:
- broker connectivity
- live position reconciliation
- order state tracking (submitted, partially filled, cancelled, rejected)
- monitoring + alerts for failures (data outage, rejected orders, desync)

== Major failure scenario if deployed live
- *Stale or missing data leading to incorrect orders*: without monitoring and safety checks, the system could repeatedly place wrong orders (false breakouts, late exits, incorrect sizing).

