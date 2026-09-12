"""
Cryptocurrency Market Point-in-Time Data Ingestor.
Fetches public market time series from Deribit (DVOL) and Binance (Spot, Futures Funding, Stablecoin Depegging),
alongside macroeconomic linkage proxies from FRED.
"""

from datetime import datetime, timezone, timedelta
import json
import logging
import os
import sqlite3
import time
import urllib.request
import warnings
from typing import Dict, List, Tuple
import numpy as np
import pandas as pd

from src.acquisition.schema import CryptoPointInTimeDatabase

logger = logging.getLogger(__name__)


class CryptoDataIngestor:
    """
    Automated fetcher for 24/7 continuous cryptocurrency systemic risk indicators.
    """

    def __init__(self, db: CryptoPointInTimeDatabase):
        self.db = db
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) 4D-Crypto-Risk/1.0"}
        self.dvol_is_proxy = False  # Track whether DVOL fell back to realized vol

    def _http_get_json(self, url: str) -> dict:
        req = urllib.request.Request(url, headers=self.headers)
        with urllib.request.urlopen(req, timeout=15) as res:
            return json.loads(res.read().decode("utf-8"))

    def fetch_binance_klines(self, symbol: str = "BTCUSDT", interval: str = "1d", limit: int = 1000) -> pd.DataFrame:
        """
        Fetches daily OHLCV from Binance public API.
        """
        url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"
        data = self._http_get_json(url)
        rows = []
        for d in data:
            open_time = datetime.fromtimestamp(d[0] / 1000.0, tz=timezone.utc)
            rows.append(
                {
                    "event_time": open_time.strftime("%Y-%m-%d"),
                    "close": float(d[4]),
                    "volume": float(d[5]),
                }
            )
        df = pd.DataFrame(rows)
        df["event_time"] = pd.to_datetime(df["event_time"])
        return df.set_index("event_time")

    def fetch_binance_funding_rates(self, symbol: str = "BTCUSDT", pages: int = 6) -> pd.DataFrame:
        """
        Fetches historical 8-hour perpetual funding rates from Binance Futures with pagination.
        """
        rows = []
        end_time = int(datetime.now(timezone.utc).timestamp() * 1000)
        for _ in range(pages):
            url = f"https://fapi.binance.com/fapi/v1/fundingRate?symbol={symbol}&endTime={end_time}&limit=500"
            try:
                data = self._http_get_json(url)
            except Exception:
                break
            if not data:
                break
            for d in data:
                funding_time = datetime.fromtimestamp(d["fundingTime"] / 1000.0, tz=timezone.utc)
                rows.append(
                    {
                        "event_time": funding_time.strftime("%Y-%m-%d"),
                        "funding_rate": float(d["fundingRate"]),
                    }
                )
            end_time = data[0]["fundingTime"] - 1
            if len(data) < 500:
                break

        df = pd.DataFrame(rows)
        if df.empty:
            return pd.DataFrame()
        # Daily average annualized funding rate in %
        df["event_time"] = pd.to_datetime(df["event_time"])
        daily = df.groupby("event_time")["funding_rate"].mean() * 3 * 365 * 100.0
        return daily.sort_index().to_frame(name="BTC_FUNDING_RATE")

    def fetch_deribit_dvol(self, days_back: int = 1000) -> pd.DataFrame:
        """
        Fetches Deribit Bitcoin Implied Volatility Index (DVOL).
        """
        end_ms = int(datetime.now(timezone.utc).timestamp() * 1000)
        start_ms = end_ms - (days_back * 86400 * 1000)
        url = f"https://www.deribit.com/api/v2/public/get_volatility_index_data?currency=BTC&start_timestamp={start_ms}&end_timestamp={end_ms}&resolution=86400"
        
        try:
            res = self._http_get_json(url)
            data = res.get("result", {}).get("data", [])
            rows = []
            for d in data:
                # [timestamp, open, high, low, close]
                dt = datetime.fromtimestamp(d[0] / 1000.0, tz=timezone.utc)
                rows.append({"event_time": dt.strftime("%Y-%m-%d"), "DVOL": float(d[4])})
            df = pd.DataFrame(rows)
            if not df.empty:
                df["event_time"] = pd.to_datetime(df["event_time"])
                return df.set_index("event_time")
        except Exception as e:
            print(f"Warning: Deribit DVOL fetch encountered: {e}")
        return pd.DataFrame()

    def fetch_macro_fred_data(self, fred_db_path: str = "../4d-global-risk/data/processed/global_risk_database.db") -> pd.DataFrame:
        """
        Extracts macro dollar liquidity (DTWEXBGS) and VIX from local global risk database.
        """
        if not os.path.exists(fred_db_path):
            logger.warning(
                f"FRED macro database not found at '{fred_db_path}'. "
                "Macro features (DTWEXBGS, VIXCLS) will be excluded. "
                "To include them, ensure the 4d-global-risk project has been run first."
            )
            warnings.warn(
                f"4d-global-risk dependency missing: '{fred_db_path}' not found. "
                "Macro spillover features will be dropped from the model.",
                UserWarning,
                stacklevel=2,
            )
            return pd.DataFrame()
        conn = sqlite3.connect(fred_db_path)
        query = """
            SELECT event_time, indicator, raw_value
            FROM global_risk_provenance
            WHERE indicator IN ('DTWEXBGS', 'VIXCLS')
        """
        df = pd.read_sql_query(query, conn)
        df["event_time"] = pd.to_datetime(df["event_time"])
        piv = df.pivot_table(index="event_time", columns="indicator", values="raw_value", aggfunc="last")
        return piv

    # FRED publication delay lookup (business days after event_time).
    # DTWEXBGS (trade-weighted USD): published with ~2 business day lag.
    # VIXCLS (VIX close): published next business day by CBOE.
    FRED_PUB_DELAYS = {
        "DTWEXBGS": timedelta(days=3),  # ~2 business days ≈ 3 calendar days conservative
        "VIXCLS": timedelta(days=1),    # Next-day publication
    }

    def run_ingestion_pipeline(self, fred_db_path: str = "../4d-global-risk/data/processed/global_risk_database.db") -> pd.DataFrame:
        print("[Ingestion] Fetching Binance BTC & ETH spot klines...")
        df_btc = self.fetch_binance_klines("BTCUSDT", interval="1d", limit=1000)
        df_eth = self.fetch_binance_klines("ETHUSDT", interval="1d", limit=1000)
        df_usdc = self.fetch_binance_klines("USDCUSDT", interval="1d", limit=1000)

        print("[Ingestion] Fetching Binance BTC perpetual funding rates...")
        df_funding = self.fetch_binance_funding_rates("BTCUSDT", pages=7)

        print("[Ingestion] Fetching Deribit Bitcoin Volatility Index (DVOL)...")
        df_dvol = self.fetch_deribit_dvol(days_back=1000)

        print("[Ingestion] Fetching macro financial proxies from local FRED archive...")
        df_macro = self.fetch_macro_fred_data(fred_db_path)

        # Merge datasets on continuous daily calendar
        combined = pd.DataFrame(index=df_btc.index)
        combined["BTC_PRICE"] = df_btc["close"]
        
        # 30-day realized rolling volatility (annualized %)
        btc_ret = np.log(df_btc["close"] / df_btc["close"].shift(1))
        combined["BTC_REALIZED_VOL"] = btc_ret.rolling(30).std() * np.sqrt(365) * 100.0

        if not df_eth.empty:
            combined["ETH_BTC_RATIO"] = df_eth["close"] / df_btc["close"]
        
        if not df_usdc.empty:
            # Stablecoin depeg spread in basis points: abs(1.0 - price) * 10000
            combined["STABLECOIN_DEPEG_BPS"] = np.abs(df_usdc["close"] - 1.0) * 10000.0

        if not df_funding.empty:
            combined = combined.join(df_funding, how="left")
            combined["BTC_FUNDING_RATE"] = combined["BTC_FUNDING_RATE"].ffill()

        if not df_dvol.empty:
            combined = combined.join(df_dvol, how="left")
            # If DVOL has missing dates, use high-correlation realized volatility proxy
            dvol_missing = combined["DVOL"].isna().sum()
            if dvol_missing > 0:
                warnings.warn(
                    f"DVOL has {dvol_missing} missing dates filled with BTC_REALIZED_VOL proxy. "
                    "This may reduce implied volatility signal quality.",
                    UserWarning,
                    stacklevel=2,
                )
            combined["DVOL"] = combined["DVOL"].fillna(combined["BTC_REALIZED_VOL"])
        else:
            warnings.warn(
                "Deribit DVOL API failed completely. Using BTC_REALIZED_VOL as full proxy for DVOL. "
                "All DVOL-dependent analysis will reflect 30-day realized volatility instead of "
                "market-implied volatility. Results may differ significantly.",
                UserWarning,
                stacklevel=2,
            )
            logger.warning("DVOL entirely proxied by BTC_REALIZED_VOL — Deribit API unavailable.")
            self.dvol_is_proxy = True
            combined["DVOL"] = combined["BTC_REALIZED_VOL"]

        if not df_macro.empty:
            combined = combined.join(df_macro, how="left").ffill()

        # Clean aligned panel
        aligned = combined.dropna().sort_index()

        # Ingest records into SQLite Point-In-Time Database
        print(f"[Ingestion] Persisting {len(aligned)} daily time points across {len(aligned.columns)} indicators into SQLite...")
        records = []
        vintage_id = datetime.now(timezone.utc).strftime("VINTAGE_%Y%m%d")
        
        for dt, row in aligned.iterrows():
            event_str = dt.strftime("%Y-%m-%d")
            for col in aligned.columns:
                val = row[col]
                if pd.notnull(val):
                    # Use realistic publication delays per source
                    if col in self.FRED_PUB_DELAYS:
                        pub_delay = self.FRED_PUB_DELAYS[col]
                    else:
                        # Crypto public feeds: ~1 hour lag for daily closes
                        pub_delay = timedelta(hours=1)
                    pub_str = (dt + pub_delay).strftime("%Y-%m-%d %H:%M:%S")
                    records.append((col, event_str, pub_str, float(val), "Binance/Deribit/FRED", vintage_id))

        self.db.insert_records(records)
        print(f"[Ingestion] Complete. Total records stored: {len(records)}")
        if self.dvol_is_proxy:
            print("[Ingestion] WARNING: DVOL is fully proxied by BTC_REALIZED_VOL.")
        return aligned
