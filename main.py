from src.loader import load_all_files, build_lingusitic_lookup
from src.spherical_fuzzy import score
from src.swam import swam
from src.models import SphericalFuzzyNumber
from src.sf_swara import sf_swara
from src.sf_edas import sf_edas


def run_lookup(lookup: {}):

    print("\n***********************************")
    print("        Loaded linguistic terms:")
    print("***********************************")


    for key, value in lookup.items():
        print(key, value)

def run_scores(lookup: {}):
    print("\n***********************************")
    print("    Score Values:")
    print("***********************************")

    for name, sfn in lookup.items():
        print(f"{name:3} -> {score(sfn):.6f}")  

def test_swam():
    sfns = [
        SphericalFuzzyNumber(0.6, 0.4, 0.3),
        SphericalFuzzyNumber(0.6, 0.4, 0.3),
        SphericalFuzzyNumber(0.9, 0.1, 0.0),
        SphericalFuzzyNumber(0.2, 0.8, 0.1),
    ]

    weights = [0.25, 0.25, 0.25, 0.25]

    result = swam(sfns, weights)
    print("\n***********************************")
    print("    Testing Swam")
    print("***********************************")
    print(result)

def test_swara(data, lookup):
    # print(data["criteria"])
    criteria_df = data["criteria"]
    evaluations_df = data["criteria_eval"]
    ### assume equal expertise of witness
    expert_weights = [0.25, 0.25, 0.25, 0.25] 
    
    results = sf_swara(
        criteria_df,
        evaluations_df,
        lookup,
        expert_weights
    )

    print("\n***********************************")
    print("        SF-SWARA Results")
    print("*************************************")

    print("\nAggregated SFNs")
    for criterion, value in results["aggregated"].items():
        print(f"{criterion}: {value}")

    print("\nScores")
    for criterion, value in results["scores"].items():
        print(f"{criterion}: {value:.6f}")

    print("\nRanking")
    for item in results["ranking"]:
        print(item)

    print("\nNormalized Weights")
    for criterion, weight in results["weights"].items():
        print(f"{criterion}: {weight:.6f}")

def test_edas(data, lookup):
    expert_weights = [0.25, 0.25, 0.25, 0.25]
    criteria_df = data["criteria"]
    criteria_evaluations_df = data["criteria_eval"]
    strategy_evaluations_df = data["strategy_eval"]

    swara_results = sf_swara(
        criteria_df,
        criteria_evaluations_df,
        lookup,
        expert_weights
    )

    criterion_weights = swara_results["weights"]

    criterion_types = {
        "C1": "benefit",
        "C2": "benefit",
        "C3": "benefit",
        "C4": "benefit",
        "C5": "benefit",
    }

    edas_results = sf_edas(
        strategy_evaluations_df,
        lookup,
        expert_weights,
        criterion_weights,
        criterion_types
    )
    # ========================================================================
    # print(swara_results["weights"])
    # print()
    # print(edas_results["average_scores"] )
    # print()
    # print(edas_results["p_plus"])
    # print()
    # print(edas_results["n_minus"])
    # print()
    # print(edas_results["normalized_p"])
    # print()
    # print(edas_results["normalized_n"])
    # print()
    # print(edas_results["ranking"])
    # # ========================================================================

    print("\n=== Criterion Weights ===")
    for c, w in criterion_weights.items():
        print(c, round(w, 6))

    print("\n=== Average Scores ===")
    for c, s in edas_results["average_scores"].items():
        print(c, round(s, 6))

    print("\n=== PDA ===")
    print(edas_results["pda"])

    print("\n=== NDA ===")
    print(edas_results["nda"])

    print("\n=== P+ ===")
    print(edas_results["p_plus"])

    print("\n=== N- ===")
    print(edas_results["n_minus"])

    print("\n=== Final Ranking ===")
    for strategy, score in edas_results["ranking"]:
        print(f"{strategy}: {score:.6f}")

def main():
    data = load_all_files();
    lookup = build_lingusitic_lookup(data['linguistic'])
    
    # run_lookup(lookup);
    # run_scores(lookup)
    # test_swam()
    # test_swara(data, lookup)
    test_edas(data, lookup);

if __name__ == "__main__":
    main()
