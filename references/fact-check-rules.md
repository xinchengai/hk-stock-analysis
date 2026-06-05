# HK Stock Fact Check Rules

Use these rules before writing a Hong Kong stock research brief. These rules are mandatory for event-driven stocks and for any report containing offer, placing, acquisition, disposal, resumption, financial, valuation, or large price-move claims.

## Source Priority

1. HKEX/company announcements and annual/interim reports.
2. Exchange or official company websites.
3. Reputable financial data pages.
4. News summaries and market commentary.

When sources conflict, prefer HKEX/company announcements for legal events and financial statement figures. Use news only as context unless it directly quotes the announcement.

## Premium and Discount

Formula:

```text
(offer_or_transaction_price - reference_price) / reference_price * 100
```

Rules:

- Positive result = `溢价`.
- Negative result = `折让`.
- Never infer the direction from wording in a news article without recalculating.
- Always name the reference price, such as `最后交易日收市价`, `停牌前收市价`, `前5个交易日平均收市价`, or `每股资产净值`.

Example:

```text
8.323 vs 30.00 = (8.323 - 30.00) / 30.00 = -72.26%
```

Correct wording: `较30.00港元折让约72.26%`.

Incorrect wording: `较30.00港元溢价72.26%`.

## Price Change

Formula:

```text
(current_or_close_price - previous_close) / previous_close * 100
```

Rules:

- If the quote was captured before market close, call it `盘中价`, `盘中涨幅`, or `截至 HH:MM`.
- Only use `收盘价` or `收盘涨幅` after the source explicitly shows final close data or the market is closed and the source identifies the figure as close.
- If high/low/open/current values imply inconsistent percentages, report the inconsistency and prefer source-labeled last price plus previous close.

Example:

```text
61.60 vs 30.00 = (61.60 - 30.00) / 30.00 = 105.33%
```

## Announcements and Event-Driven Stocks

For offers, subscriptions, placings, buybacks, dividends, index inclusion/removal, Stock Connect inclusion/removal, resumption, acquisitions, disposals, winding-up, liquidation, share consolidation, or very large one-day moves:

- Find the HKEX announcement title, date, and link where possible.
- Distinguish sale share price, offer price, subscription price, placing price, market price, and previous close.
- Do not call a control transaction price a market-support level unless it is close to current market price and the source supports that interpretation.
- State that technical indicators have reduced reliability when the price action is dominated by an event or when liquidity is extremely thin.
- For buybacks, distinguish announced mandate, actual repurchase date, repurchase price range, number of shares, and cumulative repurchase amount.
- For dividends, distinguish final, interim, special, ex-dividend date, record date, and payment date.
- For index or Stock Connect changes, identify the effective date and whether the stock is added or removed.

## Financial Year and Financial Data

Rules:

- Use the annual/interim report title for fiscal-period wording.
- Do not infer fiscal year from publication date.
- Keep units exactly clear: HKD, RMB, HK$ thousand, HK$ million, shares, or percent.
- For cash flow, distinguish `cash used in operations`, `net cash used in operating activities`, and free cash flow.
- If figures come from a table, preserve the source period and unit in the report.

Example wording:

```text
FY2025 means `截至2025年4月30日止年度` if that is the HKEX annual report title.
```

## Valuation

Rules:

- PE is not meaningful when trailing earnings are negative. Write `PE为负，不具备常规估值意义`.
- PB can be recalculated as `market price / NAV per share` if NAV per share is available.
- Market cap can be recalculated as `price * issued shares` if issued shares are available.
- If PE, PB, dividend yield, or market cap comes from a third-party data page and cannot be reconciled, label it `第三方口径，未能复算`.
- Never mix a current market price with stale balance-sheet data without saying so.

## Liquidity and Market Microstructure

Rules:

- Always discuss liquidity for HK stocks.
- Prefer trading value over share volume when comparing liquidity across price levels.
- If available, check 20-day average trading value, current-day trading value, turnover ratio, bid/ask spread, free float, and Stock Connect eligibility.
- For small-cap, very low-turnover, resumed, or event-driven stocks, state that price can be heavily affected by sparse trading.
- Do not treat low PE or low PB as attractive without checking trading value and corporate-governance/event risk.

## Conditional HK Modules

Rules:

- AH premium applies only to dual-listed A/H companies. If not dual-listed, write `不适用`.
- Southbound flow applies when Stock Connect data is available or when the company is Stock Connect eligible. If unavailable, write `未取得可靠来源`.
- Short-selling data should be used for liquid names when available. If unavailable, do not infer short pressure from price action alone.
- Sector metrics must match the company industry. Do not apply bank metrics to internet companies or PE/PB-only frameworks to platform companies.

## Required Output Checks

Before finalizing, verify the report contains:

- A source/date line.
- A fact-check table.
- Recomputed premium/discount when offers or transactions are discussed.
- Recomputed price change when large daily moves are discussed.
- A clear intraday/close label for market data.
- Liquidity and conditional HK module status.
- `未取得可靠来源` or `第三方口径，未能复算` for unverified figures.
