import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data from the dataset URL
data_url = "https://raw.githubusercontent.com/esnt/Data/main/Names/popular_names.csv"
data = pd.read_csv(data_url)

# Streamlit app title and description
st.title("Popular Names")
st.header("Top Baby Names Analysis")

# Filter data by year
selected_year = st.slider("Select a year:", min_value=1910, max_value=2021, value=1910, step=1)

# User input for the name
selected_name = st.text_input(f"Enter a name to see popularity over time in {selected_year}:")

# Create a subplot with two plots
fig, axes = plt.subplots(2, 1, figsize=(18, 18), gridspec_kw={'height_ratios': [5, 6]})

# Define color palette
palette = sns.color_palette("husl")

# Calculate the popularity of the selected name over time
if selected_name:
    name_data = data[(data['name'] == selected_name)]
    if not name_data.empty:
        # Create a plot for popularity over time
        sns.lineplot(
            data=name_data,
            x='year',
            y='n',
            hue='sex',
            palette=palette[:2],  # Use the first two colors for females and males
            ax=axes[0]
        )
        axes[0].set_title(f'Popularity of {selected_name} Over Time')
        axes[0].set_xlabel('Year')
        axes[0].set_ylabel('Count (n)')
        # Set fixed x-axis limits
        axes[0].set_xlim(1910, 2021)
    else:
        st.warning(f"Name '{selected_name}' not found in the dataset.")
else:
    axes[0].set_visible(False)

# Calculate the top 10 baby names by 'n' for both genders for the selected year
data_selected_year = data[data['year'] == selected_year]
top_names_selected_year = (
    data_selected_year.groupby(['name', 'sex'])['n']
    .sum()
    .reset_index()
    .sort_values(by='n', ascending=False)
    .groupby('sex')
    .head(10)
    .sort_values(by='n', ascending=False)
)

# Create bar chart for top baby names for females and males
sns.barplot(
    data=top_names_selected_year,
    x='name',
    y='n',
    hue='sex',
    palette=palette[:2],  # Use the first two colors for females and males
    ax=axes[1]
)
axes[1].set_title(f'Top Baby Names in {selected_year}')
axes[1].set_xlabel('Name')
axes[1].set_ylabel('Count (n)')

# Adjust spacing between subplots
plt.tight_layout()

# Streamlit app description
st.text("Explore the popularity of a name over time and the top baby names for a selected year.")
