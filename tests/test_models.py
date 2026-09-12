"""Unit tests for M0-M7 cryptocurrency risk models."""

import numpy as np
import pandas as pd
import pytest

from src.models import (
    CryptoPersistenceModel,
    CryptoClimatologyModel,
    CryptoSingleDomainLogisticModel,
    CryptoMultidisciplinaryRegularizedModel,
    CryptoDynamicAutoregressiveModel,
    CryptoNonlinearGBDTModel,
    CryptoStateSpaceAugmentedModel,
    CryptoFull4DDLMModel,
)


@pytest.fixture
def synthetic_training_data():
    np.random.seed(42)
    N = 90
    dates = pd.date_range("2024-01-01", periods=N, freq="D")
    data = {
        "BTC_PRICE": np.linspace(40000, 45000, N) + np.random.normal(0, 200, N),
        "BTC_REALIZED_VOL": np.random.uniform(40, 80, N),
        "ETH_BTC_RATIO": np.random.uniform(0.04, 0.06, N),
        "STABLECOIN_DEPEG_BPS": np.random.exponential(1.5, N),
        "BTC_FUNDING_RATE": np.random.normal(10, 5, N),
        "DVOL": np.random.uniform(50, 90, N),
    }
    X = pd.DataFrame(data, index=dates)
    y = np.random.binomial(1, 0.15, size=N)
    return X, y


@pytest.mark.parametrize(
    "model_cls, kwargs",
    [
        (CryptoPersistenceModel, {}),
        (CryptoClimatologyModel, {}),
        (CryptoSingleDomainLogisticModel, {"target_cols": ["DVOL"]}),
        (CryptoMultidisciplinaryRegularizedModel, {}),
        (CryptoDynamicAutoregressiveModel, {}),
        (CryptoNonlinearGBDTModel, {}),
        (CryptoStateSpaceAugmentedModel, {"anchor_indicator": "DVOL"}),
        (CryptoFull4DDLMModel, {"anchor_indicator": "DVOL", "horizons": [1, 3, 7, 14]}),
    ],
)
def test_model_fit_and_predict_bounds(synthetic_training_data, model_cls, kwargs):
    X, y = synthetic_training_data
    model = model_cls(**kwargs)
    model.fit(X, y)

    X_test = X.iloc[-5:].copy()
    for h in [1, 3, 7, 14]:
        probs = model.predict_proba(X_test, horizon=h)
        assert len(probs) == len(X_test)
        assert np.all(probs >= 0.0), f"{model_cls.__name__} predicted prob < 0 at h={h}"
        assert np.all(probs <= 1.0), f"{model_cls.__name__} predicted prob > 1 at h={h}"
        assert not np.any(np.isnan(probs)), f"{model_cls.__name__} produced NaN at h={h}"


def test_m7_full_4d_girf_properties(synthetic_training_data):
    X, y = synthetic_training_data
    p = X.shape[1]
    m7 = CryptoFull4DDLMModel(anchor_indicator="DVOL", horizons=[1, 7])
    m7.fit(X, y)

    for h in [1, 7]:
        pi_h = m7.get_propagation_matrix(horizon=h)
        raw_pi_h = m7.get_raw_propagation_matrix(horizon=h)

        # Shape verification
        assert pi_h.shape == (p, p)
        assert raw_pi_h.shape == (p, p)

        # Generalized IRF diagonal must be 1.0
        assert np.allclose(np.diag(pi_h), 1.0, atol=1e-8)

        # Values must be bounded in [-1.0, 1.0]
        assert np.all(pi_h >= -1.0)
        assert np.all(pi_h <= 1.0)

        # No NaNs or Infs
        assert not np.any(np.isnan(pi_h))
        assert not np.any(np.isnan(raw_pi_h))
