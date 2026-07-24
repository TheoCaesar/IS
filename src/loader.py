from pathlib import Path
import pandas as pd

DATA_DIR = Path("data")

def load_csv(filename: str) -> pd.Dataframe:
    return pd.read_csv(DATA_DIR/name)

def load_all_files():
    return {
        "linguistic": load_csv("linguistic_scale.csv"),
        "criteria": load_csv("criteria.csv"),
        "strategies": load_csv("strategies.csv"),
        "criteria_eval": load_csv("criteria_evaluations.csv"),
        "strategy_eval": load_csv("strategy_evaluations.csv"),
    }