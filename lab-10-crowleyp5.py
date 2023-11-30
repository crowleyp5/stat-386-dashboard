import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
data_url = "https://raw.githubusercontent.com/esnt/Data/main/Names/popular_names.csv"
data = pd.read_csv(data_url)

st.title("Popular Names")
st.header("Top Baby Names Analysis")

selected_year = st.slider("Select a year:", min_value=1910, max_value=2021, value=1910, step=1)
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
fig, axes = plt.subplots(3, 1, figsize=(12, 16), gridspec_kw={'height_ratios': [5, 5, 5]})
palette = sns.color_palette("husl")
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
sns.barplot(
    data=top_names_selected_year[top_names_selected_year['sex'] == 'M'],
    x='name',
    y='n',
    palette=[palette[1]],  # Use the second color for males
    ax=axes[1]
)
axes[1].set_title(f'Top Baby Names for Males in {selected_year}')
axes[1].set_xlabel('Name')
axes[0].tick_params(axis='x', rotation=45)
axes[1].tick_params(axis='x', rotation=45)
selected_name = st.text_input(f"Enter a name to see popularity over time and see top names in {selected_year}:")
if selected_name:
    name_data = data[(data['name'] == selected_name) & (data['year'] >= 1910) & (data['year'] <= 2021)]
    if not name_data.empty:
        sns.lineplot(
            data=name_data,
            x='year',
            y='n',
            hue='sex',
            palette=[palette[0], palette[1]], 
            hue_order=['F', 'M'], 
            ax=axes[2]
        )
        axes[2].set_title(f'Popularity of {selected_name} Over Time')
        axes[2].set_xlabel('Year')
        axes[2].set_ylabel('Count (n)')
    else:
        st.warning(f"Name '{selected_name}' not found in the dataset.")
else:
    st.info("Enter a name to see popularity over time.")
plt.tight_layout()
st.pyplot(fig)
st.text("Explore the top baby names and their popularity over time.")
