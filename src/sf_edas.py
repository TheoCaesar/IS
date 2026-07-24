from .swam import swam
from .spherical_fuzzy import score


def aggregate_decision_matrix(
    strategy_evaluations_df,
    lookup,
    expert_weights
):
    """
    Equations A16–A18
    Build the aggregated spherical fuzzy decision matrix
    using the SWAM operator.

    Returns
    -------
    dict
        {
            strategy:
            {
                criterion: SphericalFuzzyNumber
            }
        }
    """
    decision_matrix = {}

    for _, row in strategy_evaluations_df.iterrows():

        strategy = row["strategy"]
        criterion = row["criterion"]

        sfns = [
            lookup[row["E1"]],
            lookup[row["E2"]],
            lookup[row["E3"]],
            lookup[row["E4"]],
        ]

        aggregated = swam(
            sfns,
            expert_weights
        )

        if strategy not in decision_matrix:
            decision_matrix[strategy] = {}

        decision_matrix[strategy][criterion] = aggregated

    return decision_matrix


def average_solution(decision_matrix):
    """
    Equation A19

    Compute the average solution for each criterion
    across all alternatives.

    Returns
    -------
    dict
        criterion -> average SFN
    """

    average = {}

    first_strategy = next(iter(decision_matrix))
    criteria = decision_matrix[first_strategy].keys()

    for criterion in criteria:

        sfns = []

        for strategy in decision_matrix:
            sfns.append(
                decision_matrix[strategy][criterion]
            )

        weights = [1 / len(sfns)] * len(sfns)

        average[criterion] = swam(
            sfns,
            weights
        )

    return average

def score_matrix(decision_matrix):
    """
    Equation A24

    Convert each aggregated SFN into a
    non-negative score matrix.

    Returns
    -------
    dict
        strategy -> criterion -> score
    """
    scores = {}

    for strategy in decision_matrix:

        scores[strategy] = {}

        for criterion, sfn in decision_matrix[strategy].items():
            scores[strategy][criterion] = score(sfn)
            # scores[strategy][criterion] = max(
            #     0,
            #     score(sfn)
            # )

    return scores


def pda_nda(
    score_matrix,
    average_scores,
    criterion_types
):
    """
    Equations A20–A23

    Compute

    Positive Distance from Average (PDA)

    Negative Distance from Average (NDA)

    Returns
    -------
    PDA, NDA
    """
    pda = {}
    nda = {}

    for strategy in score_matrix:

        pda[strategy] = {}
        nda[strategy] = {}

        for criterion in score_matrix[strategy]:

            T = score_matrix[strategy][criterion]
            AV = average_scores[criterion]

            if criterion_types[criterion] == "benefit":

                pda[strategy][criterion] = max(
                    0,
                    T - AV
                ) / AV

                nda[strategy][criterion] = max(
                    0,
                    AV - T
                ) / AV

            else:

                pda[strategy][criterion] = max(
                    0,
                    AV - T
                ) / AV

                nda[strategy][criterion] = max(
                    0,
                    T - AV
                ) / AV

    return pda, nda


def weighted_sums(
    pda,
    nda,
    criterion_weights
):
    """
    Equations A25–A26

    Compute weighted PDA and NDA for
    every strategy.

    Returns
    -------
    P_plus
    N_minus
    """

    P_plus = {}
    N_minus = {}

    for strategy in pda:

        p = 0
        n = 0

        for criterion in pda[strategy]:

            weight = criterion_weights[criterion]

            p += weight * pda[strategy][criterion]
            n += weight * nda[strategy][criterion]

        P_plus[strategy] = p
        N_minus[strategy] = n

    return P_plus, N_minus


def normalize_scores(
    p_plus,
    n_minus
):
    """
    Equations A27–A28

    Normalize the weighted sums.

    Returns
    -------
    normalized_p
    normalized_n
    """

    normalized_p = {}
    normalized_n = {}

    max_p = max(p_plus.values())
    max_n = max(n_minus.values())

    for strategy in p_plus:

        if max_p == 0:
            normalized_p[strategy] = 0
        else:
            normalized_p[strategy] = (
                p_plus[strategy] / max_p
            )

        if max_n == 0:
            normalized_n[strategy] = 1
        else:
            normalized_n[strategy] = (
                1 - (n_minus[strategy] / max_n)
            )

    return normalized_p, normalized_n


def appraisal_scores(
    normalized_p,
    normalized_n
):
    """
    Equation A29

    Compute appraisal scores and
    rank alternatives.

    Returns
    -------
    dict
    """
    results = {}

    for strategy in normalized_p:

        results[strategy] = (
            normalized_p[strategy]
            +
            normalized_n[strategy]
        ) / 2

    ranking = sorted(
        results.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return ranking

def sf_edas(
    strategy_evaluations_df,
    lookup,
    expert_weights,
    criterion_weights,
    criterion_types
):
    """
    Complete SF-EDAS pipeline.

    Executes Equations A16–A29.
    """

    decision_matrix = aggregate_decision_matrix(
        strategy_evaluations_df,
        lookup,
        expert_weights
    )

    average = average_solution(
        decision_matrix
    )

    scores = score_matrix(
        decision_matrix
    )

    average_scores = {
        criterion: score(sfn)
        for criterion, sfn in average.items()
    }

    pda, nda = pda_nda(
        scores,
        average_scores,
        criterion_types
    )

    p_plus, n_minus = weighted_sums(
        pda,
        nda,
        criterion_weights
    )

    normalized_p, normalized_n = normalize_scores(
        p_plus,
        n_minus
    )

    ranking = appraisal_scores(
        normalized_p,
        normalized_n
    )

    return {
        "decision_matrix": decision_matrix,
        "average_solution": average,
        "score_matrix": scores,
        "average_scores": average_scores,
        "pda": pda,
        "nda": nda,
        "p_plus": p_plus,
        "n_minus": n_minus,
        "normalized_p": normalized_p,
        "normalized_n": normalized_n,
        "ranking": ranking,
    }