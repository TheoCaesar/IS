from .swam import swam
from .fuzzy import score


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
    pass


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
    pass


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
    pass


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
    pass


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
    pass


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
    pass


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
    pass


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