import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load data from the new dataset URL
data_url = "https://raw.githubusercontent.com/esnt/Data/main/Names/popular_names.csv"
data = pd.read_csv(data_url)

# App title
st.title('Baby Names Analysis')

# Sidebar with user input
selected_year = st.sidebar.selectbox('Select a year:', data['year'].unique())

# Filter data for the selected year
filtered_data = data[data['year'] == selected_year]

# Show top 5 baby names by 'n' for both genders
st.header(f'Top 5 Baby Names in {selected_year}')
top_names = (
    filtered_data.groupby(['name', 'sex'])['n']
    .sum()
    .reset_index()
    .sort_values(by='n', ascending=False)
    .head(5)
)
st.bar_chart(top_names.set_index('name'))

# Show least common baby names by 'n' for both genders
st.header(f'Least Common Baby Names in {selected_year}')
least_common_names = (
    filtered_data.groupby(['name', 'sex'])['n']
    .sum()
    .reset_index()
    .sort_values(by='n')
    .head(5)
)
st.bar_chart(least_common_names.set_index('name'))

# User selects a name to see 'n' by year
selected_name = st.sidebar.text_input('Enter a name to see its popularity over time:')
if selected_name:
    st.header(f'Popularity of {selected_name} Over Time')
    name_data = filtered_data[filtered_data['name'] == selected_name]
    if not name_data.empty:
        st.line_chart(name_data.groupby('year')['n'].sum())
    else:
        st.warning(f'{selected_name} not found in the dataset for {selected_year}')

# Main content
st.write('Baby Name Data:')
st.write(filtered_data)
