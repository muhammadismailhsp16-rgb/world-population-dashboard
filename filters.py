"""
filters.py — Data loading, cleaning, and filtering functions
"""

import pandas as pd
import numpy as np


def load_data(filepath: str = "data/Population_by_country.xlsx") -> pd.DataFrame:
    """Load and clean the population dataset."""
    df = pd.read_excel(filepath)

    # Rename columns for cleanliness
    df.columns = [
        "rank", "country", "population_2020", "yearly_change",
        "net_change", "density_km2", "land_area_km2",
        "migrants_net", "fertility_rate", "median_age",
        "urban_pop_pct", "world_share"
    ]

    # Convert object columns to numeric
    for col in ["fertility_rate", "median_age", "urban_pop_pct"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Convert percentages stored as fractions to actual percent
    if df["yearly_change"].max() < 1:
        df["yearly_change"] = df["yearly_change"] * 100
    if df["urban_pop_pct"].max() <= 1:
        df["urban_pop_pct"] = df["urban_pop_pct"] * 100
    if df["world_share"].max() <= 1:
        df["world_share"] = df["world_share"] * 100

    # Derive population size category
    bins = [0, 1e6, 10e6, 50e6, 100e6, 500e6, 2e9]
    labels = ["<1M", "1M–10M", "10M–50M", "50M–100M", "100M–500M", ">500M"]
    df["pop_category"] = pd.cut(df["population_2020"], bins=bins, labels=labels)

    # Derive migration direction
    df["migration_dir"] = df["migrants_net"].apply(
        lambda x: "Positive" if pd.notna(x) and x > 0
        else ("Negative" if pd.notna(x) and x < 0 else "Neutral/Unknown")
    )

    return df


def apply_filters(
    df: pd.DataFrame,
    search_text: str = "",
    pop_range: tuple = None,
    pop_categories: list = None,
    migration_dirs: list = None,
    density_range: tuple = None,
) -> pd.DataFrame:
    """Apply all sidebar filters to the dataframe and return filtered copy."""
    filtered = df.copy()

    # Text search
    if search_text:
        filtered = filtered[
            filtered["country"].str.contains(search_text, case=False, na=False)
        ]

    # Population range
    if pop_range:
        filtered = filtered[
            (filtered["population_2020"] >= pop_range[0]) &
            (filtered["population_2020"] <= pop_range[1])
        ]

    # Population category multi-select
    if pop_categories:
        filtered = filtered[filtered["pop_category"].isin(pop_categories)]

    # Migration direction multi-select
    if migration_dirs:
        filtered = filtered[filtered["migration_dir"].isin(migration_dirs)]

    # Density range
    if density_range:
        filtered = filtered[
            (filtered["density_km2"] >= density_range[0]) &
            (filtered["density_km2"] <= density_range[1])
        ]

    return filtered
