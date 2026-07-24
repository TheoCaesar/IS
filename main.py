from src.loader import load_all_files, build_lingusitic_lookup
from src.spherical_fuzzy import score
from src.swam import swam
from src.models import SphericalFuzzyNumber
from src.sf_swara import sf_swara


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

def main():
    data = load_all_files();
    lookup = build_lingusitic_lookup(data['linguistic'])
    
    # run_lookup(lookup);
    # run_scores(lookup)
    # test_swam()
    test_swara(data, lookup)

if __name__ == "__main__":
    main()
