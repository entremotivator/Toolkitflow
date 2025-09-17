import streamlit as st
import requests
import json

st.title("Toolkitflow – n8n Workflows")

# GitHub raw base URL
base_url = "https://raw.githubusercontent.com/entremotivator/Toolkitflow/main/"

# List of workflow files
files = [
    "5DFwypiEh4EOHlzW.json",
    "5ffxJs8rOKZ9yt3g.json",
    "5lq5cFPMiPQ46wZZ.json",
    "5qpZpZXupMOvK1vV.json",
    "6A46EhObByy7KRqf.json",
    "6ENOYGPUsVxXhurz.json",
    "6bB0EmALHIWPaXAE.json",
    "6kR3VErnDkdbTuaN.json",
    "6m9j0LxGaQk3P5EB.json",
    "6n0o2It39BYn7YxT.json",
    "7uIvNpxljlOTaZEA.json",
    "8PFBHVbfII2ck4wE.json",
    "8QDOfCtR8OVTNX4c.json",
    "8XF5jkMyhP4gtGbw.json",
    "8gHsz2f9UQR7T1jL.json"
]

# Loop through files
for file in files:
    url = base_url + file
    response = requests.get(url)

    if response.status_code == 200:
        workflow_data = response.json()

        # Show JSON in expander
        with st.expander(file):
            st.json(workflow_data)

        # Download button
        st.download_button(
            label=f"⬇️ Download {file}",
            data=json.dumps(workflow_data, indent=2),
            file_name=file,
            mime="application/json"
        )
    else:
        st.error(f"❌ Failed to load {file} (HTTP {response.status_code})")
