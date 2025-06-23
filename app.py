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

if "Part Number" in parts_df.columns:
    # Make everything uppercase for case-insensitive matching
    parts_df["Part Number"] = parts_df["Part Number"].astype(str).str.upper()
    input_upper = part_input.upper()

    if input_upper in parts_df["Part Number"].values:
        matched_row = parts_df[parts_df["Part Number"] == input_upper].iloc[0]
        part_name = matched_row["Part Name"]
        st.success(f"✅ {input_upper} is correct – {part_name}")
    else:
        st.error("❌ Part Number Not Found")
else:
    st.error("🚨 'Part Number' column missing from parts_list.csv")
