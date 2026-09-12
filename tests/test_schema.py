"""Unit tests for SQLite Point-in-Time Schema and Temporal Query Isolation."""

import os
import tempfile
import pandas as pd
import pytest

from src.acquisition.schema import CryptoPointInTimeDatabase


@pytest.fixture
def temp_db():
    import gc
    tmp = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
    db_path = os.path.join(tmp.name, "test_crypto.db")
    db = CryptoPointInTimeDatabase(db_path=db_path)
    yield db
    del db
    gc.collect()
    try:
        tmp.cleanup()
    except Exception:
        pass


def test_schema_insertion_and_pit_isolation(temp_db):
    records = [
        # indicator, event_time, publication_time, raw_value, source, vintage_id
        ("BTC_PRICE", "2024-01-01", "2024-01-01 01:00:00", 42000.0, "Binance", "V1"),
        # Revision published later
        ("BTC_PRICE", "2024-01-01", "2024-01-01 05:00:00", 42050.0, "Binance", "V2"),
        # Event on Jan 2 published on Jan 2 at 01:00:00
        ("BTC_PRICE", "2024-01-02", "2024-01-02 01:00:00", 43000.0, "Binance", "V1"),
        # Macro event on Jan 1 with multi-day reporting lag (published Jan 4)
        ("DTWEXBGS", "2024-01-01", "2024-01-04 12:00:00", 102.5, "FRED", "V1"),
    ]
    temp_db.insert_records(records)

    # 1. Query as of Jan 1 at 02:00:00
    # Should see V1 of BTC_PRICE (42000.0), NOT V2 (42050.0)
    # Should NOT see Jan 2 BTC_PRICE
    # Should NOT see DTWEXBGS (published Jan 4)
    df_early = temp_db.query_as_of("2024-01-01 02:00:00")
    assert len(df_early) == 1
    assert df_early["BTC_PRICE"].iloc[0] == 42000.0
    assert "DTWEXBGS" not in df_early.columns

    # 2. Query as of Jan 1 at 06:00:00
    # Should see V2 of BTC_PRICE (42050.0)
    df_rev = temp_db.query_as_of("2024-01-01 06:00:00")
    assert len(df_rev) == 1
    assert df_rev["BTC_PRICE"].iloc[0] == 42050.0

    # 3. Query as of Jan 2 at 02:00:00
    # Should see Jan 1 and Jan 2 BTC_PRICE, but still NOT DTWEXBGS
    df_jan2 = temp_db.query_as_of("2024-01-02 02:00:00")
    assert len(df_jan2) == 2
    assert "DTWEXBGS" not in df_jan2.columns

    # 4. Query as of Jan 5
    # Should now see DTWEXBGS because publication_time (Jan 4) <= as_of_time
    df_jan5 = temp_db.query_as_of("2024-01-05 00:00:00")
    assert len(df_jan5) == 2
    assert "DTWEXBGS" in df_jan5.columns
    assert df_jan5.loc[pd.to_datetime("2024-01-01"), "DTWEXBGS"] == 102.5
