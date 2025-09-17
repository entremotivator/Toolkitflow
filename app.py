import streamlit as st
import json
import requests

st.title("📂 Load & Download Workflows from GitHub")

# 👇 Replace with your actual repo path
base_url = "https://raw.githubusercontent.com/user/repo/main/workflows/"

files = [f"workflow{i}.json" for i in range(1, 6)]

for file in files:
    url = base_url + file
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        json_bytes = json.dumps(data, indent=2).encode("utf-8")

        with st.expander(file):
            st.json(data)

            # ✅ Download button
            st.download_button(
                label=f"⬇️ Download {file}",
                data=json_bytes,
                file_name=file,
                mime="application/json",
                key=file
            )
    else:
        st.error(f"❌ Could not load {file}")
