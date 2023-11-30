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

# Calculate the top 10 baby names by 'n' for both genders
top_names = (
    filtered_data.groupby(['name', 'sex'])['n']
    .sum()
    .reset_index()
    .sort_values(by=['sex', 'n'], ascending=[True, False])
    .groupby('sex')
    .head(10)
    .sort_values(by=['sex', 'n'], ascending=[True, False])
)

# Calculate the least common 10 baby names by 'n' for both genders
least_common_names = (
    filtered_data.groupby(['name', 'sex'])['n']
    .sum()
    .reset_index()
    .sort_values(by=['sex', 'n'])
    .groupby('sex')
    .head(10)
    .sort_values(by=['sex', 'n'])
)

# Create bar charts for the top 10 and least common 10 baby names by 'n'
fig, ax = plt.subplots(2, 1, figsize=(10, 12))
colors = ['b', 'g', 'r', 'c', 'm', 'y', 'tab:blue', 'tab:orange', 'tab:green', 'tab:red']

# Function to label the x-axis with rank
def add_rank_labels(ax, data):
    for i, (_, row) in enumerate(data.iterrows()):
        ax.text(i, row['n'], f'{i + 1}', ha='center', va='bottom', fontsize=10)

# Top 10 names for both genders
ax[0].bar(top_names.index, top_names['n'], color=colors, label=top_names['sex'])
ax[0].set_xticks(range(len(top_names)))
ax[0].set_xticklabels([])
add_rank_labels(ax[0], top_names)

# Least common 10 names for both genders
ax[1].bar(least_common_names.index, least_common_names['n'], color=colors, label=least_common_names['sex'])
ax[1].set_xticks(range(len(least_common_names)))
ax[1].set_xticklabels([])
add_rank_labels(ax[1], least_common_names)

# Set y-axis label
ax[0].set_ylabel('Count (n)')
ax[1].set_ylabel('Count (n)')

# Set chart titles
ax[0].set_title(f'Top 10 Baby Names in {selected_year}')
ax[1].set_title(f'Least Common 10 Baby Names in {selected_year}')

# Display the charts
st.pyplot(fig)

# User selects a name to see 'n' by year
selected_name = st.sidebar.text_input('Enter a name to see its popularity over time:')
if selected_name:
    st.header(f'Popularity of {selected_name} Over Time')
    name_data = data[data['name'] == selected_name]
    if not name_data.empty:
        st.line_chart(name_data.groupby(['year', 'sex'])['n'].sum().unstack().fillna(0))
    else:
        st.warning(f'{selected_name} not found in the dataset')

# Main content
st.write('Here is some data:')
st.write(filtered_data)
