# src/data_generator.py
import pandas as pd, numpy as np, random
np.random.seed(42)
n = 500

companies = ['Google','Microsoft','Infosys','TCS',
             'Amazon','Wipro','Deloitte','Accenture']
branches  = ['CSE','ECE','Mechanical','Civil','IT','EEE']
skills_pool = ['Python','ML','SQL','Java','React',
               'AWS','DSA','Excel','Power BI','Communication']

df = pd.DataFrame({
  'student_id':      range(1, n+1),
  'year':            np.random.choice([2021,2022,2023,2024], n),
  'branch':          np.random.choice(branches, n),
  'cgpa':            np.round(np.random.uniform(6.0,9.5,n),2),
  'company':         np.random.choice(companies, n),
  'package_lpa':     np.round(np.random.uniform(3.5,42.0,n),2),
  'placement_type':  np.random.choice(['On-Campus','Off-Campus'],n),
  'placed':          np.random.choice([True,False],n,p=[0.78,0.22]),
  'skills':          [', '.join(random.sample(skills_pool,
                      k=random.randint(2,5))) for _ in range(n)],
  'backlogs':        np.random.choice([0,1,2],n,p=[0.75,0.18,0.07]),
})
df.to_csv('data/raw/placements.csv', index=False)
print(f'Created {len(df)} records')