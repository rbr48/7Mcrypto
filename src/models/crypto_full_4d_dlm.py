"""
Full 4D Dynamic Linear Model (M7) for Cryptocurrency Systemic Risk.
Integrates:
- D1: Latent State St (Sign-Identified DGRS Kalman Filter with EM-estimated Q)
- D2: Contemporaneous Interaction Network At
- D3: Multi-Horizon Generalized IRF Propagation Matrix Pi_h (Pesaran & Shin 1998)
- D4: Temporal Shock Decay Across Time Horizons (t + h)
"""

from typing import Dict, List, Optional
import numpy as np
import pandas as pd
from scipy.optimize import minimize

from src.statespace.crypto_dgrs import SignIdentifiedCryptoDGRS


def _sigmoid(z: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-np.clip(z, -25.0, 25.0)))


class CryptoFull4DDLMModel:
    """
    M7: Full 4D Dynamic Linear Model generating continuous systemic state tracking
    and multi-horizon Generalized Impulse Response matrices Pi_h.
    """

    def __init__(self, anchor_indicator: str = "DVOL", horizons: Optional[List[int]] = None):
        self.anchor_indicator = anchor_indicator
        self.horizons = horizons or [1, 3, 7, 14]
        self.dgrs = SignIdentifiedCryptoDGRS(anchor_indicator=anchor_indicator)
        self.propagation_matrices: Dict[int, np.ndarray] = {}
        self.propagation_matrices_raw: Dict[int, np.ndarray] = {}
        self.feature_names: List[str] = []
        self.weights: np.ndarray = np.array([])
        self.intercept: float = 0.0
        self.latest_state: float = 0.0

    def fit(self, X_train: pd.DataFrame, y_train: np.ndarray) -> "CryptoFull4DDLMModel":
        self.feature_names = list(X_train.columns)
        p = len(self.feature_names)
        y = np.asarray(y_train, dtype=float)

        # 1. Fit Sign-Identified DGRS state-space model
        self.dgrs.fit(X_train)
        smoothed_means, _, _ = self.dgrs.smooth(X_train)
        self.latest_state = float(smoothed_means[-1]) if len(smoothed_means) > 0 else 0.0

        # 2. Estimate Transition & Structural Propagation Matrices Pi_h
        # Standardized feature matrix
        Z = (X_train.values - self.dgrs.train_mean) / self.dgrs.train_std
        N = len(Z)

        # Contemporaneous covariance / network interaction At
        Sigma = np.cov(Z.T) if N > 2 else np.eye(p)

        # Autoregressive transition matrix Phi (VAR(1) via Ridge regression)
        if N > 5:
            Z_lag = Z[:-1]
            Z_curr = Z[1:]
            # Phi = (Z_lag^T Z_lag + alpha*I)^(-1) Z_lag^T Z_curr
            alpha = 1.0
            Phi = np.linalg.solve(Z_lag.T @ Z_lag + alpha * np.eye(p), Z_lag.T @ Z_curr)
        else:
            Phi = np.eye(p) * 0.90

        # Generalized IRF (Pesaran & Shin 1998):
        # GIRF_j(h) = Phi^h @ Sigma @ e_j / sqrt(sigma_jj)
        # This gives the response of all variables to a one-std-dev shock to variable j at horizon h.
        sigma_diag = np.diag(Sigma).copy()
        sigma_diag[sigma_diag < 1e-8] = 1e-8

        for h in self.horizons:
            Phi_h = np.linalg.matrix_power(Phi, h)

            # Build GIRF matrix: column j = response to shock in variable j
            girf_matrix = np.zeros((p, p))
            for j in range(p):
                e_j = np.zeros(p)
                e_j[j] = 1.0
                girf_matrix[:, j] = Phi_h @ Sigma @ e_j / np.sqrt(sigma_diag[j])

            # Store raw IRF
            self.propagation_matrices_raw[h] = girf_matrix.copy()

            # Normalize each row by its L2 norm for interpretability
            # This produces transmission coefficients in [-1, 1] with diagonal = 1
            row_norms = np.sqrt(np.sum(girf_matrix ** 2, axis=1, keepdims=True))
            row_norms[row_norms < 1e-8] = 1e-8
            normalized = girf_matrix / row_norms
            # Force exact unity on diagonal
            np.fill_diagonal(normalized, 1.0)
            self.propagation_matrices[h] = np.clip(normalized, -1.0, 1.0)

        # 3. Logistic calibration layer mapping (St, Z_t) to shock probability
        # Augment features with latent factor St
        X_aug = np.column_stack([smoothed_means, Z])

        def loss(params):
            b0 = params[0]
            w = params[1:]
            prob = _sigmoid(b0 + X_aug @ w)
            prob = np.clip(prob, 1e-12, 1.0 - 1e-12)
            nll = -np.mean(y * np.log(prob) + (1.0 - y) * np.log(1.0 - prob))
            reg = 0.2 * np.sum(w ** 2)
            return nll + reg

        init_p = np.zeros(X_aug.shape[1] + 1)
        base_rate = np.clip(np.mean(y), 0.01, 0.99)
        init_p[0] = np.log(base_rate / (1.0 - base_rate))
        init_p[1] = 1.0  # Positive initial loading on latent state St

        res = minimize(loss, init_p, method="L-BFGS-B")
        self.intercept = float(res.x[0])
        self.weights = res.x[1:]
        return self

    def predict_proba(self, X_test: pd.DataFrame, horizon: int = 1) -> np.ndarray:
        # Standardize test observation
        X_val = X_test.values
        Z_test = (X_val - self.dgrs.train_mean) / self.dgrs.train_std

        # Estimate test latent state through forward Kalman step
        Lambda = self.dgrs.loadings
        a_pred = float(np.dot(Z_test[-1], Lambda)) if len(Z_test) > 0 else self.latest_state
        # Horizon decay for latent state forward projection
        decay = (self.dgrs.T_transition) ** horizon
        a_proj = a_pred * decay

        X_aug_test = np.column_stack([np.full(len(X_test), a_proj), Z_test])
        logits = self.intercept + X_aug_test @ self.weights
        p = _sigmoid(logits)

        # Structural temporal dampening across longer horizons
        time_decay = np.exp(-0.02 * (horizon - 1))
        return np.clip(p * time_decay + (1.0 - time_decay) * 0.15, 0.01, 0.99)

    def get_propagation_matrix(self, horizon: int = 1) -> np.ndarray:
        """
        Returns Generalized IRF propagation matrix Pi_h for specified horizon.
        """
        if horizon in self.propagation_matrices:
            return self.propagation_matrices[horizon]
        p = len(self.feature_names)
        return np.eye(p)

    def get_raw_propagation_matrix(self, horizon: int = 1) -> np.ndarray:
        """
        Returns the unnormalized GIRF matrix for diagnostic purposes.
        """
        if horizon in self.propagation_matrices_raw:
            return self.propagation_matrices_raw[horizon]
        p = len(self.feature_names)
        return np.eye(p)
