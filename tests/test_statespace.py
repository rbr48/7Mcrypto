"""Unit tests for Sign-Identified DGRS state-space model with EM estimation."""

import numpy as np
import pandas as pd
import pytest

from src.statespace.crypto_dgrs import SignIdentifiedCryptoDGRS


@pytest.fixture
def sample_crypto_panel():
    np.random.seed(42)
    N = 120
    dates = pd.date_range("2024-01-01", periods=N, freq="D")
    
    # Generate coupled latent factor and indicators
    true_latent = np.cumsum(np.random.normal(0, 0.5, size=N))
    
    data = {
        "BTC_PRICE": 40000 - 500 * true_latent + np.random.normal(0, 100, size=N),
        "BTC_REALIZED_VOL": 50 + 5 * true_latent + np.random.normal(0, 2, size=N),
        "ETH_BTC_RATIO": 0.05 - 0.002 * true_latent + np.random.normal(0, 0.001, size=N),
        "STABLECOIN_DEPEG_BPS": np.abs(true_latent * 2 + np.random.normal(0, 1, size=N)),
        "BTC_FUNDING_RATE": 10 + 3 * true_latent + np.random.normal(0, 1, size=N),
        "DVOL": 60 + 8 * true_latent + np.random.normal(0, 2, size=N),  # Anchor
    }
    return pd.DataFrame(data, index=dates)


def test_dgrs_polarity_constraint(sample_crypto_panel):
    dgrs = SignIdentifiedCryptoDGRS(anchor_indicator="DVOL")
    dgrs.fit(sample_crypto_panel)

    anchor_idx = dgrs.feature_names.index("DVOL")
    assert dgrs.loadings[anchor_idx] > 0.0, "Anchor loading must strictly satisfy lambda_anchor > 0"


def test_dgrs_polarity_inversion():
    # Construct data where first SVD eigenvector has negative anchor loading
    np.random.seed(123)
    N = 80
    dates = pd.date_range("2024-01-01", periods=N, freq="D")
    latent = np.linspace(-3, 3, N)
    
    # DVOL decreases as latent increases
    data = {
        "FEATURE_A": latent + np.random.normal(0, 0.1, size=N),
        "DVOL": -2.0 * latent + np.random.normal(0, 0.1, size=N),
    }
    df = pd.DataFrame(data, index=dates)

    dgrs = SignIdentifiedCryptoDGRS(anchor_indicator="DVOL")
    dgrs.fit(df)

    anchor_idx = dgrs.feature_names.index("DVOL")
    assert dgrs.loadings[anchor_idx] > 0.0, "Polarity must be flipped so lambda_DVOL > 0"


def test_dgrs_em_q_estimation(sample_crypto_panel):
    dgrs = SignIdentifiedCryptoDGRS(anchor_indicator="DVOL", em_iterations=5)
    dgrs.fit(sample_crypto_panel)

    # Q must be strictly positive and bounded
    assert 1e-4 <= dgrs.Q_variance <= 2.0
    assert not np.isnan(dgrs.Q_variance)


def test_dgrs_filtering_and_smoothing(sample_crypto_panel):
    dgrs = SignIdentifiedCryptoDGRS(anchor_indicator="DVOL")
    dgrs.fit(sample_crypto_panel)

    # Forward filter
    filtered_means, filtered_covs = dgrs.filter(sample_crypto_panel)
    assert len(filtered_means) == len(sample_crypto_panel)
    assert len(filtered_covs) == len(sample_crypto_panel)
    assert not np.any(np.isnan(filtered_means))
    assert np.all(filtered_covs > 0)

    # Backward RTS smoother
    smoothed_means, smoothed_covs, ci_df = dgrs.smooth(sample_crypto_panel)
    assert len(smoothed_means) == len(sample_crypto_panel)
    assert len(smoothed_covs) == len(sample_crypto_panel)
    assert not np.any(np.isnan(smoothed_means))
    assert np.all(smoothed_covs > 0)

    # Credible intervals
    assert set(ci_df.columns) == {"mean", "lower_95", "upper_95"}
    assert np.all(ci_df["lower_95"] <= ci_df["mean"])
    assert np.all(ci_df["mean"] <= ci_df["upper_95"])


def test_dgrs_huber_robustness(sample_crypto_panel):
    # Inject an extreme flash-crash outlier into one observation
    corrupted_panel = sample_crypto_panel.copy()
    corrupted_panel.iloc[50, corrupted_panel.columns.get_loc("DVOL")] = 500.0  # +500 vol shock

    dgrs = SignIdentifiedCryptoDGRS(anchor_indicator="DVOL", huber_threshold=3.0)
    dgrs.fit(corrupted_panel)

    smoothed_means, _, _ = dgrs.smooth(corrupted_panel)
    assert not np.any(np.isnan(smoothed_means))
    assert not np.any(np.isinf(smoothed_means))


def test_dgrs_select_n_factors(sample_crypto_panel):
    dgrs = SignIdentifiedCryptoDGRS()
    best_m = dgrs.select_n_factors(sample_crypto_panel, max_factors=4)
    assert 1 <= best_m <= 4
