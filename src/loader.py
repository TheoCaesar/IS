from pathlib import Path
from src.models import SphericalFuzzyNumber
import pandas as pd

DATA_DIR = Path("data")

def load_csv(filename: str) -> pd.Dataframe:
    return pd.read_csv(DATA_DIR/filename)

def load_all_files():
    return {
        "linguistic": load_csv("linguistic_scale.csv"),
        "criteria": load_csv("criteria.csv"),
        "strategies": load_csv("strategies.csv"),
        "criteria_eval": load_csv("criteria_evaluations.csv"),
        "strategy_eval": load_csv("strategy_evaluations.csv"),
    }


#lookup table
def build_lingusitic_lookup(dataframe):
    lookup = {}

    for _, row in dataframe.iterrows():
        lookup[row['abbreviation']] = SphericalFuzzyNumber(
            mu = float(row['mu']),
            nu = float(row['nu']),
            pi = float(row['pi']),
        )
    return lookup