"""
Point-in-Time Schema for Cryptocurrency Systemic Risk Database.
Guarantees strict auditability, event_time vs publication_time separation,
and non-leaking vintage isolation for 24/7/365 crypto markets.
"""

from datetime import datetime, timezone
import os
import sqlite3
from typing import Dict, List, Optional, Tuple, Union
import pandas as pd


SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS crypto_risk_provenance (
    indicator TEXT NOT NULL,
    event_time TEXT NOT NULL,
    publication_time TEXT NOT NULL,
    raw_value REAL NOT NULL,
    source TEXT NOT NULL,
    vintage_id TEXT NOT NULL,
    created_at TEXT NOT NULL,
    PRIMARY KEY (indicator, event_time, publication_time)
);

CREATE INDEX IF NOT EXISTS idx_crypto_indicator_time 
ON crypto_risk_provenance(indicator, event_time);

CREATE INDEX IF NOT EXISTS idx_crypto_pub_time 
ON crypto_risk_provenance(publication_time);
"""


class CryptoPointInTimeDatabase:
    """
    Manages point-in-time time-series persistence for 24/7 continuous crypto markets.
    """

    def __init__(self, db_path: str = "data/processed/crypto_risk_database.db"):
        self.db_path = db_path
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.init_db()

    def init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.executescript(SCHEMA_SQL)

    def insert_records(self, records: List[Tuple[str, str, str, float, str, str]]):
        """
        Inserts records: (indicator, event_time, publication_time, raw_value, source, vintage_id).
        """
        if not records:
            return
        now_str = datetime.now(timezone.utc).isoformat()
        insert_sql = """
        INSERT OR REPLACE INTO crypto_risk_provenance 
        (indicator, event_time, publication_time, raw_value, source, vintage_id, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        rows = [(r[0], r[1], r[2], float(r[3]), r[4], r[5], now_str) for r in records]
        with sqlite3.connect(self.db_path) as conn:
            conn.executemany(insert_sql, rows)

    def query_as_of(
        self,
        as_of_time: Union[datetime, str],
        indicators: Optional[List[str]] = None,
    ) -> pd.DataFrame:
        """
        Queries all records known as of a specific point-in-time timestamp.
        Filters strictly by publication_time <= as_of_time to eliminate lookahead bias.
        """
        if isinstance(as_of_time, str):
            as_of_str = as_of_time
        elif hasattr(as_of_time, "strftime"):
            as_of_str = as_of_time.strftime("%Y-%m-%d %H:%M:%S")
        else:
            as_of_str = str(as_of_time)
        with sqlite3.connect(self.db_path) as conn:
            if indicators:
                placeholders = ",".join(["?"] * len(indicators))
                query = f"""
                SELECT event_time, indicator, raw_value
                FROM crypto_risk_provenance
                WHERE publication_time <= ?
                  AND indicator IN ({placeholders})
                ORDER BY event_time ASC
                """
                params = [as_of_str] + indicators
                df = pd.read_sql_query(query, conn, params=params)
            else:
                query = """
                SELECT event_time, indicator, raw_value
                FROM crypto_risk_provenance
                WHERE publication_time <= ?
                ORDER BY event_time ASC
                """
                df = pd.read_sql_query(query, conn, params=[as_of_str])

        if df.empty:
            return pd.DataFrame()

        df["event_time"] = pd.to_datetime(df["event_time"])
        pivoted = df.pivot_table(index="event_time", columns="indicator", values="raw_value", aggfunc="last")
        return pivoted.sort_index()
