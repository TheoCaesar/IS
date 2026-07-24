from src.loader import load_all_files, build_lingusitic_lookup

def main():
    data = load_all_files();
    lookup = build_lingusitic_lookup(data['linguistic'])

    print("Loaded linguistic terms:")

    for key, value in lookup.items():
        print(key, value)


if __name__ == "__main__":
    main()
