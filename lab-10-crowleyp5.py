import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data from the dataset URL
data_url = "https://raw.githubusercontent.com/esnt/Data/main/Names/popular_names.csv"
data = pd.read_csv(data_url)

# Streamlit app title and description
st.title("Baby Names Analysis")
st.header("Top Baby Names Analysis")

# Filter data by year
selected_year = st.slider("Select a year:", min_value=1910, max_value=2021, value=1910, step=1)

# User input for the name
selected_name = st.text_input(f"Enter a name to see popularity over time in {selected_year}:")

# Create a copy of the data
data_copy = data.copy()

# Calculate the popularity of the selected name over time
if selected_name:
    name_data = data_copy[(data_copy['name'] == selected_name)]
    if not name_data.empty:
        # Create a plot for popularity over time
        fig, axes = plt.subplots(1, 1, figsize=(18, 9))
        sns.lineplot(
            data=name_data,
            x='year',
            y='n',
            hue='sex',
            palette=sns.color_palette("husl")[:2],  # Use the first two colors for females and males
            ax=axes
        )
        axes.set_title(f'Popularity of {selected_name} Over Time')
        axes.set_xlabel('Year')
        axes.set_ylabel('Count (n)')
        # Set fixed x-axis limits
        axes.set_xlim(1910, 2021)
        st.pyplot(fig)
    else:
        st.warning(f"Name '{selected_name}' not found in the dataset.")
else:
    st.info("Enter a name to see popularity over time.")

# Calculate the top 10 baby names by 'n' for both genders for the selected year
data_selected_year = data_copy[data_copy['year'] == selected_year]
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
fig, axes = plt.subplots(1, 1, figsize=(18, 9))
sns.barplot(
    data=top_names_selected_year,
    x='name',
    y='n',
    hue='sex',
    palette=sns.color_palette("husl")[:2],  # Use the first two colors for females and males
    ax=axes
)
axes.set_title(f'Top Baby Names in {selected_year}')
axes.set_xlabel('Name')
axes.set_ylabel('Count (n)')
# Adjust spacing between subplots
plt.tight_layout()
st.pyplot(fig)

# Streamlit app description
st.text("Explore the popularity of a name over time and the top baby names for a selected year.")
