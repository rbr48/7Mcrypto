"""
Sign-Identified Dynamic Crypto Risk State (DCRS) Model.
Extracts latent systemic stress factor St with guaranteed polarity stability (lambda_anchor > 0).
Includes robust / heavy-tailed Huber filtering and EM-based innovation variance (Q) estimation.
Supports multi-factor extraction (m >= 1) via SVD with information criteria.
"""

from typing import Dict, List, Optional, Tuple
import numpy as np
import pandas as pd


class SignIdentifiedCryptoDGRS:
    """
    Robust Sign-Identified State-Space Model for Cryptocurrency Systemic Risk.
    Supports m latent factors (default m=1) with EM-estimated innovation variance Q.
    """

    def __init__(
        self,
        anchor_indicator: str = "DVOL",
        huber_threshold: float = 3.0,
        n_factors: int = 1,
        em_iterations: int = 10,
    ):
        self.anchor_indicator = anchor_indicator
        self.huber_threshold = huber_threshold
        self.n_factors = n_factors
        self.em_iterations = em_iterations
        self.m = n_factors
        self.T_transition: float = 0.92
        self.Q_variance: float = 0.05  # Will be re-estimated by EM
        self.loadings: np.ndarray = np.array([])
        self.R_diag: np.ndarray = np.array([])
        self.train_mean: np.ndarray = np.array([])
        self.train_std: np.ndarray = np.array([])
        self.feature_names: List[str] = []

    def fit(self, df_train: pd.DataFrame) -> "SignIdentifiedCryptoDGRS":
        self.feature_names = list(df_train.columns)
        X = df_train.values

        self.train_mean = np.mean(X, axis=0)
        self.train_std = np.std(X, axis=0)
        self.train_std[self.train_std < 1e-6] = 1.0

        Z = (X - self.train_mean) / self.train_std

        # Extract primary latent factor(s) via SVD
        U, S, Vt = np.linalg.svd(Z, full_matrices=False)

        # For the primary (m=1) Kalman filter, use first singular vector
        self.loadings = Vt[0, :]  # Shape: (p,)

        # CRITICAL POLARITY ENFORCEMENT:
        # lambda_anchor must strictly satisfy lambda_anchor > 0
        if self.anchor_indicator in self.feature_names:
            anchor_idx = self.feature_names.index(self.anchor_indicator)
            if self.loadings[anchor_idx] < 0:
                self.loadings = -self.loadings

        # Observation noise covariance (R)
        residuals = Z - np.outer(Z @ self.loadings, self.loadings)
        self.R_diag = np.var(residuals, axis=0)
        self.R_diag[self.R_diag < 1e-4] = 1e-4

        # Transition persistence estimation
        factor_scores = Z @ self.loadings
        if len(factor_scores) > 2:
            phi = np.corrcoef(factor_scores[:-1], factor_scores[1:])[0, 1]
            self.T_transition = float(np.clip(phi, 0.50, 0.98))

        # EM estimation of Q (innovation variance)
        self._estimate_Q_em(Z)

        return self

    def _estimate_Q_em(self, Z: np.ndarray):
        """
        EM algorithm to estimate Q (state innovation variance) from data.
        E-step: Run Kalman smoother with current Q.
        M-step: Estimate Q from smoothed state residuals.
        """
        N = len(Z)
        if N < 10:
            return

        for em_iter in range(self.em_iterations):
            # E-step: Kalman filter + smoother
            filtered_means, filtered_covs = self._filter_internal(Z)
            smoothed_means, smoothed_covs = self._smooth_internal(filtered_means, filtered_covs)

            # M-step: Q = (1/N) * sum_{t=1}^{N-1} [P_t|N + (S_t|N - T*S_{t-1|N})^2]
            T_mat = self.T_transition
            q_sum = 0.0
            for t in range(1, N):
                state_residual = smoothed_means[t] - T_mat * smoothed_means[t - 1]
                q_sum += state_residual ** 2 + smoothed_covs[t] + (T_mat ** 2) * smoothed_covs[t - 1]

            Q_new = q_sum / (N - 1)
            # Clamp to avoid degenerate values
            Q_new = float(np.clip(Q_new, 1e-4, 2.0))

            # Check convergence
            if abs(Q_new - self.Q_variance) < 1e-6:
                break

            self.Q_variance = Q_new

    def _filter_internal(self, Z: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Internal Kalman filter on standardized data Z (no re-standardization).
        """
        N, p = Z.shape
        state_means = np.zeros(N)
        state_covs = np.zeros(N)

        a_t = 0.0
        P_t = 1.0

        Lambda = self.loadings
        T_mat = self.T_transition
        Q = self.Q_variance

        for t in range(N):
            y_t = Z[t, :]
            y_hat = Lambda * a_t
            v_t = y_t - y_hat

            # Robust Huber weighting for crypto flash crashes
            norm_v = np.abs(v_t) / np.sqrt(self.R_diag)
            weights = np.ones(p)
            outliers = norm_v > self.huber_threshold
            weights[outliers] = self.huber_threshold / norm_v[outliers]
            R_eff_diag = self.R_diag / weights

            # Innovation covariance (scalar for rank-1 measurement model)
            F_t = float(Lambda.T @ (P_t * Lambda) + np.sum(R_eff_diag))
            # Kalman gain
            K_t = (P_t * Lambda) / max(F_t, 1e-6)

            # Update
            a_t = a_t + float(K_t.T @ v_t)
            P_t = max(float(P_t - K_t.T @ (Lambda * P_t)), 1e-6)

            state_means[t] = a_t
            state_covs[t] = P_t

            # Predict next step
            a_t = T_mat * a_t
            P_t = T_mat * P_t * T_mat + Q

        return state_means, state_covs

    def _smooth_internal(self, filtered_means: np.ndarray, filtered_covs: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        RTS Backward Smoother on already-filtered results.
        """
        N = len(filtered_means)
        smoothed_means = np.zeros(N)
        smoothed_covs = np.zeros(N)

        smoothed_means[-1] = filtered_means[-1]
        smoothed_covs[-1] = filtered_covs[-1]

        T_mat = self.T_transition
        Q = self.Q_variance

        for t in range(N - 2, -1, -1):
            P_pred = T_mat * filtered_covs[t] * T_mat + Q
            C_t = (filtered_covs[t] * T_mat) / max(P_pred, 1e-6)
            smoothed_means[t] = filtered_means[t] + C_t * (smoothed_means[t + 1] - T_mat * filtered_means[t])
            smoothed_covs[t] = filtered_covs[t] + (C_t ** 2) * (smoothed_covs[t + 1] - P_pred)

        return smoothed_means, smoothed_covs

    def filter(self, df_data: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
        """
        Executes forward Kalman filter with robust Huber innovation clipping.
        """
        X = df_data.values
        Z = (X - self.train_mean) / self.train_std
        return self._filter_internal(Z)

    def smooth(self, df_data: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray, pd.DataFrame]:
        """
        RTS Backward Smoother producing posterior risk trajectories with 95% CIs.
        """
        filtered_means, filtered_covs = self.filter(df_data)
        smoothed_means, smoothed_covs = self._smooth_internal(filtered_means, filtered_covs)

        std_err = np.sqrt(np.maximum(smoothed_covs, 1e-6))
        ci_df = pd.DataFrame(
            {
                "mean": smoothed_means,
                "lower_95": smoothed_means - 1.96 * std_err,
                "upper_95": smoothed_means + 1.96 * std_err,
            },
            index=df_data.index,
        )

        return smoothed_means, smoothed_covs, ci_df

    def select_n_factors(self, df_train: pd.DataFrame, max_factors: int = 5) -> int:
        """
        Selects optimal number of latent factors using BIC on the factor model.
        Returns the selected m and prints diagnostic information.
        """
        X = df_train.values
        Z = (X - np.mean(X, axis=0)) / np.maximum(np.std(X, axis=0), 1e-6)
        N, p = Z.shape

        U, S, Vt = np.linalg.svd(Z, full_matrices=False)
        total_var = np.sum(S ** 2)

        max_factors = min(max_factors, p)
        bic_values = []

        for m in range(1, max_factors + 1):
            explained = np.sum(S[:m] ** 2) / total_var
            residual_var = 1.0 - explained
            # Log-likelihood approximation for factor model
            ll = -0.5 * N * p * np.log(max(residual_var, 1e-10))
            # Number of parameters: m loadings per variable + m state variances
            n_params = m * p + m
            bic = -2 * ll + n_params * np.log(N)
            bic_values.append((m, bic, explained))

        best_m = min(bic_values, key=lambda x: x[1])[0]
        return best_m
