import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load data from the new dataset URL
data_url = "https://raw.githubusercontent.com/esnt/Data/main/Names/popular_names.csv"
data = pd.read_csv(data_url)

# App title
st.title('Popular Names Analysis')

# Sidebar with user input
selected_columns = st.sidebar.multiselect('Select columns:', data.columns)

# Check if 'year', 'name', and 'n' are selected
if 'year' in selected_columns and 'name' in selected_columns and 'n' in selected_columns:
    st.write('Selected columns:', selected_columns)
    
    # Group data by year and name, summing the counts 'n'
    grouped_data = data.groupby(['year', 'name'])['n'].sum().reset_index()

    # Create a bar chart
    fig, ax = plt.subplots(figsize=(10, 6))
    for name, group in grouped_data.groupby('name'):
        ax.plot(group['year'], group['n'], label=name)

    ax.set_xlabel('Year')
    ax.set_ylabel('Count')
    ax.set_title('Name Popularity Over Time')
    ax.legend()

    # Display the chart
    st.pyplot(fig)

# Main content
st.write('Here is some data:')
st.write(data)
