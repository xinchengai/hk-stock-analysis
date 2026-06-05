---
name: hk-stock-analysis
description: Hong Kong stock research skill for OpenClaw; analyzes HK tickers only with market data, technical indicators, news, and a research-reference brief.
metadata: version=1.0; market=HK; output=research-reference
---

# HK Stock Analysis

Use this skill when the user asks to analyze a Hong Kong listed stock, including inputs like `HK00700`, `00700.HK`, `00700`, or a Chinese company name such as `腾讯控股`.

Do not use this skill for A-share or US tickers. If the input is clearly outside Hong Kong, say the skill only supports HK stocks and ask for an HK ticker or company name.

## Operating Rules

- Treat the output as research reference only. Do not give direct buy/sell instructions, portfolio allocation, or personalized investment advice.
- Always state data source names and fetch/search dates.
- Prefer current web sources for market/news context. For news, search recent HKEX announcements, company news, sector news, and broad market context.
- If the user provides a Chinese company name, use web search first to resolve the HK ticker, then run the data script.
- Keep conclusions as `偏强`, `中性`, or `偏弱`, with evidence and risks.
- Before writing the final report, run the Fact Check Gate below. Do not skip it for urgent or simple requests.

## Input Normalization

Accept:

- `HK` + 5 digits: `HK00700`
- 5 digits + `.HK`: `00700.HK`
- 5 digits alone: `00700`

Normalize all valid tickers to `HKNNNNN` before analysis. Reject obvious non-HK formats like `AAPL`, `TSLA`, `600519`, `000001.SZ`, or `600519.SH`.

## Workflow

1. Resolve the HK ticker:
   - If the user gave a valid HK ticker, normalize it.
   - If the user gave a company name, search the web for the HK stock code and use the best-supported result.
2. Run the bundled script:
   - Script path: `{baseDir}/references/stock_data_fetcher.py`
   - Command: `python3 {baseDir}/references/stock_data_fetcher.py HK00700 --days 180`
   - For multiple HK stocks, run the script once per ticker.
3. Read the JSON result:
   - If `ok` is false and `error_type` is `missing_dependencies`, tell the user to install the listed packages and include the suggested install command.
   - If `ok` is false for any other reason, report the failure with the ticker and data source errors.
4. Search current context:
   - HKEX announcements for the company.
   - Recent company news.
   - Sector or index context, including Hang Seng Index and Southbound Stock Connect when available.
5. Run the Fact Check Gate using `references/fact-check-rules.md`.
6. Write the final report using `references/output-format-template.md`.

## Fact Check Gate

Read `references/fact-check-rules.md` before drafting any report section that mentions announcements, offers, subscriptions, placings, resumption, financial years, valuation, or large price moves.

The final report must pass these checks:

- HKEX primary-source check: material events must be verified against HKEX/company announcements where available. News summaries can support context but cannot override HKEX documents.
- Premium/discount check: every `溢价` or `折让` claim must be recomputed with `(offer_or_transaction_price - reference_price) / reference_price`. Positive means `溢价`; negative means `折让`.
- Price-change check: every intraday or daily percentage move must be recomputed with `(current_or_close_price - previous_close) / previous_close`.
- Time-label check: if the quote is intraday or captured during trading hours, write `盘中` or `截至 HH:MM`; do not write `收盘` or `收盘涨幅`.
- Financial-year check: fiscal-year dates must follow the HKEX annual/interim report title, not inference from publish date.
- Valuation check: PE, PB, dividend yield, market cap, and NAV-derived figures must either be recalculated from disclosed values or labeled as third-party source figures.
- Event-driven check: for resumption, offer, placing, acquisition, disposal, liquidation, winding-up, or very large one-day moves, explicitly state that technical indicators have reduced reliability.

If a figure cannot be verified or reconciled, write `未取得可靠来源` or `第三方口径，未能复算`, and do not present it as confirmed fact.

## Recommended Dependencies

The skill can load without dependencies, but the data script needs at least one data provider package to fetch live data.

Recommended install command:

```bash
python3 -m pip install efinance akshare yfinance pandas requests
```

Provider priority for HK stocks:

1. `efinance`
2. `akshare`
3. `yfinance`

## Report Requirements

- Start with a compact summary table.
- Include market data snapshot, technical view, recent news/announcement context, market/sector context, risks, and a final research stance.
- Include a `事实校验` section before the conclusion or evidence-weighting section.
- Use evidence-weighted language: `supporting evidence`, `contradicting evidence`, `watch items`.
- Avoid `买入`, `卖出`, `止损`, `目标价`, `仓位`, or similar direct trading instructions unless quoting a third-party analyst rating, and clearly label it as third-party.
