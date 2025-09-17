import streamlit as st
import requests
import json

st.title("n8n Workflow Loader")

# GitHub raw base URL
base_url = "https://raw.githubusercontent.com/entremotivator/Toolkitflow/main/"

# JSON file path in repo
file_path = "mainToolkitflow/08b1gIbnNFYMbzhf.json"

# Full URL to raw file
url = base_url + file_path

# Fetch JSON from GitHub
response = requests.get(url)
if response.status_code == 200:
    workflow_data = response.json()

    # Show JSON in expander
    with st.expander("08b1gIbnNFYMbzhf.json"):
        st.json(workflow_data)

    # Download button
    st.download_button(
        label="⬇️ Download Workflow",
        data=json.dumps(workflow_data, indent=2),
        file_name="08b1gIbnNFYMbzhf.json",
        mime="application/json"
    )
else:
    st.error(f"❌ Failed to load file (HTTP {response.status_code})")

