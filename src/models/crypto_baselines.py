"""
Cryptocurrency Benchmark Baseline Models (M0, M1).
M0: Crypto Persistence Model (tomorrow's risk state = today's state)
M1: Crypto Climatology Model (unconditional sample base rate)
"""

import numpy as np
import pandas as pd


class CryptoPersistenceModel:
    """
    M0: Assumes probability of crisis shock at horizon h equals current state.
    """

    def __init__(self):
        self.last_state: float = 0.0

    def fit(self, X_train: pd.DataFrame, y_train: np.ndarray) -> "CryptoPersistenceModel":
        if len(y_train) > 0:
            self.last_state = float(y_train[-1])
        return self

    def predict_proba(self, X_test: pd.DataFrame, horizon: int = 1) -> np.ndarray:
        # Decay persistence slightly as horizon increases
        decay = np.exp(-0.05 * (horizon - 1))
        p = self.last_state * decay + (1.0 - decay) * 0.15
        p_clipped = np.clip(p, 0.01, 0.99)
        return np.full(len(X_test), p_clipped)


class CryptoClimatologyModel:
    """
    M1: Unconditional historical base rate.
    """

    def __init__(self):
        self.base_rate: float = 0.15

    def fit(self, X_train: pd.DataFrame, y_train: np.ndarray) -> "CryptoClimatologyModel":
        if len(y_train) > 0:
            self.base_rate = float(np.mean(y_train))
        return self

    def predict_proba(self, X_test: pd.DataFrame, horizon: int = 1) -> np.ndarray:
        p = np.clip(self.base_rate, 0.01, 0.99)
        return np.full(len(X_test), p)
