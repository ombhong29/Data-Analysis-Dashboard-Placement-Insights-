# dashboard/app.py
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import streamlit as st, sys, os
sys.path.append('..')
from src.preprocessor import clean
from src.data_loader import load_data
from src.analysis import placement_summary

st.set_page_config(
    page_title='Placement Insights',
    layout='wide', page_icon='📊')

st.title('📊 Placement Insights Dashboard')

# Load data
df = clean(load_data())

# Sidebar filters
with st.sidebar:
    st.header('Filters')
    years = st.multiselect('Year',
        sorted(df['year'].unique()),
        default=sorted(df['year'].unique()))
    branches = st.multiselect('Branch',
        df['branch'].unique(),
        default=df['branch'].unique())

df_f = df[df['year'].isin(years) &
          df['branch'].isin(branches)]

# KPI cards
stats = placement_summary(df_f)
c1,c2,c3,c4 = st.columns(4)
c1.metric('Placement Rate', f"{stats['rate']}%")
c2.metric('Avg Package', f"₹{stats['avg_pkg']} LPA")
c3.metric('Highest Package', f"₹{stats['max_pkg']} LPA")
c4.metric('Total Placed', stats['placed'])

# Add after KPI cards in app.py
from src.visualizations import (
    plot_top_companies, plot_skill_demand,
    plot_package_distribution, plot_cgpa_vs_package)
from src.analysis import skill_demand

st.divider()
col1, col2 = st.columns(2)

with col1:
    st.subheader('Top hiring companies')
    st.pyplot(plot_top_companies(df_f[df_f['placed']]))

with col2:
    st.subheader('Most in-demand skills')
    skills = skill_demand(df_f)
    st.pyplot(plot_skill_demand(skills))

col3, col4 = st.columns(2)
with col3:
    st.subheader('Package distribution')
    st.pyplot(plot_package_distribution(df_f[df_f['placed']]))
with col4:
    st.subheader('CGPA vs Package')
    st.pyplot(plot_cgpa_vs_package(df_f[df_f['placed']]))

with st.expander('View raw data'):
    st.dataframe(df_f, use_container_width=True)


    # Add to app.py
from sklearn.ensemble import RandomForestClassifier
import numpy as np

@st.cache_resource
def train_model(df):
    feats = ['cgpa','backlogs']
    df_ml = df.dropna(subset=feats+['placed'])
    df_ml = df_ml.copy()
    df_ml['backlogs'] = df_ml['backlogs'].astype(int)
    X = df_ml[feats]
    y = df_ml['placed'].astype(int)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    return model

model = train_model(df)

with st.sidebar:
    st.divider()
    st.subheader('Placement predictor')
    cgpa_in = st.slider('Your CGPA', 6.0, 10.0, 7.5, 0.1)
    back_in = st.number_input('Backlogs', 0, 5, 0)
    prob = model.predict_proba([[cgpa_in, back_in]])[0][1]
    pct = round(prob * 100, 1)
    color = 'green' if pct >= 70 else 'orange' if pct >= 50 else 'red'
    st.markdown(f'Placement chance: **:{color}[{pct}%]**')


    # Add to app.py — Export section
import io
from src.analysis import branch_stats, skill_demand

st.divider()
st.subheader('Export reports')
e1, e2 = st.columns(2)

with e1:
    # CSV download
    csv = df_f.to_csv(index=False).encode('utf-8')
    st.download_button(
        'Download filtered CSV',
        csv, 'placement_data.csv', 'text/csv')

with e2:
    # Excel download
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as w:
        df_f.to_excel(w, sheet_name='Raw Data', index=False)
        branch_stats(df_f).to_excel(w, sheet_name='Branch Stats', index=False)
        skill_demand(df_f).to_excel(w, sheet_name='Skills', index=False)
    st.download_button(
        'Download Excel Report',
        buffer.getvalue(),
        'placement_report.xlsx',
        'application/vnd.ms-excel')