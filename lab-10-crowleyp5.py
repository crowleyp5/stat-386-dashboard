import streamlit as st
import pandas as pd

# Load data from the new dataset URL
data_url = "https://raw.githubusercontent.com/esnt/Data/main/Names/popular_names.csv"
data = pd.read_csv(data_url)

# App title
st.title('Popular Names Analysis')

# Sidebar with user input
selected_columns = st.sidebar.multiselect('Select columns for the bar chart:', data.columns)

# Create a bar chart based on user selection
if selected_columns:
    st.write('Selected columns:', selected_columns)
    selected_data = data[selected_columns]
    st.bar_chart(selected_data)

# Main content
st.write('Here is some data:')
st.write(data)
