from src.loader import load_all_files, build_lingusitic_lookup
from src.spherical_fuzzy import score


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


def main():
    data = load_all_files();
    lookup = build_lingusitic_lookup(data['linguistic'])
    
    run_lookup(lookup);
    run_scores(lookup)

if __name__ == "__main__":
    main()
