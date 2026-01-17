import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.title("🚴 Washington D.C. Bike Rental Dashboard")

# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv('train.csv')
    df['datetime'] = pd.to_datetime(df['datetime'])
    df['hour'] = df['datetime'].dt.hour
    df['month'] = df['datetime'].dt.month
    season_map = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
    df['season_name'] = df['season'].map(season_map)
    return df

df = load_data()

# --- 3 INTERACTIVE WIDGETS ---
st.sidebar.header("Filters")
selected_season = st.sidebar.multiselect("Select Season", df['season_name'].unique(), default=df['season_name'].unique())
temp_limit = st.sidebar.slider("Minimum Temperature (°C)", 0, 45, 0)
day_type = st.sidebar.selectbox("Day Type", ["All", "Working Day", "Weekend/Holiday"])

# Apply Filters
filt_df = df[df['season_name'].isin(selected_season)]
filt_df = filt_df[filt_df['temp'] >= temp_limit]
if day_type == "Working Day":
    filt_df = filt_df[filt_df['workingday'] == 1]
elif day_type == "Weekend/Holiday":
    filt_df = filt_df[filt_df['workingday'] == 0]

# --- 5 PLOTS ---
col1, col2 = st.columns(2)
with col1:
    fig1, ax1 = plt.subplots(); sns.lineplot(data=filt_df, x='hour', y='count', ax=ax1); st.pyplot(fig1)
    fig2, ax2 = plt.subplots(); sns.barplot(data=filt_df, x='weather', y='count', ax=ax2); st.pyplot(fig2)
with col2:
    fig3, ax3 = plt.subplots(); sns.scatterplot(data=filt_df, x='temp', y='count', alpha=0.2, ax=ax3); st.pyplot(fig3)
    fig4, ax4 = plt.subplots(); sns.boxplot(data=filt_df, x='season_name', y='count', ax=ax4); st.pyplot(fig4)

fig5, ax5 = plt.subplots(figsize=(10,3)); sns.heatmap(filt_df[['temp', 'humidity', 'windspeed', 'count']].corr(), annot=True, ax=ax5); st.pyplot(fig5)