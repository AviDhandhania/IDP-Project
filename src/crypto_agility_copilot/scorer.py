"""
Crypto-Agility Copilot - Prioritisation & Scoring Engine (Stage 3)
Computes the HNDL Exposure Score per data path, operationalizes Mosca's inequality,
suppresses context-irrelevant findings, and outputs a prioritized migration plan.
"""

from typing import List, Tuple
from .models import DataPath, HNDLScore, ExposureSurface, QuantumVulnerability


class HNDLScoringEngine:
    """Stage 3 Engine: Computes HNDL Exposure Score and orders remediation candidates."""

    def __init__(
        self,
        weight_retention: float = 1.0,
        weight_exposure: float = 1.0,
        weight_algorithm: float = 1.0,
        weight_key_reuse: float = 1.0,
        migration_years: float = 2.0,
        crqc_horizon_years: float = 7.0   # Conservative target: 2026 + 7 = 2033 (or 2027-2029 CII deadline)
    ):
        self.w_r = weight_retention
        self.w_e = weight_exposure
        self.w_a = weight_algorithm
        self.w_k = weight_key_reuse
        self.migration_years = migration_years
        self.crqc_horizon_years = crqc_horizon_years

    def score_data_path(self, path: DataPath) -> HNDLScore:
        """Calculates HNDL score and Mosca status for a given data path."""
        if not path.is_security_relevant:
            return HNDLScore(
                raw_score=0.0,
                normalized_score=0.0,
                retention_factor=0.0,
                exposure_factor=0.0,
                algorithm_factor=0.0,
                key_reuse_factor=0.0,
                urgency_tier="SUPPRESSED",
                mosca_violated=False,
                remediation_recommendation="Suppressed: Non-security context"
            )

        # 1. Retention factor R(p): normalized on a log/saturating scale (up to 30 years)
        r_val = min(30.0, path.retention.retention_years)
        # Give higher weight to observed evidence over inferred priors
        evidence_multiplier = 1.0 if path.retention.observed else 0.8
        retention_factor = (r_val / 30.0) * evidence_multiplier

        # 2. Exposure factor E(p)
        exposure_factor = path.exposure.value

        # 3. Algorithm vulnerability factor A(p)
        algorithm_factor = path.invocation.quantum_vulnerability.value

        # 4. Key-reuse / blast-radius factor K(p)
        key_reuse_factor = min(2.0, 1.0 + 0.1 * (path.key_reuse_count - 1))

        # Composite score
        raw_score = (
            (self.w_r * retention_factor) *
            (self.w_e * exposure_factor) *
            (self.w_a * algorithm_factor) *
            (self.w_k * key_reuse_factor)
        )

        # Normalize score to 0 - 100
        normalized_score = min(100.0, raw_score * 100.0)

        # Mosca's inequality evaluation: x + y > z
        x = path.retention.retention_years
        y = self.migration_years
        z = self.crqc_horizon_years
        mosca_violated = (x + y) > z

        # Urgency classification
        if mosca_violated and (normalized_score >= 15.0 or path.invocation.quantum_vulnerability == QuantumVulnerability.SHOR_BROKEN):
            urgency_tier = "CRITICAL_IMMEDIATE"
            recommendation = (
                f"Mosca's inequality violated (Retention {x:.1f}y + Migration {y:.1f}y > Horizon {z:.1f}y). "
                f"Immediate migration to hybrid FIPS 203 (ML-KEM) required to mitigate HNDL."
            )

        elif normalized_score >= 10.0:
            urgency_tier = "HIGH"
            recommendation = "High HNDL exposure. Schedule hybrid migration in next engineering sprint."
        elif normalized_score >= 1.0:
            urgency_tier = "MEDIUM"
            recommendation = "Moderate exposure. Include in annual quantum-readiness roadmap."
        else:
            urgency_tier = "LOW"
            recommendation = "Low exposure or short-lived data. Defer migration."

        return HNDLScore(
            raw_score=raw_score,
            normalized_score=round(normalized_score, 2),
            retention_factor=round(retention_factor, 4),
            exposure_factor=round(exposure_factor, 2),
            algorithm_factor=round(algorithm_factor, 2),
            key_reuse_factor=round(key_reuse_factor, 2),
            urgency_tier=urgency_tier,
            mosca_violated=mosca_violated,
            remediation_recommendation=recommendation
        )

    def rank_paths(self, paths: List[DataPath]) -> List[Tuple[DataPath, HNDLScore]]:
        """Scores and ranks data paths in descending order of HNDL Exposure."""
        scored = [(p, self.score_data_path(p)) for p in paths]
        # Sort by:
        # 1. Non-suppressed first
        # 2. Mosca violation boolean (True first)
        # 3. Normalized score descending
        scored.sort(
            key=lambda item: (
                item[1].urgency_tier != "SUPPRESSED",
                item[1].mosca_violated,
                item[1].normalized_score
            ),
            reverse=True
        )
        return scored
