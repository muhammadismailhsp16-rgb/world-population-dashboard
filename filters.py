import pandas as pd
import numpy as np

def load_data(filepath: str = "data/Population_by_country.xlsx") -> pd.DataFrame:
    """Load and clean the population dataset."""
    df = pd.read_excel(filepath)
    df.columns = [
        "rank", "country", "population_2020", "yearly_change",
        "net_change", "density_km2", "land_area_km2",
        "migrants_net", "fertility_rate", "median_age",
        "urban_pop_pct", "world_share"
    ]
    for col in ["fertility_rate", "median_age", "urban_pop_pct"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    if df["yearly_change"].max() < 1:
        df["yearly_change"] = df["yearly_change"] * 100
    if df["urban_pop_pct"].max() < 1:
        df["urban_pop_pct"] = df["urban_pop_pct"] * 100
    return df

def apply_filters(df, countries, pop_range, categories):
    return df
