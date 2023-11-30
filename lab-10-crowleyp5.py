import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load data
data = pd.read_csv('loldata_cleaned.csv')

# App title
st.title('League of Legends: Red Side vs Blue Side Comparison')

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