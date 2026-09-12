"""
Cryptocurrency State-Space Augmented Ensemble Model (M6).
M6: Regularized Logistic Regression augmented with DGRS latent state St,
isolating the value of the state-space extraction without full 4D propagation.
"""

from typing import List, Optional
import numpy as np
import pandas as pd
from scipy.optimize import minimize

from src.statespace.crypto_dgrs import SignIdentifiedCryptoDGRS


def _sigmoid(z: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-np.clip(z, -25.0, 25.0)))


class CryptoStateSpaceAugmentedModel:
    """
    M6: Logistic Regression with DGRS latent state St appended to raw features.
    Bridges the gap between M5 (pure ML on raw features) and M7 (full 4D framework)
    by adding only Dimension 1 (latent state) without Dimensions 2-4.
    """

    def __init__(self, anchor_indicator: str = "DVOL", l2_penalty: float = 0.3):
        self.anchor_indicator = anchor_indicator
        self.l2_penalty = l2_penalty
        self.dgrs = SignIdentifiedCryptoDGRS(anchor_indicator=anchor_indicator)
        self.weights: np.ndarray = np.array([])
        self.intercept: float = 0.0
        self.train_mean: np.ndarray = np.array([])
        self.train_std: np.ndarray = np.array([])
        self.latest_state: float = 0.0

    def fit(self, X_train: pd.DataFrame, y_train: np.ndarray) -> "CryptoStateSpaceAugmentedModel":
        y = np.asarray(y_train, dtype=float)

        # 1. Extract latent state via DGRS
        self.dgrs.fit(X_train)
        smoothed_means, _, _ = self.dgrs.smooth(X_train)
        self.latest_state = float(smoothed_means[-1]) if len(smoothed_means) > 0 else 0.0

        # 2. Augment raw features with latent state
        X_raw = X_train.values
        X_aug = np.column_stack([smoothed_means, X_raw])

        self.train_mean = np.mean(X_aug, axis=0)
        self.train_std = np.std(X_aug, axis=0)
        self.train_std[self.train_std < 1e-6] = 1.0
        X_norm = (X_aug - self.train_mean) / self.train_std

        # 3. Fit regularized logistic regression
        def loss(params):
            b0 = params[0]
            w = params[1:]
            p = _sigmoid(b0 + X_norm @ w)
            p = np.clip(p, 1e-12, 1.0 - 1e-12)
            nll = -np.mean(y * np.log(p) + (1.0 - y) * np.log(1.0 - p))
            reg = self.l2_penalty * np.sum(w ** 2)
            return nll + reg

        init_p = np.zeros(X_norm.shape[1] + 1)
        base_rate = np.clip(np.mean(y), 0.01, 0.99)
        init_p[0] = np.log(base_rate / (1.0 - base_rate))
        init_p[1] = 1.0  # Positive initial loading on latent state

        res = minimize(loss, init_p, method="L-BFGS-B")
        self.intercept = float(res.x[0])
        self.weights = res.x[1:]
        return self

    def predict_proba(self, X_test: pd.DataFrame, horizon: int = 1) -> np.ndarray:
        X_raw = X_test.values
        Z_test = (X_raw - self.dgrs.train_mean) / self.dgrs.train_std

        # Forward-project latent state
        Lambda = self.dgrs.loadings
        a_pred = float(np.dot(Z_test[-1], Lambda)) if len(Z_test) > 0 else self.latest_state
        decay = (self.dgrs.T_transition) ** horizon
        a_proj = a_pred * decay

        X_aug = np.column_stack([np.full(len(X_test), a_proj), X_raw])
        X_norm = (X_aug - self.train_mean) / self.train_std

        logits = self.intercept + X_norm @ self.weights
        p = _sigmoid(logits)

        # Horizon dampening
        time_decay = np.exp(-0.03 * (horizon - 1))
        return np.clip(p * time_decay + (1.0 - time_decay) * 0.15, 0.01, 0.99)
