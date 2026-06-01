import pandas as pd
import numpy as np

def load_data(filepath: str = "data/Population_by_country.xlsx") -> pd.DataFrame:
    try:
        df = pd.read_excel(filepath, engine='openpyxl')
    except:
        df = pd.read_excel(filepath, engine='xlrd')
    
    df.columns = range(len(df.columns))
    df = df.rename(columns={
        0: "rank", 1: "country", 2: "population_2020",
        3: "yearly_change", 4: "net_change", 5: "density_km2",
        6: "land_area_km2", 7: "migrants_net", 8: "fertility_rate",
        9: "median_age", 10: "urban_pop_pct", 11: "world_share"
    })
    return df

def apply_filters(df, countries=None, pop_range=None, categories=None):
    return df
