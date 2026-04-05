# src/data_loader.py
import pandas as pd
import os

def load_data(filepath: str = 'data/raw/placements.csv') -> pd.DataFrame:
    if not os.path.exists(filepath):
        raise FileNotFoundError(f'Dataset not found: {filepath}')
    df = pd.read_csv(filepath)
    print(f'Loaded {len(df)} records, {df.shape[1]} columns')
    return df

if __name__ == '__main__':
    df = load_data()
    print(df.head())