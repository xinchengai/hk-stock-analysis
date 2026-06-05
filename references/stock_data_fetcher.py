#!/usr/bin/env python3
"""
Hong Kong stock data fetcher for hk-stock-analysis.

Outputs structured JSON only. The agent using this skill performs the final
research writing and current-news synthesis.
"""

from __future__ import annotations

import argparse
import datetime as dt
import importlib.util
import json
import math
import re
import sys
from typing import Any, Dict, Iterable, List, Optional, Tuple


RECOMMENDED_INSTALL = "python3 -m pip install efinance akshare yfinance pandas requests"
PROVIDERS = ("efinance", "akshare", "yfinance")


def emit(payload: Dict[str, Any], exit_code: int = 0) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    raise SystemExit(exit_code)


def provider_available(name: str) -> bool:
    return importlib.util.find_spec(name) is not None


def normalize_hk_ticker(raw: str) -> str:
    token = raw.strip().upper().replace(" ", "")
    patterns = [
        r"^HK(\d{5})$",
        r"^(\d{5})\.HK$",
        r"^(\d{5})$",
    ]
    for pattern in patterns:
        match = re.match(pattern, token)
        if match:
            return f"HK{match.group(1)}"
    raise ValueError(f"Only HK tickers are supported. Expected HK00700, 00700.HK, or 00700; got {raw!r}.")


def hk_numeric(ticker: str) -> str:
    return ticker.replace("HK", "")


def yahoo_symbol(ticker: str) -> str:
    return f"{hk_numeric(ticker)}.HK"


def safe_float(value: Any) -> Optional[float]:
    if value is None:
        return None
    try:
        if isinstance(value, str):
            value = value.replace(",", "").replace("%", "").strip()
            if not value or value in {"-", "--", "N/A", "nan", "None"}:
                return None
        result = float(value)
        if math.isnan(result) or math.isinf(result):
            return None
        return result
    except Exception:
        return None


def safe_int(value: Any) -> Optional[int]:
    number = safe_float(value)
    return int(number) if number is not None else None


def clean_records(records: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    cleaned: List[Dict[str, Any]] = []
    for row in records:
        date_value = row.get("date") or row.get("日期") or row.get("Date")
        close = safe_float(row.get("close") or row.get("收盘") or row.get("Close"))
        if not date_value or close is None:
            continue
        cleaned.append(
            {
                "date": str(date_value)[:10],
                "open": safe_float(row.get("open") or row.get("开盘") or row.get("Open")),
                "high": safe_float(row.get("high") or row.get("最高") or row.get("High")),
                "low": safe_float(row.get("low") or row.get("最低") or row.get("Low")),
                "close": close,
                "volume": safe_int(row.get("volume") or row.get("成交量") or row.get("Volume")),
            }
        )
    cleaned.sort(key=lambda item: item["date"])
    return cleaned


def tail(values: List[Optional[float]], n: int) -> Optional[float]:
    if len(values) < n:
        return None
    subset = [value for value in values[-n:] if value is not None]
    if len(subset) != n:
        return None
    return sum(subset) / n


def ema(values: List[float], span: int) -> List[float]:
    if not values:
        return []
    alpha = 2 / (span + 1)
    result = [values[0]]
    for value in values[1:]:
        result.append(alpha * value + (1 - alpha) * result[-1])
    return result


def rsi(values: List[float], period: int = 14) -> Optional[float]:
    if len(values) <= period:
        return None
    gains: List[float] = []
    losses: List[float] = []
    for prev, curr in zip(values[-period - 1 : -1], values[-period:]):
        diff = curr - prev
        gains.append(max(diff, 0))
        losses.append(abs(min(diff, 0)))
    avg_gain = sum(gains) / period
    avg_loss = sum(losses) / period
    if avg_loss == 0:
        return 100.0
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))


def macd(values: List[float]) -> Dict[str, Optional[float]]:
    if len(values) < 35:
        return {"macd": None, "signal": None, "histogram": None}
    ema12 = ema(values, 12)
    ema26 = ema(values, 26)
    macd_line = [a - b for a, b in zip(ema12[-len(ema26) :], ema26)]
    signal = ema(macd_line, 9)
    return {
        "macd": round(macd_line[-1], 4),
        "signal": round(signal[-1], 4),
        "histogram": round(macd_line[-1] - signal[-1], 4),
    }


def compute_indicators(ohlcv: List[Dict[str, Any]]) -> Dict[str, Any]:
    closes = [row["close"] for row in ohlcv if row.get("close") is not None]
    volumes = [row.get("volume") for row in ohlcv]
    highs = [row.get("high") for row in ohlcv if row.get("high") is not None]
    lows = [row.get("low") for row in ohlcv if row.get("low") is not None]
    latest = closes[-1] if closes else None
    prev = closes[-2] if len(closes) >= 2 else None
    volume_latest = volumes[-1] if volumes else None
    volume_ma20 = tail([safe_float(v) for v in volumes], 20)

    high_180 = max(highs[-180:]) if highs else None
    low_180 = min(lows[-180:]) if lows else None

    return {
        "last_close": round(latest, 4) if latest is not None else None,
        "change_pct": round((latest - prev) / prev * 100, 2) if latest is not None and prev else None,
        "ma20": round(tail(closes, 20), 4) if tail(closes, 20) is not None else None,
        "ma60": round(tail(closes, 60), 4) if tail(closes, 60) is not None else None,
        "ma120": round(tail(closes, 120), 4) if tail(closes, 120) is not None else None,
        "rsi14": round(rsi(closes, 14), 2) if rsi(closes, 14) is not None else None,
        "macd": macd(closes),
        "volume_latest": volume_latest,
        "volume_ma20": round(volume_ma20, 2) if volume_ma20 is not None else None,
        "range_high": round(high_180, 4) if high_180 is not None else None,
        "range_low": round(low_180, 4) if low_180 is not None else None,
        "support_reference": round(low_180, 4) if low_180 is not None else None,
        "resistance_reference": round(high_180, 4) if high_180 is not None else None,
    }


def fetch_with_efinance(ticker: str, days: int) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
    import efinance as ef  # type: ignore

    code = hk_numeric(ticker)
    quote_rows = ef.stock.get_realtime_quotes("港股")
    quote = None
    for _, row in quote_rows.iterrows():
        row_dict = row.to_dict()
        if str(row_dict.get("股票代码") or row_dict.get("代码") or "").zfill(5) == code:
            quote = row_dict
            break
    hist = ef.stock.get_quote_history(code, klt=101)
    records = clean_records(hist.tail(days).to_dict("records"))
    meta = {
        "name": quote.get("股票名称") if quote else None,
        "last_price": safe_float(quote.get("最新价")) if quote else None,
        "change_pct": safe_float(quote.get("涨跌幅")) if quote else None,
        "volume": safe_int(quote.get("成交量")) if quote else None,
        "currency": "HKD",
    }
    return meta, records


def fetch_with_akshare(ticker: str, days: int) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
    import akshare as ak  # type: ignore

    code = hk_numeric(ticker)
    hist = ak.stock_hk_hist(symbol=code, period="daily", adjust="")
    records = clean_records(hist.tail(days).to_dict("records"))
    meta = {"name": None, "last_price": None, "change_pct": None, "volume": None, "currency": "HKD"}
    try:
        spot = ak.stock_hk_spot_em()
        for _, row in spot.iterrows():
            row_dict = row.to_dict()
            row_code = str(row_dict.get("代码") or row_dict.get("序号") or "").zfill(5)
            if row_code == code:
                meta.update(
                    {
                        "name": row_dict.get("名称"),
                        "last_price": safe_float(row_dict.get("最新价")),
                        "change_pct": safe_float(row_dict.get("涨跌幅")),
                        "volume": safe_int(row_dict.get("成交量")),
                    }
                )
                break
    except Exception:
        pass
    return meta, records


def fetch_with_yfinance(ticker: str, days: int) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
    import yfinance as yf  # type: ignore

    stock = yf.Ticker(yahoo_symbol(ticker))
    hist = stock.history(period=f"{max(days, 30)}d", interval="1d")
    records = clean_records(hist.reset_index().tail(days).to_dict("records"))
    info = {}
    try:
        info = stock.get_info() or {}
    except Exception:
        info = {}
    meta = {
        "name": info.get("shortName") or info.get("longName"),
        "last_price": safe_float(info.get("currentPrice") or info.get("regularMarketPrice")),
        "change_pct": None,
        "volume": safe_int(info.get("volume") or info.get("regularMarketVolume")),
        "currency": info.get("currency") or "HKD",
    }
    return meta, records


def fetch_hk_stock(ticker: str, days: int) -> Dict[str, Any]:
    attempts = [
        ("efinance", fetch_with_efinance),
        ("akshare", fetch_with_akshare),
        ("yfinance", fetch_with_yfinance),
    ]
    errors: List[Dict[str, str]] = []
    missing = [name for name in PROVIDERS if not provider_available(name)]
    if len(missing) == len(PROVIDERS):
        return {
            "ok": False,
            "error_type": "missing_dependencies",
            "ticker": ticker,
            "missing_provider_packages": list(PROVIDERS),
            "install_command": RECOMMENDED_INSTALL,
            "message": "No HK data provider package is installed.",
        }

    for provider, fetcher in attempts:
        if not provider_available(provider):
            errors.append({"provider": provider, "error": "package not installed"})
            continue
        try:
            meta, ohlcv = fetcher(ticker, days)
            if not ohlcv:
                raise RuntimeError("provider returned no OHLCV records")
            indicators = compute_indicators(ohlcv)
            latest_price = meta.get("last_price") or indicators.get("last_close")
            change_pct = meta.get("change_pct") if meta.get("change_pct") is not None else indicators.get("change_pct")
            return {
                "ok": True,
                "ticker": ticker,
                "yahoo_symbol": yahoo_symbol(ticker),
                "market": "HK",
                "name": meta.get("name"),
                "currency": meta.get("currency") or "HKD",
                "latest_price": latest_price,
                "change_pct": change_pct,
                "volume": meta.get("volume") or indicators.get("volume_latest"),
                "ohlcv": ohlcv,
                "indicators": indicators,
                "data_source": provider,
                "fetch_time": dt.datetime.now(dt.timezone.utc).astimezone().isoformat(timespec="seconds"),
                "provider_errors": errors,
            }
        except Exception as exc:
            errors.append({"provider": provider, "error": str(exc)})

    return {
        "ok": False,
        "error_type": "provider_failure",
        "ticker": ticker,
        "provider_errors": errors,
        "install_command": RECOMMENDED_INSTALL,
    }


def main(argv: Optional[List[str]] = None) -> None:
    parser = argparse.ArgumentParser(description="Fetch HK stock data and technical indicators as JSON.")
    parser.add_argument("ticker", help="HK ticker, e.g. HK00700, 00700.HK, or 00700")
    parser.add_argument("--days", type=int, default=180, help="Number of daily bars to fetch; default 180")
    args = parser.parse_args(argv)

    try:
        ticker = normalize_hk_ticker(args.ticker)
    except ValueError as exc:
        emit({"ok": False, "error_type": "unsupported_ticker", "message": str(exc)}, exit_code=2)

    days = max(30, min(args.days, 365))
    payload = fetch_hk_stock(ticker, days)
    emit(payload, exit_code=0 if payload.get("ok") else 1)


if __name__ == "__main__":
    main()
