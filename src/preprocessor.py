# src/preprocessor.py
import pandas as pd

def clean(df: pd.DataFrame) -> pd.DataFrame:
    df = df.drop_duplicates()
    df['package_lpa'].fillna(df['package_lpa'].median(), inplace=True)
    df['cgpa'] = df['cgpa'].clip(0, 10)
    df['placed'] = df['placed'].astype(bool)
    df['skills_list'] = df['skills'].str.split(', ')

    bins   = [0, 5, 10, 20, float('inf')]
    labels = ['0-5 LPA','5-10 LPA','10-20 LPA','20+ LPA']
    df['package_band'] = pd.cut(df['package_lpa'],
                                bins=bins, labels=labels)
    return df

if __name__ == '__main__':
    from data_loader import load_data
    df = clean(load_data())
    print(df.dtypes)
    print(df['package_band'].value_counts())