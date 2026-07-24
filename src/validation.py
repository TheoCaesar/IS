EXPECTED_SWARA = {
    "scores": {
        "C1": 1.381,
        "C2": 1.984,
        "C3": 0.712,
        "C4": 1.994,
        "C5": 2.319,
    },
    "weights": {
        "C1": 0.1910,
        "C2": 0.2086,
        "C3": 0.1731,
        "C4": 0.2118,
        "C5": 0.2155,
    },
    "ranking": [
        "C5",
        "C4",
        "C2",
        "C1",
        "C3"
    ]
}

EXPECTED_AGGREGATED = {
    "S1": {
        "C1": (0.51,0.50,0.31),
        "C2": (0.55,0.45,0.35),
        "C3": (0.74,0.26,0.20),
        "C4": (0.85,0.16,0.09),
        "C5": (0.81,0.20,0.16),
    },
    "S2": {
        "C1": (0.83,0.25,0.08),
        "C2": (0.80,0.30,0.10),
        "C3": (0.78,0.33,0.13),
        "C4": (0.83,0.23,0.11),
        "C5": (0.82,0.23,0.14),
    },
    "S3": {
        "C1": (0.55,0.56,0.35),
        "C2": (0.53,0.56,0.38),
        "C3": (0.43,0.65,0.40),
        "C4": (0.74,0.33,0.18),
        "C5": (0.87,0.23,0.07),
    }
}

EXPECTED_PDA = {
    "S1": {
        "C1":0.000,
        "C2":0.000,
        "C3":1.135,
        "C4":1.153,
        "C5":0.655,
    },
    "S2":{
        "C1":2.258,
        "C2":2.198,
        "C3":1.476,
        "C4":0.959,
        "C5":0.720,
    },
    "S3":{
        "C1":0.000,
        "C2":0.000,
        "C3":0.000,
        "C4":0.325,
        "C5":1.093,
    }
}

EXPECTED_NDA = {
    "S1":{
        "C1":0.555,
        "C2":0.255,
        "C3":0.000,
        "C4":0.000,
        "C5":0.000,
    },
    "S2":{
        "C1":0.000,
        "C2":0.000,
        "C3":0.000,
        "C4":0.000,
        "C5":0.000,
    },
    "S3":{
        "C1":0.496,
        "C2":0.568,
        "C3":1.057,
        "C4":0.000,
        "C5":0.000,
    }
}

EXPECTED_RANKING = {
    "S1":0.4927,
    "S2":1.0000,
    "S3":0.1012,
}

def compare(actual, expected, tol=1e-2):
    for key in expected:
        if isinstance(expected[key], dict):
            compare(actual[key], expected[key], tol)
        else:
            diff = abs(actual[key] - expected[key])
            if diff <= tol:
                print(f"✓ {key}: {actual[key]:.4f}")
            else:
                print(
                    f"✗ {key}: "
                    f"{actual[key]:.4f} "
                    f"(expected {expected[key]:.4f})"
                )

def validate_swara(results):
    print("\n========== SF-SWARA ==========\n")
    print("Scores")
    compare(
        results["scores"],
        EXPECTED_SWARA["scores"],
    )
    print("\nRanking")
    if results["ranking"] == EXPECTED_SWARA["ranking"]:
        print("✓ Ranking")
    else:
        print("✗ Ranking")
        print(results["ranking"])
    print("\nWeights")
    compare(
        results["weights"],
        EXPECTED_SWARA["weights"],
    )

def compare_sfn(actual, expected, tol=0.02):
    if (
        abs(actual.mu - expected[0]) <= tol
        and
        abs(actual.nu - expected[1]) <= tol
        and
        abs(actual.pi - expected[2]) <= tol
    ):
        return True
    return False

def validate_aggregation(results):
    print("\n========== SWAM ==========\n")
    matrix = results["decision_matrix"]

    for strategy in EXPECTED_AGGREGATED:
        for criterion in EXPECTED_AGGREGATED[strategy]:
            expected = EXPECTED_AGGREGATED[strategy][criterion]
            actual = matrix[strategy][criterion]

            if compare_sfn(actual, expected):
                print(f"✓ {strategy}-{criterion}")
            else:
                print(
                    f"✗ {strategy}-{criterion}"
                )
                print(
                    actual.mu,
                    actual.nu,
                    actual.pi
                )

def validate_pda(results):
    print("\n========== PDA ==========\n")
    compare(results["pda"], EXPECTED_PDA, tol=0.05 )

def validate_nda(results):
    print("\n========== NDA ==========\n")
    compare(results["nda"],EXPECTED_NDA, tol=0.05 )

def validate_final_scores(results):
    ranking = dict(results["ranking"])
    print("\n========== FINAL ==========\n")
    compare(  ranking,  EXPECTED_RANKING,   tol=0.02 )

def validate(swara_results,  edas_results):
    validate_swara(swara_results)
    validate_aggregation(edas_results)
    validate_pda(edas_results)
    validate_nda(edas_results)
    validate_final_scores(edas_results)
