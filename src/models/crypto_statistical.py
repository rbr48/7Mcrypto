"""
Cryptocurrency Statistical Models (M2, M3, M4).
M2: Single-Domain DVOL Logistic Model
M3: Multidisciplinary Regularized Logistic Model (ElasticNet/L2)
M4: Dynamic Autoregressive Model with Regime Transition Memory
"""

from typing import List, Optional
import numpy as np
import pandas as pd
from scipy.optimize import minimize


def _sigmoid(z: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-np.clip(z, -25.0, 25.0)))


class CryptoSingleDomainLogisticModel:
    """
    M2: Fits logistic regression exclusively on single crypto anchor domain (DVOL).
    """

    def __init__(self, target_cols: Optional[List[str]] = None):
        self.target_cols = target_cols or ["DVOL"]
        self.weights: np.ndarray = np.array([])
        self.intercept: float = 0.0
        self.train_mean: np.ndarray = np.array([])
        self.train_std: np.ndarray = np.array([])

    def fit(self, X_train: pd.DataFrame, y_train: np.ndarray) -> "CryptoSingleDomainLogisticModel":
        cols = [c for c in self.target_cols if c in X_train.columns]
        if not cols:
            cols = [X_train.columns[0]]

        X = X_train[cols].values
        self.train_mean = np.mean(X, axis=0)
        self.train_std = np.std(X, axis=0)
        self.train_std[self.train_std < 1e-6] = 1.0

        X_norm = (X - self.train_mean) / self.train_std
        y = np.asarray(y_train, dtype=float)

        def loss(params):
            b0 = params[0]
            w = params[1:]
            p = _sigmoid(b0 + X_norm @ w)
            p = np.clip(p, 1e-12, 1.0 - 1e-12)
            nll = -np.mean(y * np.log(p) + (1.0 - y) * np.log(1.0 - p))
            reg = 0.1 * np.sum(w**2)
            return nll + reg

        init_p = np.zeros(X_norm.shape[1] + 1)
        base_rate = np.clip(np.mean(y), 0.01, 0.99)
        init_p[0] = np.log(base_rate / (1.0 - base_rate))

        res = minimize(loss, init_p, method="L-BFGS-B")
        self.intercept = float(res.x[0])
        self.weights = res.x[1:]
        return self

    def predict_proba(self, X_test: pd.DataFrame, horizon: int = 1) -> np.ndarray:
        cols = [c for c in self.target_cols if c in X_test.columns]
        if not cols:
            cols = [X_test.columns[0]]
        X = X_test[cols].values
        X_norm = (X - self.train_mean) / self.train_std
        logits = self.intercept + X_norm @ self.weights
        p = _sigmoid(logits)
        # Multi-horizon shrinkage toward climatology
        decay = np.exp(-0.03 * (horizon - 1))
        return np.clip(p * decay + (1.0 - decay) * 0.15, 0.01, 0.99)


class CryptoMultidisciplinaryRegularizedModel:
    """
    M3: Multidisciplinary Regularized Model (L2 Ridge / ElasticNet) across all crypto features.
    """

    def __init__(self, l2_penalty: float = 0.5):
        self.l2_penalty = l2_penalty
        self.weights: np.ndarray = np.array([])
        self.intercept: float = 0.0
        self.train_mean: np.ndarray = np.array([])
        self.train_std: np.ndarray = np.array([])

    def fit(self, X_train: pd.DataFrame, y_train: np.ndarray) -> "CryptoMultidisciplinaryRegularizedModel":
        X = X_train.values
        self.train_mean = np.mean(X, axis=0)
        self.train_std = np.std(X, axis=0)
        self.train_std[self.train_std < 1e-6] = 1.0

        X_norm = (X - self.train_mean) / self.train_std
        y = np.asarray(y_train, dtype=float)

        def loss(params):
            b0 = params[0]
            w = params[1:]
            p = _sigmoid(b0 + X_norm @ w)
            p = np.clip(p, 1e-12, 1.0 - 1e-12)
            nll = -np.mean(y * np.log(p) + (1.0 - y) * np.log(1.0 - p))
            reg = self.l2_penalty * np.sum(w**2)
            return nll + reg

        init_p = np.zeros(X_norm.shape[1] + 1)
        base_rate = np.clip(np.mean(y), 0.01, 0.99)
        init_p[0] = np.log(base_rate / (1.0 - base_rate))

        res = minimize(loss, init_p, method="L-BFGS-B")
        self.intercept = float(res.x[0])
        self.weights = res.x[1:]
        return self

    def predict_proba(self, X_test: pd.DataFrame, horizon: int = 1) -> np.ndarray:
        X = X_test.values
        X_norm = (X - self.train_mean) / self.train_std
        logits = self.intercept + X_norm @ self.weights
        p = _sigmoid(logits)
        decay = np.exp(-0.03 * (horizon - 1))
        return np.clip(p * decay + (1.0 - decay) * 0.15, 0.01, 0.99)


class CryptoDynamicAutoregressiveModel:
    """
    M4: Dynamic Autoregressive Model with state persistence and mean-reverting regime memory.
    """

    def __init__(self, p_lags: int = 3):
        self.p_lags = p_lags
        self.phi: np.ndarray = np.array([])
        self.intercept: float = 0.0
        self.recent_history: np.ndarray = np.array([])

    def fit(self, X_train: pd.DataFrame, y_train: np.ndarray) -> "CryptoDynamicAutoregressiveModel":
        y = np.asarray(y_train, dtype=float)
        N = len(y)
        self.recent_history = y[-self.p_lags :] if N >= self.p_lags else np.pad(y, (self.p_lags - N, 0))

        if N <= self.p_lags + 5:
            self.intercept = float(np.mean(y)) if N > 0 else 0.15
            self.phi = np.zeros(self.p_lags)
            return self

        # Construct autoregressive matrix
        Y_target = y[self.p_lags :]
        X_lagged = np.column_stack([y[self.p_lags - k : N - k] for k in range(1, self.p_lags + 1)])

        def ar_loss(params):
            c = params[0]
            w = params[1:]
            logits = c + X_lagged @ w
            p = _sigmoid(logits)
            p = np.clip(p, 1e-12, 1.0 - 1e-12)
            nll = -np.mean(Y_target * np.log(p) + (1.0 - Y_target) * np.log(1.0 - p))
            reg = 0.2 * np.sum(w**2)
            return nll + reg

        init_p = np.zeros(self.p_lags + 1)
        base_rate = np.clip(np.mean(y), 0.01, 0.99)
        init_p[0] = np.log(base_rate / (1.0 - base_rate))
        if self.p_lags > 0:
            init_p[1] = 0.5  # Positive first-lag inertia

        res = minimize(ar_loss, init_p, method="L-BFGS-B")
        self.intercept = float(res.x[0])
        self.phi = res.x[1:]
        return self

    def predict_proba(self, X_test: pd.DataFrame, horizon: int = 1) -> np.ndarray:
        # Multi-step ahead autoregressive roll forward
        state = list(self.recent_history[::-1])  # [y_{t-1}, y_{t-2}, ...]
        p_future = 0.15
        for h in range(1, horizon + 1):
            lags = np.array(state[: self.p_lags])
            if len(lags) < self.p_lags:
                lags = np.pad(lags, (0, self.p_lags - len(lags)), constant_values=0.15)
            logit = self.intercept + float(np.dot(self.phi, lags))
            p_future = float(_sigmoid(logit))
            state.insert(0, p_future)

        return np.full(len(X_test), np.clip(p_future, 0.01, 0.99))
