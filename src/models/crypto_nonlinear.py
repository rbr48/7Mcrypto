"""
Cryptocurrency Nonlinear Machine Learning Model (M5).
M5: LightGBM Gradient Boosted Decision Tree Ensemble.
"""

from typing import List, Optional
import lightgbm as lgb
import numpy as np
import pandas as pd


class CryptoNonlinearGBDTModel:
    """
    M5: 100-Tree Gradient Boosted Decision Tree (LightGBM) for crypto volatility and liquidation classification.
    """

    def __init__(self, n_estimators: int = 100, max_depth: int = 4, learning_rate: float = 0.05):
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.learning_rate = learning_rate
        self.model: Optional[lgb.LGBMClassifier] = None
        self.feature_names: List[str] = []
        self.fallback_prob: float = 0.15

    def fit(self, X_train: pd.DataFrame, y_train: np.ndarray) -> "CryptoNonlinearGBDTModel":
        self.feature_names = list(X_train.columns)
        y = np.asarray(y_train, dtype=int)
        self.fallback_prob = float(np.mean(y)) if len(y) > 0 else 0.15

        # If training labels are all 0 or all 1, fallback to base rate
        if len(np.unique(y)) < 2:
            self.model = None
            return self

        self.model = lgb.LGBMClassifier(
            n_estimators=self.n_estimators,
            max_depth=self.max_depth,
            learning_rate=self.learning_rate,
            num_leaves=15,
            min_child_samples=10,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=42,
            verbose=-1,
        )
        self.model.fit(X_train.values, y)
        return self

    def predict_proba(self, X_test: pd.DataFrame, horizon: int = 1) -> np.ndarray:
        if self.model is None:
            return np.full(len(X_test), np.clip(self.fallback_prob, 0.01, 0.99))

        try:
            probs = self.model.predict_proba(X_test.values)[:, 1]
        except Exception:
            probs = np.full(len(X_test), self.fallback_prob)

        # Multi-horizon uncertainty decay
        decay = np.exp(-0.04 * (horizon - 1))
        p_adj = probs * decay + (1.0 - decay) * self.fallback_prob
        return np.clip(p_adj, 0.01, 0.99)
