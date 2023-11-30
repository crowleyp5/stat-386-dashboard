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
selected_year = st.slider("Select a year:", min_value=1880, max_value=2020, value=1910, step=1)
data_selected_year = data[data['year'] == selected_year]

# Calculate the top 10 baby names by 'n' for both genders
top_names_selected_year = (
    data_selected_year.groupby(['name', 'sex'])['n']
    .sum()
    .reset_index()
    .sort_values(by='n', ascending=False)
    .groupby('sex')
    .head(10)
    .sort_values(by='n', ascending=False)
)

# Create subplots for males, females, and popularity over time
fig, axes = plt.subplots(1, 3, figsize=(18, 6), gridspec_kw={'width_ratios': [1, 1, 2]})  # 3 subplots side by side

# Define color palette
palette = sns.color_palette("husl")

# Create bar chart for top baby names for females
sns.barplot(
    data=top_names_selected_year[top_names_selected_year['sex'] == 'F'],
    x='name',
    y='n',
    palette=[palette[0]],  # Use the first color for females
    ax=axes[0]
)
axes[0].set_title(f'Top Baby Names for Females in {selected_year}')
axes[0].set_xlabel('Name')
axes[0].set_ylabel('Count (n)')

# Create bar chart for top baby names for males
sns.barplot(
    data=top_names_selected_year[top_names_selected_year['sex'] == 'M'],
    x='name',
    y='n',
    palette=[palette[1]],  # Use the second color for males
    ax=axes[1]
)
axes[1].set_title(f'Top Baby Names for Males in {selected_year}')
axes[1].set_xlabel('Name')

# Rotate x-axis labels for better readability
axes[0].tick_params(axis='x', rotation=45)
axes[1].tick_params(axis='x', rotation=45)

# User input for the name
selected_name = st.text_input(f"Enter a name to see popularity over time in {selected_year}:")

# Filter data for the selected name and plot popularity over time
if selected_name:
    name_data = data[(data['name'] == selected_name) & (data['year'] >= selected_year - 10) & (data['year'] <= selected_year + 10)]
    if not name_data.empty:
        sns.lineplot(
            data=name_data,
            x='year',
            y='n',
            hue='sex',
            palette=palette[:2],  # Use the first two colors for females and males
            ax=axes[2]
        )
        axes[2].set_title(f'Popularity of {selected_name} Over Time')
        axes[2].set_xlabel('Year')
        axes[2].set_ylabel('Count (n)')
    else:
        st.warning(f"Name '{selected_name}' not found in the dataset.")
else:
    st.info("Enter a name to see popularity over time.")

# Adjust spacing between subplots
plt.tight_layout()

# Display the Seaborn subplots within Streamlit
st.pyplot(fig)

# Streamlit app description
st.text("Explore the top baby names and their popularity over time.")
