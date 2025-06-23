import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Load part list
@st.cache_data
def load_parts():
    df = pd.read_csv("parts_list.csv")
    df.columns = df.columns.str.strip()  # Clean header spaces
    return df

parts_df = load_parts()

# Title
st.title("🔍 Part Number Checker")
part_input = st.text_input("Enter Part Number").strip()

# Ensure Part Number column is uppercase for match
parts_df["Part Number"] = parts_df["Part Number"].astype(str).str.upper()

# Logging function
def log_search(part_number, part_name):
    log_file = "search_log.csv"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = pd.DataFrame([[timestamp, part_number, part_name]], columns=["Timestamp", "Part Number", "Part Name"])

    try:
        if os.path.exists(log_file):
            entry.to_csv(log_file, mode='a', header=False, index=False)
        else:
            entry.to_csv(log_file, mode='w', header=True, index=False)
    except Exception as e:
        st.error(f"Error writing to log: {e}")

# Main logic
if part_input:
    input_upper = part_input.upper()
    if input_upper in parts_df["Part Number"].values:
        matched_row = parts_df[parts_df["Part Number"] == input_upper].iloc[0]
        part_name = matched_row["Part Name"]
        st.success(f"✅ {input_upper} is correct – {part_name}")
        log_search(input_upper, part_name)
    else:
        st.error("❌ Part Number Not Found")
        log_search(input_upper, "Not Found")

# Optional: Display log in app
if os.path.exists("search_log.csv"):
    with st.expander("📄 View Search Log"):
        log_df = pd.read_csv("search_log.csv")
        st.dataframe(log_df)
