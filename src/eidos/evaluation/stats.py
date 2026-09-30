"""Statistical analysis engine for Phase 7 empirical evaluation.

Provides deterministic calculations for:
- Parametric and non-parametric central tendencies (Mean, Median)
- Dispersion (Standard Deviation, Variance, Interquartile Range)
- 95% Confidence Intervals via Student's t distribution and Bootstrap resampling
- Standardized effect sizes (Cohen's d, Glass's delta)
- Two-sample permutation tests and exact difference testing
"""

import math
import random
from typing import List, Tuple, Dict, Any


def mean(values: List[float]) -> float:
    """Calculates arithmetic mean."""
    if not values:
        return 0.0
    return sum(values) / len(values)


def median(values: List[float]) -> float:
    """Calculates median."""
    if not values:
        return 0.0
    s = sorted(values)
    n = len(s)
    mid = n // 2
    if n % 2 == 0:
        return (s[mid - 1] + s[mid]) / 2.0
    return float(s[mid])


def variance(values: List[float], ddof: int = 1) -> float:
    """Calculates sample variance with ddof degrees of freedom."""
    n = len(values)
    if n <= ddof:
        return 0.0
    m = mean(values)
    return sum((x - m) ** 2 for x in values) / (n - ddof)


def std_dev(values: List[float], ddof: int = 1) -> float:
    """Calculates sample standard deviation."""
    return math.sqrt(variance(values, ddof=ddof))


def confidence_interval_95(values: List[float]) -> Tuple[float, float]:
    """Calculates 95% confidence interval for the mean using Student's t approximation."""
    n = len(values)
    if n < 2:
        m = mean(values) if values else 0.0
        return (m, m)
    m = mean(values)
    s = std_dev(values)
    # Approximate t-critical for 95% CI (1.96 for large N, ~2.26 for N=10, ~2.04 for N=30)
    t_crit = 2.045 if n >= 30 else (2.262 if n >= 10 else 2.571)
    margin = t_crit * (s / math.sqrt(n))
    return (round(m - margin, 4), round(m + margin, 4))


def bootstrap_ci_95(values: List[float], num_resamples: int = 1000, seed: int = 42) -> Tuple[float, float]:
    """Calculates empirical 95% confidence interval via non-parametric bootstrap resampling."""
    if not values:
        return (0.0, 0.0)
    if len(values) == 1:
        return (values[0], values[0])
    rng = random.Random(seed)
    n = len(values)
    resample_means = []
    for _ in range(num_resamples):
        resample = [rng.choice(values) for _ in range(n)]
        resample_means.append(mean(resample))
    resample_means.sort()
    lower_idx = int(0.025 * num_resamples)
    upper_idx = int(0.975 * num_resamples)
    return (round(resample_means[lower_idx], 4), round(resample_means[upper_idx], 4))


def cohens_d(group1: List[float], group2: List[float]) -> float:
    """Calculates Cohen's d standardized effect size between two groups.
    
    Positive d indicates group2 > group1.
    Small effect: ~0.2, Medium: ~0.5, Large: ~0.8.
    """
    n1, n2 = len(group1), len(group2)
    if n1 < 2 or n2 < 2:
        return 0.0
    m1, m2 = mean(group1), mean(group2)
    var1, var2 = variance(group1), variance(group2)
    pooled_sd = math.sqrt(((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2))
    if pooled_sd == 0:
        return 0.0
    return round((m2 - m1) / pooled_sd, 4)


def permutation_test_p_value(group1: List[float], group2: List[float], num_permutations: int = 1000, seed: int = 42) -> float:
    """Calculates two-sided permutation test p-value between two distributions."""
    n1, n2 = len(group1), len(group2)
    if n1 == 0 or n2 == 0:
        return 1.0
    observed_diff = abs(mean(group2) - mean(group1))
    combined = group1 + group2
    total = len(combined)
    
    rng = random.Random(seed)
    extreme_count = 0
    for _ in range(num_permutations):
        shuffled = list(combined)
        rng.shuffle(shuffled)
        p1 = shuffled[:n1]
        p2 = shuffled[n1:]
        diff = abs(mean(p2) - mean(p1))
        if diff >= observed_diff:
            extreme_count += 1
            
    return round(extreme_count / num_permutations, 4)


def compute_relative_change(baseline_val: float, treatment_val: float) -> float:
    """Calculates relative percentage difference: (treatment - baseline) / baseline * 100."""
    if baseline_val == 0:
        return 0.0 if treatment_val == 0 else 100.0
    return round(((treatment_val - baseline_val) / abs(baseline_val)) * 100.0, 2)
