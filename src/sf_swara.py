from .swam import swam
from .spherical_fuzzy import score


def sf_swara(criteria_df, evaluations_df, lookup, expert_weights):
    """
        Implements the Spherical Fuzzy SWARA procedure
        (Equations A10–A15).

        Parameters
        ----------
        criteria_df : pd.DataFrame          Criteria information.
        evaluations_df : pd.DataFrame       Expert linguistic evaluations.
        lookup : dict                       Linguistic term -> SphericalFuzzyNumber
        expert_weights : list[float]        Weights of the experts.

        Returns
        -------
        dict                                Intermediate results and final criterion weights.
    """
    # ==========================================================
    # Equation A10     # Aggregate expert opinions using SWAM
    # ==========================================================

    aggregated = {}

    for _, row in evaluations_df.iterrows():
        criterion = row["criterion"]
        sfns = [
            lookup[row["E1"]],
            lookup[row["E2"]],
            lookup[row["E3"]],
            lookup[row["E4"]],
        ]
        aggregated[criterion] = swam(
            sfns,
            expert_weights
        )

    # ==========================================================
    # Equation A11     # Compute score values
    # ==========================================================

    scores = {}

    for criterion, sfn in aggregated.items():
        scores[criterion] = score(sfn)

    # ==========================================================
    # Equation A12    # Rank criteria
    # ==========================================================

    ranking = sorted(
        scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    comparative_importance = [0]

    for i in range(1, len(ranking)):
        previous_score = ranking[i - 1][1]
        current_score = ranking[i][1]

        comparative_importance.append(  previous_score - current_score )

    # ==========================================================
    # Equation A13    # Comparative coefficients
    # ==========================================================

    comparative_coefficients = []
    for i, value in enumerate(comparative_importance):
        if i == 0:
            comparative_coefficients.append(1)
        else:
            comparative_coefficients.append( value + 1  )

    # ==========================================================
    # Equation A14    # SF weights
    # ==========================================================
    sf_weights = [1]
    for i in range(1, len(comparative_coefficients)):
        sf_weights.append(
            sf_weights[-1] /
            comparative_coefficients[i]
        )
    # ==========================================================
    # Equation A15     # Normalize weights
    # ==========================================================
    total = sum(sf_weights)
    normalized_weights = [
        value / total
        for value in sf_weights
    ]

    criterion_weights = {}

    for (criterion, _), weight in zip(ranking,  normalized_weights ):
        criterion_weights[criterion] = weight

    # ==========================================================
    # Return all intermediate results
    # ==========================================================
    return {
        "aggregated": aggregated,
        "scores": scores,
        "ranking": ranking,
        "comparative_importance": comparative_importance,
        "comparative_coefficients": comparative_coefficients,
        "sf_weights": sf_weights,
        "weights": criterion_weights,
    }