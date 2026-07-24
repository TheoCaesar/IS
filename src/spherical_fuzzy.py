from .models import SphericalFuzzyNumber
from math import sqrt

# Computes the score value of a spherical fuzzy number - equation A7.
def score(sfn: SphericalFuzzyNumber) -> float:
    return (2 * sfn.mu - sfn.pi) ** 2 - (sfn.nu - sfn.pi) ** 2

# Equation A9 - Euclidean distance between two SFNs.
def euclidean_distance(a: SphericalFuzzyNumber,
                       b: SphericalFuzzyNumber) -> float:

    return sqrt(
        (a.mu - b.mu) ** 2 +
        (a.nu - b.nu) ** 2 +
        (a.pi - b.pi) ** 2
    )

# Computes the accuracy value if required by the paper.
def accuracy(sfn: SphericalFuzzyNumber) -> float:
    pass

# Returns True if the SFN satisfies the spherical fuzzy constraint.
def validate(sfn: SphericalFuzzyNumber) -> bool:
    pass