# HK Market Modules

Use these modules to make Hong Kong stock analysis reflect HK market structure. Apply modules conditionally and keep the output concise.

## Liquidity Risk

Apply to every HK stock.

Check when available:

- 20-day average trading value.
- Current-day trading value.
- Turnover ratio.
- Bid/ask spread.
- Free float.
- Market cap and public float.
- Whether the stock is a penny stock, shell-like company, or very low-liquidity small cap.

Guidance:

- Trading value is often more useful than share volume.
- Low liquidity can make price, technical indicators, and valuation multiples unreliable.
- A low PE/PB stock with weak liquidity is not automatically cheap.
- If spread/free-float data is unavailable, write `未取得可靠来源`.

## Stock Connect and Southbound Flow

Apply when the stock is Stock Connect eligible or when southbound flow is material.

Check when available:

- Whether the stock is included in Southbound Stock Connect.
- Southbound net buy/sell.
- Southbound holding percentage.
- Recent change in southbound holding.

Guidance:

- Southbound flow can be important for large caps and mainland-favored sectors.
- If Stock Connect eligibility or flow data is unavailable, state that it was not verified.

## Short Selling

Apply when short-selling data is available or the stock is a liquid large/mid cap.

Check when available:

- Short selling turnover.
- Short selling ratio.
- Outstanding short position.
- Whether short pressure is high relative to recent average.

Guidance:

- Do not infer short selling from price decline alone.
- For high short-selling ratio names, discuss potential pressure and uncertainty, not trading instructions.

## AH Premium

Apply only when the company has both A-shares and H-shares.

Check when available:

- A-share ticker and H-share ticker.
- A/H price ratio adjusted for exchange rate.
- Historical AH premium percentile if available.

Formula:

```text
AH premium = (A-share price in HKD equivalent / H-share price - 1) * 100
```

Guidance:

- If not dual-listed, write `不适用`.
- Do not force AH analysis on red chips, local HK companies, or single-listed internet companies.

## HK Trading Rules

Consider where relevant:

- HK stocks are T+0.
- There is no normal daily price limit.
- Short selling and securities lending are more developed than A-share markets.
- Thin liquidity and wide spreads can amplify intraday moves.
- Odd lots and board-lot size can affect retail execution quality.

## Event-Driven Checklist

Apply to offers, resumptions, placings, subscriptions, buybacks, dividends, index changes, Stock Connect changes, acquisitions, disposals, and large price moves.

Check:

- Announcement date and effective date.
- Transaction price and reference price.
- Premium/discount calculation.
- Whether the event changes fundamentals, capital structure, ownership, liquidity, or only short-term sentiment.
- Whether technical analysis should be downgraded.

Use `观察点` and `验证点`, not direct trading strategy.
