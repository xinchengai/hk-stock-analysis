# HK Stock Analysis Skill

An OpenClaw/Codex skill for Hong Kong stock research briefs. It analyzes HK-listed stocks only, combines market data with current announcements/news, and includes a mandatory fact-check gate for event-driven situations such as offers, resumptions, placings, and large price moves.

This skill is designed for research reference. It does not provide personalized investment advice or direct trading instructions.

## What It Does

- Accepts Hong Kong tickers such as `HK00700`, `00700.HK`, and `00700`.
- Resolves Chinese company names by searching for the HK ticker first.
- Rejects non-HK tickers such as `AAPL`, `TSLA`, `600519`, or `000001.SZ`.
- Fetches HK market data through a provider fallback chain:
  - `efinance`
  - `akshare`
  - `yfinance`
- Produces a structured Hong Kong stock research brief covering:
  - price and valuation snapshot
  - technical view
  - HKEX announcements and company news
  - market and sector context
  - evidence weighting
  - observation checklist
- Requires a fact-check section before finalizing the report.

## Fact-Check Gate

The skill includes `references/fact-check-rules.md` to reduce common mistakes in Hong Kong event-driven stocks.

It requires the agent to:

- Prefer HKEX/company announcements for material events.
- Recalculate premium/discount:

  ```text
  (offer_or_transaction_price - reference_price) / reference_price * 100
  ```

- Use `折让` when the result is negative and `溢价` only when it is positive.
- Recalculate price moves:

  ```text
  (current_or_close_price - previous_close) / previous_close * 100
  ```

- Distinguish intraday data from closing data.
- Use annual/interim report titles for fiscal-year wording.
- Label unreconciled valuation figures as third-party source figures.
- Reduce the weight of technical indicators when a stock is driven by offers, resumptions, placings, acquisitions, disposals, or very large one-day moves.

Example check:

```text
8.323 vs 30.00 = (8.323 - 30.00) / 30.00 = -72.26%
```

Correct wording: `较30.00港元折让约72.26%`.

## Installation

Copy this repository into one of the skill locations supported by your agent runtime.

Project-local installation:

```bash
mkdir -p skills
git clone https://github.com/xinchengai/hk-stock-analysis.git skills/hk-stock-analysis
```

Global OpenClaw-style installation:

```bash
mkdir -p ~/.openclaw/skills
git clone https://github.com/xinchengai/hk-stock-analysis.git ~/.openclaw/skills/hk-stock-analysis
```

If your runtime supports a built-in skill installer, install the repository using that mechanism instead.

## Optional Data Dependencies

The skill can be loaded without Python dependencies. The bundled data script needs at least one market-data provider package to fetch live data.

Recommended:

```bash
python3 -m pip install efinance akshare yfinance pandas requests
```

If no provider package is available, the script returns structured JSON with an installation hint instead of crashing.

## Usage

Example prompts:

```text
分析 HK00700
```

```text
分析 00700.HK，重点看公告和技术面
```

```text
分析腾讯控股这支港股
```

For event-driven stocks, ask for explicit verification:

```text
分析 01657.HK，并核对要约价、折让/溢价、今日涨跌幅和公告来源
```

## Files

```text
SKILL.md
agents/openai.yaml
references/fact-check-rules.md
references/output-format-template.md
references/stock_data_fetcher.py
```

## Validation

Run a syntax check for the bundled script:

```bash
python3 -m py_compile references/stock_data_fetcher.py
```

Test unsupported tickers:

```bash
python3 references/stock_data_fetcher.py AAPL
python3 references/stock_data_fetcher.py 600519
```

Both should return an `unsupported_ticker` JSON response.

Test HK ticker normalization:

```bash
python3 references/stock_data_fetcher.py HK00700 --days 30
python3 references/stock_data_fetcher.py 00700.HK --days 30
python3 references/stock_data_fetcher.py 00700 --days 30
```

All valid forms normalize to `HK00700`.

## Disclaimer

This skill is for research reference only. It does not provide financial advice, personalized investment recommendations, trading instructions, position sizing, or risk-management instructions. Always verify figures against primary sources such as HKEX announcements and consult a licensed professional for investment decisions.
