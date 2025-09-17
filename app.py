import streamlit as st
import requests
import json
import time
from datetime import datetime
from typing import Dict, List, Any, Optional
import concurrent.futures
import threading

# Page configuration
st.set_page_config(
    page_title="Toolkitflow – n8n Workflows",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .workflow-card {
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        background: #f9f9f9;
    }
    .workflow-title {
        color: #1f77b4;
        font-weight: bold;
        font-size: 1.2em;
    }
    .workflow-stats {
        color: #666;
        font-size: 0.9em;
    }
    .success-message {
        color: #28a745;
        font-weight: bold;
    }
    .error-message {
        color: #dc3545;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=300)  # Cache for 5 minutes
def get_workflow_files() -> List[str]:
    """Automatically fetch workflow files from the repository"""
    try:
        # GitHub API to list files in the repository
        api_url = "https://api.github.com/repos/entremotivator/Toolkitflow/contents/"
        response = requests.get(api_url)
        
        if response.status_code == 200:
            files_data = response.json()
            json_files = [file['name'] for file in files_data 
                         if file['name'].endswith('.json') and file['type'] == 'file']
            return sorted(json_files)
        else:
            # Fallback to manual list if API fails
            return [
                "5DFwypiEh4EOHlzW.json", "5ffxJs8rOKZ9yt3g.json", "5lq5cFPMiPQ46wZZ.json",
                "5qpZpZXupMOvK1vV.json", "6A46EhObByy7KRqf.json", "6ENOYGPUsVxXhurz.json",
                "6bB0EmALHIWPaXAE.json", "6kR3VErnDkdbTuaN.json", "6m9j0LxGaQk3P5EB.json",
                "6n0o2It39BYn7YxT.json", "7uIvNpxljlOTaZEA.json", "8PFBHVbfII2ck4wE.json",
                "8QDOfCtR8OVTNX4c.json", "8XF5jkMyhP4gtGbw.json", "8gHsz2f9UQR7T1jL.json"
            ]
    except Exception:
        # Return fallback list if anything goes wrong
        return [
            "5DFwypiEh4EOHlzW.json", "5ffxJs8rOKZ9yt3g.json", "5lq5cFPMiPQ46wZZ.json",
            "5qpZpZXupMOvK1vV.json", "6A46EhObByy7KRqf.json", "6ENOYGPUsVxXhurz.json",
            "6bB0EmALHIWPaXAE.json", "6kR3VErnDkdbTuaN.json", "6m9j0LxGaQk3P5EB.json",
            "6n0o2It39BYn7YxT.json", "7uIvNpxljlOTaZEA.json", "8PFBHVbfII2ck4wE.json",
            "8QDOfCtR8OVTNX4c.json", "8XF5jkMyhP4gtGbw.json", "8gHsz2f9UQR7T1jL.json"
        ]

@st.cache_data(ttl=600)  # Cache for 10 minutes
def fetch_workflow(file: str, base_url: str) -> Optional[Dict[str, Any]]:
    """Fetch a single workflow file with error handling"""
    try:
        url = base_url + file
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception:
        return None

def analyze_workflow(workflow_data: Dict[str, Any]) -> Dict[str, Any]:
    """Extract useful information from workflow data"""
    analysis = {
        'name': workflow_data.get('name', 'Unnamed Workflow'),
        'node_count': len(workflow_data.get('nodes', [])),
        'connection_count': len(workflow_data.get('connections', {})),
        'has_trigger': False,
        'node_types': set(),
        'created_at': workflow_data.get('createdAt'),
        'updated_at': workflow_data.get('updatedAt'),
        'tags': workflow_data.get('tags', [])
    }
    
    # Analyze nodes
    for node in workflow_data.get('nodes', []):
        node_type = node.get('type', '')
        analysis['node_types'].add(node_type)
        if 'trigger' in node_type.lower() or node.get('position') == [0, 0]:
            analysis['has_trigger'] = True
    
    analysis['node_types'] = list(analysis['node_types'])
    return analysis

def main():
    st.title("🔧 Toolkitflow – n8n Workflows")
    st.markdown("*Enhanced workflow viewer with search, filtering, and batch operations*")
    
    # Sidebar configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # GitHub settings
        st.subheader("Repository Settings")
        base_url = st.text_input(
            "Base URL",
            value="https://raw.githubusercontent.com/entremotivator/Toolkitflow/main/",
            help="GitHub raw content base URL"
        )
        
        # Auto-refresh option
        auto_refresh = st.checkbox("Auto-refresh file list", value=True)
        if auto_refresh:
            refresh_interval = st.slider("Refresh interval (seconds)", 30, 300, 60)
        
        # Display options
        st.subheader("Display Options")
        show_analysis = st.checkbox("Show workflow analysis", value=True)
        items_per_page = st.slider("Items per page", 5, 50, 10)
        
        # Filters
        st.subheader("Filters")
        search_term = st.text_input("🔍 Search workflows", placeholder="Enter search term...")
        min_nodes = st.slider("Minimum nodes", 0, 50, 0)
        
    # Main content area
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("🔄 Refresh File List", type="primary"):
            st.cache_data.clear()
            st.rerun()
    
    with col2:
        load_all = st.button("📥 Load All Workflows")
    
    with col3:
        if st.button("📊 Generate Report"):
            st.session_state.generate_report = True
    
    # Get workflow files
    with st.spinner("Fetching workflow files..."):
        files = get_workflow_files()
    
    st.success(f"Found {len(files)} workflow files")
    
    # Initialize session state
    if 'workflows_data' not in st.session_state:
        st.session_state.workflows_data = {}
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 0
    
    # Load all workflows if requested
    if load_all:
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            future_to_file = {
                executor.submit(fetch_workflow, file, base_url): file 
                for file in files
            }
            
            completed = 0
            for future in concurrent.futures.as_completed(future_to_file):
                file = future_to_file[future]
                try:
                    data = future.result()
                    if data:
                        st.session_state.workflows_data[file] = data
                except Exception as e:
                    st.error(f"Error loading {file}: {str(e)}")
                
                completed += 1
                progress_bar.progress(completed / len(files))
                status_text.text(f"Loaded {completed}/{len(files)} workflows")
        
        progress_bar.empty()
        status_text.empty()
        st.success("All workflows loaded!")
    
    # Filter and search workflows
    filtered_files = files
    if search_term:
        filtered_files = [
            file for file in files 
            if search_term.lower() in file.lower() or 
            (file in st.session_state.workflows_data and 
             search_term.lower() in st.session_state.workflows_data[file].get('name', '').lower())
        ]
    
    # Pagination
    total_pages = (len(filtered_files) - 1) // items_per_page + 1
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("⬅️ Previous") and st.session_state.current_page > 0:
            st.session_state.current_page -= 1
    with col2:
        st.write(f"Page {st.session_state.current_page + 1} of {total_pages}")
    with col3:
        if st.button("➡️ Next") and st.session_state.current_page < total_pages - 1:
            st.session_state.current_page += 1
    
    # Display workflows
    start_idx = st.session_state.current_page * items_per_page
    end_idx = min(start_idx + items_per_page, len(filtered_files))
    current_files = filtered_files[start_idx:end_idx]
    
    for file in current_files:
        with st.container():
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"### 📋 {file}")
            
            with col2:
                # Individual load button
                if st.button(f"Load", key=f"load_{file}"):
                    with st.spinner(f"Loading {file}..."):
                        data = fetch_workflow(file, base_url)
                        if data:
                            st.session_state.workflows_data[file] = data
                            st.success(f"✅ Loaded {file}")
                        else:
                            st.error(f"❌ Failed to load {file}")
            
            # Display workflow if loaded
            if file in st.session_state.workflows_data:
                workflow_data = st.session_state.workflows_data[file]
                
                if show_analysis:
                    analysis = analyze_workflow(workflow_data)
                    
                    # Filter by minimum nodes
                    if analysis['node_count'] < min_nodes:
                        continue
                    
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Nodes", analysis['node_count'])
                    with col2:
                        st.metric("Connections", analysis['connection_count'])
                    with col3:
                        st.metric("Has Trigger", "Yes" if analysis['has_trigger'] else "No")
                    with col4:
                        st.metric("Node Types", len(analysis['node_types']))
                    
                    if analysis['name'] != 'Unnamed Workflow':
                        st.write(f"**Name:** {analysis['name']}")
                    
                    if analysis['node_types']:
                        st.write(f"**Node Types:** {', '.join(analysis['node_types'][:5])}{'...' if len(analysis['node_types']) > 5 else ''}")
                    
                    if analysis['tags']:
                        st.write(f"**Tags:** {', '.join(analysis['tags'])}")
                
                # Action buttons
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.download_button(
                        label=f"⬇️ Download JSON",
                        data=json.dumps(workflow_data, indent=2),
                        file_name=file,
                        mime="application/json",
                        key=f"download_{file}"
                    )
                
                with col2:
                    # Copy to clipboard button (using streamlit's native functionality)
                    if st.button(f"📋 Copy URL", key=f"copy_{file}"):
                        st.code(base_url + file, language=None)
                        st.info("URL displayed above - copy manually")
                
                with col3:
                    if st.button(f"🗑️ Remove", key=f"remove_{file}"):
                        del st.session_state.workflows_data[file]
                        st.rerun()
                

            
            st.divider()
    
    # Generate report if requested
    if st.session_state.get('generate_report', False):
        st.session_state.generate_report = False
        
        if st.session_state.workflows_data:
            st.header("📊 Workflow Analysis Report")
            
            # Summary statistics
            total_workflows = len(st.session_state.workflows_data)
            total_nodes = sum(len(data.get('nodes', [])) for data in st.session_state.workflows_data.values())
            avg_nodes = total_nodes / total_workflows if total_workflows > 0 else 0
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Workflows", total_workflows)
            with col2:
                st.metric("Total Nodes", total_nodes)
            with col3:
                st.metric("Average Nodes per Workflow", f"{avg_nodes:.1f}")
            
            # Node type analysis
            all_node_types = {}
            for data in st.session_state.workflows_data.values():
                for node in data.get('nodes', []):
                    node_type = node.get('type', 'unknown')
                    all_node_types[node_type] = all_node_types.get(node_type, 0) + 1
            
            if all_node_types:
                st.subheader("Most Common Node Types")
                sorted_types = sorted(all_node_types.items(), key=lambda x: x[1], reverse=True)[:10]
                for node_type, count in sorted_types:
                    st.write(f"• **{node_type}**: {count} instances")
        else:
            st.info("No workflows loaded. Load some workflows first to generate a report.")

    # Auto-refresh functionality
    if auto_refresh and 'last_refresh' in st.session_state:
        time_since_refresh = time.time() - st.session_state.last_refresh
        if time_since_refresh > refresh_interval:
            st.cache_data.clear()
            st.session_state.last_refresh = time.time()
            st.rerun()
    elif auto_refresh:
        st.session_state.last_refresh = time.time()

if __name__ == "__main__":
    main()
