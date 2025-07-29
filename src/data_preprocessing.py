import pandas as pd

def load_data(filepath: str) -> pd.DataFrame:
    return pd.read_csv(filepath)

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df['last_update'] = pd.to_datetime(df['last_update'], dayfirst=True, errors='coerce')
    df = df.dropna(subset=['last_update'])
    pivot_df = df.pivot_table(
        index=['country', 'state', 'city', 'station', 'latitude', 'longitude', 'last_update'],
        columns='pollutant_id',
        values='pollutant_avg'
    ).reset_index()
    pivot_df = pivot_df.dropna()
    return pivot_df

def save_clean_data(df: pd.DataFrame, output_path: str):
    df.to_csv(output_path, index=False)
