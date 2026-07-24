from math import prod, sqrt
from .models import SphericalFuzzyNumber

# Computes Π(value_i ^ weight_i): used repeatedly in the SWAM equation.
def weighted_product(values, weights):

    return prod(
        value ** weight
        for value, weight in zip(values, weights)
    )

def swam( sfns: list[SphericalFuzzyNumber],  weights: list[float]) -> SphericalFuzzyNumber:
    if len(sfns) != len(weights):
        raise ValueError("Mismatch between SFNs and weights.")

    if len(sfns) != len(weights):
        raise ValueError("Mismatch between SFNs and weights.")
    
    if abs(sum(weights) - 1.0) > 1e-9:
        raise ValueError("Weights must sum to 1.")

    mus = [x.mu for x in sfns]
    nus = [x.nu for x in sfns]
    pis = [x.pi for x in sfns]

    # Membership
    mu_term = weighted_product(
        [1 - (m ** 2) for m in mus],
        weights
    )

    mu = sqrt(1 - mu_term)

    # Non-membership
    nu = weighted_product(nus, weights)

    # Hesitancy
    pi_left = weighted_product(
        [1 - (m ** 2) for m in mus],
        weights
    )

    pi_right = weighted_product(
        [1 - (m ** 2) - (p ** 2)
        for m, p in zip(mus, pis)],
        weights
    )

    pi = sqrt(
        pi_left - pi_right
    )
    return SphericalFuzzyNumber(
        mu=mu,
        nu=nu,
        pi=pi
    )