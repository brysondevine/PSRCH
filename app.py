import streamlit as st
import pandas as pd

# Load the part list
@st.cache_data
def load_parts():
    return pd.read_csv("parts_list.csv")

parts_df = load_parts()

# UI
st.title("Part Number Checker")
part_input = st.text_input("Enter Part Number").strip()

if part_input:
    if part_input.upper() in parts_df["Part Number"].astype(str).str.upper().values:
        st.success("✅ Commodity Is Correct")
    else:
        st.error("❌ Part Number Not Found")
