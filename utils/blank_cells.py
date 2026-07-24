import pandas as pd

for f in [
    "criteria_evaluations.csv",
    "strategy_evaluations.csv",
    "linguistic_scale.csv",
    "criteria.csv",
    "strategies.csv",
]:
    df = pd.read_csv(f"data/{f}")
    print(f"{f}:")
    print(df.isnull().sum())
    print("-" * 30)