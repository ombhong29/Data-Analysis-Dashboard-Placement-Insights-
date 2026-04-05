# src/analysis.py
import pandas as pd
from collections import Counter

def placement_summary(df):
    placed = df[df['placed']]
    return {
      'total': len(df),
      'placed': len(placed),
      'rate': round(len(placed)/len(df)*100, 1),
      'avg_pkg': round(placed['package_lpa'].mean(), 2),
      'max_pkg': round(placed['package_lpa'].max(), 2),
    }

def skill_demand(df):
    skills = [s for lst in df[df['placed']]['skills_list'] for s in lst]
    counts = Counter(skills)
    return pd.DataFrame(counts.items(),
      columns=['skill','count']).sort_values('count',ascending=False)

def branch_stats(df):
    return df[df['placed']].groupby('branch').agg(
      avg_pkg=('package_lpa','mean'),
      count=('student_id','count'),
      max_pkg=('package_lpa','max')
    ).reset_index().round(2)