import streamlit as st
import requests
import json

st.title("📂 Load & Download Workflows from GitHub")

# 👇 replace with your repo and path
owner = "user"
repo = "repo"
path = "workflows"  # folder containing JSON files
branch = "main"

# GitHub API to list files in a repo folder
api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}?ref={branch}"

response = requests.get(api_url)

if response.status_code == 200:
    files = response.json()

    json_files = [f for f in files if f["name"].endswith(".json")]

    for f in json_files:
        raw_url = f["download_url"]
        filename = f["name"]

        file_response = requests.get(raw_url)
        if file_response.status_code == 200:
            try:
                data = file_response.json()
            except Exception:
                st.error(f"❌ {filename} is not valid JSON")
                continue

            json_bytes = json.dumps(data, indent=2).encode("utf-8")

            with st.expander(filename):
                st.json(data)

                st.download_button(
                    label=f"⬇️ Download {filename}",
                    data=json_bytes,
                    file_name=filename,
                    mime="application/json",
                    key=filename
                )
        else:
            st.warning(f"⚠️ Could not fetch {filename}")
else:
    st.error("❌ Could not list files from GitHub. Check repo/path/branch.")
