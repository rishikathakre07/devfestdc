import os
import pandas as pd

BASE = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE, "data")

def _read_csv_clean(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    # strip weird header/field spaces from your CSVs (they have trailing spaces)
    df.columns = [c.strip() for c in df.columns]
    for c in df.select_dtypes(include=["object"]).columns:
        df[c] = df[c].astype(str).str.strip()
    return df

def load_restaurants() -> pd.DataFrame:
    return _read_csv_clean(os.path.join(DATA_DIR, "restaurant.csv")).assign(
        latitude=lambda d: pd.to_numeric(d["latitude"], errors="coerce"),
        longitude=lambda d: pd.to_numeric(d["longitude"], errors="coerce")
    )

def load_ngos() -> pd.DataFrame:
    df = _read_csv_clean(os.path.join(DATA_DIR, "ngo.csv")).assign(
        latitude=lambda d: pd.to_numeric(d["latitude"], errors="coerce"),
        longitude=lambda d: pd.to_numeric(d["longitude"], errors="coerce")
    )
    # normalize priority rank
    priority_order = {"urgent": 1, "high": 2, "medium": 3, "low": 4}
    df["priority_rank"] = df["priority"].str.lower().map(priority_order).fillna(5).astype(int)
    return df

def load_volunteers() -> pd.DataFrame:
    df = _read_csv_clean(os.path.join(DATA_DIR, "volunteer.csv")).assign(
        latitude=lambda d: pd.to_numeric(d["latitude"], errors="coerce"),
        longitude=lambda d: pd.to_numeric(d["longitude"], errors="coerce"),
    )
    # availability derived from assigned_status
    df["available"] = df["assigned_status"].str.lower().eq("available")
    return df
