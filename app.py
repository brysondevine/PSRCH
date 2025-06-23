import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Load parts list
@st.cache_data
def load_parts():
    df = pd.read_csv("parts_list.csv")
    df.columns = df.columns.str.strip()  # Clean up any spaces in headers
    return df

parts_df = load_parts()

# Title and input
st.title("🔍 Part Number Checker")
part_input = st.text_input("Enter Part Number").strip()

# Log search
def log_search(part_number):
    log_file = "search_log.csv"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_entry = pd.DataFrame([[timestamp, part_number]], columns=["Timestamp", "Part Number"])

    if os.path.exists(log_file):
        new_entry.to_csv(log_file, mode="a", header=False, index=False)
    else:
        new_entry.to_csv(log_file, mode="w", header=True, index=False)

# Main logic
if part_input:
    log_search(part_input)  # Save the input to log
    input_upper = part_input.upper()
    parts_df["Part Number"] = parts_df["Part Number"].astype(str).str.upper()

    if input_upper in parts_df["Part Number"].values:
        matched_row = parts_df[parts_df["Part Number"] == input_upper].iloc[0]
        part_name = matched_row["Part Name"]
        st.success(f"✅ {input_upper} is correct – {part_name}")
    else:
        st.error("❌ Part Number Not Found")
