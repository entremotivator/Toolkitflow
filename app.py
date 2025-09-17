# streamlit_ollama_course.py
import streamlit as st
import time
from datetime import datetime
import json

# Page configuration
st.set_page_config(
    page_title="Streamlit + Ollama Course",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    .lesson-card {
        background: white;
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        border-left: 5px solid #667eea;
    }
    
    .code-block {
        background: #2d3748;
        color: #e2e8f0;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        font-family: 'Courier New', monospace;
        border-left: 5px solid #667eea;
    }
    
    .highlight-box {
        background: linear-gradient(135deg, #ffeaa7 0%, #fab1a0 100%);
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 5px solid #fdcb6e;
    }
    
    .warning-box {
        background: #fcf8e3;
        border: 1px solid #faebcc;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 5px solid #f0ad4e;
    }
    
    .success-box {
        background: #dff0d8;
        border: 1px solid #d6e9c6;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 5px solid #5cb85c;
    }
    
    .project-card {
        background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(116, 185, 255, 0.3);
    }
    
    .step-counter {
        background: #667eea;
        color: white;
        width: 30px;
        height: 30px;
        border-radius: 50%;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        margin-right: 10px;
    }
    
    .video-container {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "current_lesson" not in st.session_state:
    st.session_state.current_lesson = 0
if "lesson_progress" not in st.session_state:
    st.session_state.lesson_progress = {}
if "show_code_examples" not in st.session_state:
    st.session_state.show_code_examples = True

# Course data structure
LESSONS = [
    {"id": "intro", "title": "🎯 Introduction", "icon": "🎯"},
    {"id": "setup", "title": "⚙️ Setup & Installation", "icon": "⚙️"},
    {"id": "streamlit_basics", "title": "🎨 Streamlit Basics", "icon": "🎨"},
    {"id": "ollama_setup", "title": "🤖 Ollama Setup", "icon": "🤖"},
    {"id": "integration", "title": "🔗 Integration", "icon": "🔗"},
    {"id": "chatbot", "title": "💬 ChatGPT Clone", "icon": "💬"},
    {"id": "advanced", "title": "🚀 Advanced Features", "icon": "🚀"},
    {"id": "deployment", "title": "🌐 Deployment", "icon": "🌐"}
]

def mark_lesson_complete(lesson_id):
    """Mark a lesson as completed"""
    st.session_state.lesson_progress[lesson_id] = True
    
def is_lesson_complete(lesson_id):
    """Check if lesson is completed"""
    return st.session_state.lesson_progress.get(lesson_id, False)

def get_progress_percentage():
    """Calculate overall progress"""
    completed = sum(1 for lesson in LESSONS if is_lesson_complete(lesson["id"]))
    return int((completed / len(LESSONS)) * 100)

def display_code_block(code, language="python", title=""):
    """Display code block with copy functionality"""
    if title:
        st.subheader(title)
    
    st.markdown(f'<div class="code-block">', unsafe_allow_html=True)
    st.code(code, language=language)
    st.markdown('</div>', unsafe_allow_html=True)

def display_video(embed_code, title=""):
    """Display embedded video"""
    if title:
        st.subheader(title)
    
    st.markdown('<div class="video-container">', unsafe_allow_html=True)
    st.components.v1.html(embed_code, height=400)
    st.markdown('</div>', unsafe_allow_html=True)

# Sidebar Navigation
with st.sidebar:
    st.title("📚 Course Navigation")
    
    # Progress indicator
    progress = get_progress_percentage()
    st.metric("Course Progress", f"{progress}%")
    st.progress(progress / 100)
    
    st.markdown("---")
    
    # Lesson navigation
    for i, lesson in enumerate(LESSONS):
        completed_icon = "✅" if is_lesson_complete(lesson["id"]) else "⭕"
        current_icon = "👉" if i == st.session_state.current_lesson else ""
        
        if st.button(
            f"{completed_icon} {current_icon} {lesson['title']}", 
            key=f"nav_{lesson['id']}",
            use_container_width=True,
            type="primary" if i == st.session_state.current_lesson else "secondary"
        ):
            st.session_state.current_lesson = i
            st.rerun()
    
    st.markdown("---")
    
    # Settings
    st.subheader("⚙️ Settings")
    st.session_state.show_code_examples = st.checkbox(
        "Show Code Examples", 
        value=st.session_state.show_code_examples
    )
    
    # Export/Import Progress
    st.subheader("📊 Progress Management")
    
    # Export progress
    if st.button("📤 Export Progress"):
        progress_data = {
            "progress": st.session_state.lesson_progress,
            "current_lesson": st.session_state.current_lesson,
            "exported_at": datetime.now().isoformat()
        }
        st.download_button(
            "Download Progress",
            data=json.dumps(progress_data, indent=2),
            file_name=f"course_progress_{datetime.now().strftime('%Y%m%d')}.json",
            mime="application/json"
        )
    
    # Import progress
    uploaded_progress = st.file_uploader("📥 Import Progress", type=['json'])
    if uploaded_progress:
        try:
            progress_data = json.loads(uploaded_progress.read().decode('utf-8'))
            st.session_state.lesson_progress = progress_data.get("progress", {})
            st.session_state.current_lesson = progress_data.get("current_lesson", 0)
            st.success("Progress imported successfully!")
            time.sleep(1)
            st.rerun()
        except Exception as e:
            st.error(f"Error importing progress: {str(e)}")

# Main content area
current_lesson = LESSONS[st.session_state.current_lesson]

# Header
st.markdown("""
<div class="main-header">
    <h1>🚀 Streamlit + Ollama Course</h1>
    <h3>Master AI-Powered Web Applications with Python</h3>
    <p>Build ChatGPT-like applications with local AI models</p>
</div>
""", unsafe_allow_html=True)

# Lesson content based on current selection
lesson_id = current_lesson["id"]

if lesson_id == "intro":
    st.markdown('<div class="lesson-card">', unsafe_allow_html=True)
    st.title("🎯 Course Introduction")
    
    # Embedded video
    video_embed = '''
    <div style="padding: 56.25% 0 0 0; position: relative">
        <div style="height:100%;left:0;position:absolute;top:0;width:100%">
            <iframe height="100%" width="100%" src="https://embed.wave.video/9krwfjf82Rh2ihLP" frameborder="0" allow="autoplay; fullscreen" scrolling="no"></iframe>
        </div>
    </div>
    '''
    display_video(video_embed, "📹 Welcome to the Course")
    
    st.markdown('<div class="highlight-box">', unsafe_allow_html=True)
    st.markdown("### 🎓 What You'll Learn")
    st.markdown("""
    - Build interactive web applications with Streamlit
    - Integrate local AI models using Ollama  
    - Create a fully functional ChatGPT clone
    - Deploy your applications to production
    - Advanced AI integration techniques
    - Performance optimization and best practices
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="success-box">', unsafe_allow_html=True)
        st.markdown("### 📋 Prerequisites")
        st.markdown("""
        - Basic Python knowledge
        - Understanding of web concepts
        - Python 3.8+ installed
        - 8GB+ RAM recommended for Ollama
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="warning-box">', unsafe_allow_html=True)
        st.markdown("### 🛠️ Required Tools")
        st.markdown("""
        - Python 3.8+
        - Code editor (VS Code recommended)
        - Terminal/Command prompt
        - Web browser
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="project-card">', unsafe_allow_html=True)
    st.markdown("### 🎯 Course Objectives")
    st.markdown("""
    By the end of this course, you'll have built a complete AI-powered web application that can:
    - Run entirely on your local machine
    - Chat with various AI models through an intuitive web interface
    - Handle file uploads and voice input
    - Export/import conversation history
    - Compare responses from multiple models
    - Be deployed to production environments
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("✅ Mark Lesson Complete", key="complete_intro"):
        mark_lesson_complete("intro")
        st.success("Lesson completed! 🎉")
        time.sleep(1)
        st.rerun()

elif lesson_id == "setup":
    st.markdown('<div class="lesson-card">', unsafe_allow_html=True)
    st.title("⚙️ Setup & Installation")
    
    st.markdown("### Step-by-Step Environment Setup")
    
    # Step 1
    st.markdown('<span class="step-counter">1</span>**Create Virtual Environment**', unsafe_allow_html=True)
    
    if st.session_state.show_code_examples:
        display_code_block("""# Create virtual environment
python -m venv streamlit_ollama_env

# Activate virtual environment
# Windows:
streamlit_ollama_env\\Scripts\\activate

# macOS/Linux:
source streamlit_ollama_env/bin/activate""", "bash")
    
    # Step 2
    st.markdown('<span class="step-counter">2</span>**Install Required Packages**', unsafe_allow_html=True)
    
    if st.session_state.show_code_examples:
        display_code_block("""# Install core packages
pip install streamlit>=1.28.0
pip install ollama>=0.1.7
pip install requests>=2.31.0
pip install python-dotenv>=1.0.0

# Optional packages for advanced features
pip install SpeechRecognition>=3.10.0
pip install pyaudio>=0.2.11
pip install pandas>=2.0.0""")
    
    # Step 3
    st.markdown('<span class="step-counter">3</span>**Create Requirements File**', unsafe_allow_html=True)
    
    if st.session_state.show_code_examples:
        display_code_block("""# requirements.txt
streamlit>=1.28.0
ollama>=0.1.7
requests>=2.31.0
python-dotenv>=1.0.0
SpeechRecognition>=3.10.0
pyaudio>=0.2.11
pandas>=2.0.0""", "text")
    
    # Step 4
    st.markdown('<span class="step-counter">4</span>**Verify Installation**', unsafe_allow_html=True)
    
    if st.session_state.show_code_examples:
        display_code_block("""# Test Streamlit installation
streamlit hello

# This should open your browser with Streamlit's demo app""", "bash")
    
    st.markdown('<div class="warning-box">', unsafe_allow_html=True)
    st.markdown("**💡 Pro Tip:** Always use virtual environments to avoid package conflicts and maintain clean project dependencies.")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Interactive verification
    st.markdown("### 🧪 Interactive Verification")
    
    if st.button("Test Streamlit Import"):
        try:
            import streamlit as st_test
            st.success(f"✅ Streamlit {st_test.__version__} imported successfully!")
        except ImportError:
            st.error("❌ Streamlit not found. Please install it first.")
    
    if st.button("Test Other Packages"):
        packages = ['requests', 'json', 'datetime']
        results = []
        
        for package in packages:
            try:
                __import__(package)
                results.append(f"✅ {package}")
            except ImportError:
                results.append(f"❌ {package}")
        
        for result in results:
            if "✅" in result:
                st.success(result)
            else:
                st.error(result)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("✅ Mark Lesson Complete", key="complete_setup"):
        mark_lesson_complete("setup")
        st.success("Setup completed! 🎉")
        time.sleep(1)
        st.rerun()

elif lesson_id == "streamlit_basics":
    st.markdown('<div class="lesson-card">', unsafe_allow_html=True)
    st.title("🎨 Streamlit Fundamentals")
    
    st.markdown("### Your First Streamlit App")
    
    if st.session_state.show_code_examples:
        display_code_block("""# app.py
import streamlit as st
import pandas as pd
import numpy as np

# Page configuration
st.set_page_config(
    page_title="My First Streamlit App",
    page_icon="🚀",
    layout="wide"
)

# Title and header
st.title("🚀 Welcome to Streamlit!")
st.header("Building Interactive Web Apps with Python")

# Sidebar
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Choose a page", ["Home", "About", "Contact"])

# Interactive widgets
name = st.text_input("Enter your name:")
age = st.slider("Select your age:", 0, 100, 25)
favorite_color = st.selectbox("Favorite color:", ["Red", "Blue", "Green", "Yellow"])

if st.button("Submit"):
    st.success(f"Hello {name}! You are {age} years old and like {favorite_color}.")

# Display data
if st.checkbox("Show sample data"):
    data = pd.DataFrame(
        np.random.randn(10, 3),
        columns=['A', 'B', 'C']
    )
    st.dataframe(data)
    st.line_chart(data)""")
    
    st.markdown("### 🎮 Interactive Demo")
    
    # Live demo section
    st.markdown("**Try the widgets below:**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        demo_name = st.text_input("Enter your name:", key="demo_name")
        demo_age = st.slider("Select your age:", 0, 100, 25, key="demo_age")
        demo_color = st.selectbox("Favorite color:", ["Red", "Blue", "Green", "Yellow"], key="demo_color")
    
    with col2:
        if st.button("Submit Demo", key="demo_submit"):
            st.success(f"Hello {demo_name}! You are {demo_age} years old and like {demo_color}.")
        
        if st.checkbox("Show sample data", key="demo_data"):
            data = pd.DataFrame(
                np.random.randn(5, 3),
                columns=['A', 'B', 'C']
            )
            st.dataframe(data)
    
    st.markdown('<div class="highlight-box">', unsafe_allow_html=True)
    st.markdown("### 🔑 Key Streamlit Concepts")
    st.markdown("""
    - **Widgets:** Interactive elements (buttons, sliders, inputs)
    - **Layout:** Columns, sidebars, containers  
    - **State Management:** Session state for persistence
    - **Caching:** @st.cache for performance
    - **Components:** Custom HTML/JavaScript components
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Advanced examples
    st.markdown("### 🔧 Advanced Widget Examples")
    
    tab1, tab2, tab3 = st.tabs(["Basic Widgets", "Layout", "State Management"])
    
    with tab1:
        if st.session_state.show_code_examples:
            display_code_block("""# Basic widgets
text = st.text_input("Text input")
number = st.number_input("Number input", min_value=0, max_value=100)
date = st.date_input("Date picker")
time = st.time_input("Time picker")
file = st.file_uploader("File upload")
camera = st.camera_input("Camera input")""")
    
    with tab2:
        if st.session_state.show_code_examples:
            display_code_block("""# Layout examples
col1, col2, col3 = st.columns(3)
with col1:
    st.write("Column 1")
with col2:
    st.write("Column 2")
with col3:
    st.write("Column 3")

# Containers
with st.container():
    st.write("This is in a container")

# Expandable sections
with st.expander("Click to expand"):
    st.write("Hidden content here")""")
    
    with tab3:
        if st.session_state.show_code_examples:
            display_code_block("""# Session state management
if "counter" not in st.session_state:
    st.session_state.counter = 0

if st.button("Increment"):
    st.session_state.counter += 1

st.write(f"Counter: {st.session_state.counter}")

# Persistent data
if "user_data" not in st.session_state:
    st.session_state.user_data = {}""")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("✅ Mark Lesson Complete", key="complete_streamlit_basics"):
        mark_lesson_complete("streamlit_basics")
        st.success("Streamlit basics mastered! 🎉")
        time.sleep(1)
        st.rerun()

elif lesson_id == "ollama_setup":
    st.markdown('<div class="lesson-card">', unsafe_allow_html=True)
    st.title("🤖 Ollama Setup & Configuration")
    
    # Embedded video
    video_embed = '''
    <div style="padding: 56.25% 0 0 0; position: relative">
        <div style="height:100%;left:0;position:absolute;top:0;width:100%">
            <iframe height="100%" width="100%" src="https://embed.wave.video/6wo392lMuElNrw3V" frameborder="0" allow="autoplay; fullscreen" scrolling="no"></iframe>
        </div>
    </div>
    '''
    display_video(video_embed, "📹 Ollama Installation Guide")
    
    st.markdown("### Installing Ollama")
    
    # Installation steps
    st.markdown('<span class="step-counter">1</span>**Download and Install Ollama**', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["macOS", "Linux", "Windows"])
    
    with tab1:
        if st.session_state.show_code_examples:
            display_code_block("""# macOS installation
curl -fsSL https://ollama.com/install.sh | sh

# Or download from https://ollama.com/download/mac""", "bash")
    
    with tab2:
        if st.session_state.show_code_examples:
            display_code_block("""# Linux installation
curl -fsSL https://ollama.com/install.sh | sh

# Or manually:
# Download from https://ollama.com/download/linux""", "bash")
    
    with tab3:
        st.markdown("**Windows Installation:**")
        st.markdown("1. Download the installer from https://ollama.com/download/windows")
        st.markdown("2. Run the downloaded .exe file")
        st.markdown("3. Follow the installation wizard")
    
    # Step 2
    st.markdown('<span class="step-counter">2</span>**Pull Your First Model**', unsafe_allow_html=True)
    
    if st.session_state.show_code_examples:
        display_code_block("""# Pull a model (downloads locally)
ollama pull llama3.2

# Test the model
ollama run llama3.2

# Exit with /bye or Ctrl+D""", "bash")
    
    st.markdown('<div class="warning-box">', unsafe_allow_html=True)
    st.markdown("**⚠️ System Requirements:** Ollama requires significant RAM. For Llama 3.2 (7B), you need at least 8GB RAM. Larger models require more memory.")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Step 3
    st.markdown('<span class="step-counter">3</span>**Explore Available Models**', unsafe_allow_html=True)
    
    model_info = {
        "llama3.2": {"size": "7B", "ram": "8GB", "description": "Fast, efficient general purpose"},
        "mistral": {"size": "7B", "ram": "8GB", "description": "Good performance, multilingual"},
        "codellama": {"size": "7B", "ram": "8GB", "description": "Optimized for code generation"},
        "phi3": {"size": "3.8B", "ram": "4GB", "description": "Lightweight, Microsoft model"},
        "llama3.2:1b": {"size": "1B", "ram": "2GB", "description": "Ultra lightweight version"}
    }
    
    st.markdown("**Popular Models:**")
    
    for model, info in model_info.items():
        col1, col2, col3, col4 = st.columns([2, 1, 1, 3])
        with col1:
            st.markdown(f"**{model}**")
        with col2:
            st.markdown(f"{info['size']}")
        with col3:
            st.markdown(f"{info['ram']}")
        with col4:
            st.markdown(info['description'])
    
    if st.session_state.show_code_examples:
        display_code_block("""# Common Ollama commands
ollama list              # List installed models
ollama pull model_name   # Download a model
ollama rm model_name     # Remove a model
ollama serve            # Start Ollama server
ollama ps               # Show running models""", "bash")
    
    # Step 4
    st.markdown('<span class="step-counter">4</span>**Python Integration Setup**', unsafe_allow_html=True)
    
    if st.session_state.show_code_examples:
        display_code_block("""# Install Python client
pip install ollama

# Test the connection
python -c "import ollama; print(ollama.list())" """, "bash")
        
        display_code_block("""# test_ollama.py
import ollama

try:
    # Simple completion
    response = ollama.chat(
        model='llama3.2',
        messages=[{
            'role': 'user',
            'content': 'Hello, how are you?',
        }]
    )
    
    print("Response:", response['message']['content'])
    print("✅ Ollama is working correctly!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("Make sure Ollama is running and llama3.2 is installed")""")
    
    # Interactive test section
    st.markdown("### 🧪 Test Your Ollama Setup")
    
    if st.button("Test Ollama Connection"):
        try:
            import ollama
            models = ollama.list()
            st.success("✅ Ollama connected successfully!")
            st.json(models)
        except Exception as e:
            st.error(f"❌ Connection failed: {str(e)}")
            st.info("Make sure Ollama is installed and running")
    
    if st.button("Test Model Chat"):
        try:
            import ollama
            with st.spinner("Testing model..."):
                response = ollama.chat(
                    model='llama3.2',
                    messages=[{'role': 'user', 'content': 'Say hello!'}]
                )
                st.success("✅ Model test successful!")
                st.write("Response:", response['message']['content'])
        except Exception as e:
            st.error(f"❌ Model test failed: {str(e)}")
            st.info("Make sure you have pulled the llama3.2 model: `ollama pull llama3.2`")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("✅ Mark Lesson Complete", key="complete_ollama_setup"):
        mark_lesson_complete("ollama_setup")
        st.success("Ollama setup completed! 🎉")
        time.sleep(1)
        st.rerun()

elif lesson_id == "integration":
    st.markdown('<div class="lesson-card">', unsafe_allow_html=True)
    st.title("🔗 Streamlit + Ollama Integration")
    
    st.markdown("### Basic Integration")
    
    if st.session_state.show_code_examples:
        display_code_block("""# basic_integration.py
import streamlit as st
import ollama

st.set_page_config(
    page_title="Streamlit + Ollama",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Streamlit + Ollama Integration")

# Model selection
available_models = ['llama3.2', 'mistral', 'codellama', 'phi3']
selected_model = st.selectbox("Choose Model:", available_models)

# User input
user_input = st.text_area("Enter your message:", height=100)

if st.button("Send Message", type="primary"):
    if user_input:
        try:
            with st.spinner(f"Getting response from {selected_model}..."):
                response = ollama.chat(
                    model=selected_model,
                    messages=[{'role': 'user', 'content': user_input}]
                )
                
                st.subheader("Response:")
                st.write(response['message']['content'])
                
        except Exception as e:
            st.error(f"Error: {str(e)}")
            st.info("Make sure Ollama is running and the model is installed.")
    else:
        st.warning("Please enter a message.")""")
    
    # Interactive demo
    st.markdown("### 🎮 Live Demo")
    
    demo_models = ['llama3.2', 'mistral', 'codellama', 'phi3']
    demo_model = st.selectbox("Choose Model for Demo:", demo_models, key="demo_model")
    demo_input = st.text_area("Enter your message:", height=100, key="demo_input")
    
    if st.button("Send Demo Message", type="primary", key="demo_send"):
        if demo_input:
            try:
                with st.spinner(f"Getting response from {demo_model}..."):
                    # Simulate response (replace with actual ollama call)
                    st.success("Demo mode - replace with actual Ollama integration")
                    st.markdown("**Response:** This is a simulated response. In the real app, this would be generated by your chosen AI model.")
            except Exception as e:
                st.error(f"Error: {str(e)}")
                st.info("This is a demo. In the real app, make sure Ollama is running.")
        else:
            st.warning("Please enter a message.")
    
    st.markdown("### Advanced Integration with Streaming")
    
    if st.session_state.show_code_examples:
        display_code_block("""# streaming_integration.py
import streamlit as st
import ollama

def stream_response(model, messages):
    \"\"\"Stream response from Ollama model\"\"\"
    for chunk in ollama.chat(
        model=model,
        messages=messages,
        stream=True
    ):
        yield chunk['message']['content']

st.title("🚀 Streaming AI Chat")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("What's your question?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate assistant response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        # Stream the response
        for chunk in stream_response('llama3.2', st.session_state.messages):
            full_response += chunk
            message_placeholder.markdown(full_response + "▌")
        
        message_placeholder.markdown(full_response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})""")
    
    st.markdown('<div class="highlight-box">', unsafe_allow_html=True)
    st.markdown("### 🎯 Key Features Implemented")
    st.markdown("""
    - **Real-time streaming responses** - See text appear as it's generated
    - **Chat history persistence** - Messages stay between interactions  
    - **Model selection** - Switch between different AI models
    - **Error handling** - Graceful handling of connection issues
    - **Modern chat UI** - Clean, ChatGPT-like interface
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Live streaming demo
    st.markdown("### 🎮 Streaming Demo")
    
    if "demo_messages" not in st.session_state:
        st.session_state.demo_messages = []
    
    # Display demo chat history
    for message in st.session_state.demo_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Demo chat input
    if demo_prompt := st.chat_input("Try the streaming demo (simulated)"):
        # Add user message
        st.session_state.demo_messages.append({"role": "user", "content": demo_prompt})
        
        with st.chat_message("user"):
            st.markdown(demo_prompt)
        
        # Simulate streaming response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            
            # Simulated streaming response
            demo_response = f"This is a simulated streaming response to your message: '{demo_prompt}'. In the real application, this would be generated by the AI model you selected, appearing word by word as it's generated."
            
            displayed_text = ""
            for word in demo_response.split():
                displayed_text += word + " "
                message_placeholder.markdown(displayed_text + "▌")
                time.sleep(0.1)  # Simulate streaming delay
            
            message_placeholder.markdown(displayed_text)
        
        st.session_state.demo_messages.append({"role": "assistant", "content": displayed_text.strip()})
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("✅ Mark Lesson Complete", key="complete_integration"):
        mark_lesson_complete("integration")
        st.success("Integration mastered! 🎉")
        time.sleep(1)
        st.rerun()

elif lesson_id == "chatbot":
    st.markdown('<div class="lesson-card">', unsafe_allow_html=True)
    st.title("💬 Build a Complete ChatGPT Clone")
    
    # Embedded video
    video_embed = '''
    <div style="padding: 56.25% 0 0 0; position: relative">
        <div style="height:100%;left:0;position:absolute;top:0;width:100%">
            <iframe height="100%" width="100%" src="https://embed.wave.video/qA6M90GV0M8JVcKb" frameborder="0" allow="autoplay; fullscreen" scrolling="no"></iframe>
        </div>
    </div>
    '''
    display_video(video_embed, "📹 ChatGPT Clone Walkthrough")
    
    st.markdown('<div class="project-card">', unsafe_allow_html=True)
    st.markdown("### 🎯 Project: Full-Featured ChatGPT Clone")
    st.markdown("Create a production-ready ChatGPT-like application with conversation management, multiple models, and advanced features.")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Feature breakdown
    st.markdown("### 🚀 Features We'll Implement")
    
    feature_tabs = st.tabs(["Core Features", "UI/UX", "Advanced", "Performance"])
    
    with feature_tabs[0]:
        st.markdown("""
        **Core Functionality:**
        - Real-time chat interface
        - Multiple AI model support
        - Conversation persistence
        - Message history management
        - Error handling and recovery
        """)
    
    with feature_tabs[1]:
        st.markdown("""
        **User Interface:**
        - Modern chat bubble design
        - Sidebar navigation
        - Model selection dropdown
        - Parameter controls (temperature, max tokens)
        - Responsive layout
        """)
    
    with feature_tabs[2]:
        st.markdown("""
        **Advanced Features:**
        - Multiple conversation management
        - Export/import chat history
        - System prompts and personas
        - Streaming responses
        - Custom CSS styling
        """)
    
    with feature_tabs[3]:
        st.markdown("""
        **Performance:**
        - Session state management
        - Efficient message storage
        - Error recovery
        - Memory optimization
        """)
    
    # Complete code example
    if st.session_state.show_code_examples:
        st.markdown("### 📝 Complete ChatGPT Clone Code")
        
        code_sections = st.tabs(["Main App", "State Management", "UI Components", "Ollama Integration"])
        
        with code_sections[0]:
            display_code_block("""# chatgpt_clone.py
import streamlit as st
import ollama
import json
from datetime import datetime
import uuid

# Page config
st.set_page_config(
    page_title="ChatGPT Clone",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown(\"\"\"
<style>
    .chat-message {
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 10px;
        border-left: 4px solid #667eea;
    }
    .user-message {
        background-color: #f0f2f6;
        border-left-color: #667eea;
    }
    .assistant-message {
        background-color: #ffffff;
        border-left-color: #764ba2;
        border: 1px solid #e0e0e0;
    }
</style>
\"\"\", unsafe_allow_html=True)""")
        
        with code_sections[1]:
            display_code_block("""# Session state management
def init_session_state():
    if "conversations" not in st.session_state:
        st.session_state.conversations = {}
    if "current_conversation_id" not in st.session_state:
        st.session_state.current_conversation_id = None
    if "messages" not in st.session_state:
        st.session_state.messages = []

def create_new_conversation():
    conversation_id = str(uuid.uuid4())
    st.session_state.conversations[conversation_id] = {
        "title": f"Chat {len(st.session_state.conversations) + 1}",
        "messages": [],
        "created_at": datetime.now().isoformat()
    }
    st.session_state.current_conversation_id = conversation_id
    st.session_state.messages = []
    return conversation_id

def save_message(role, content):
    message = {
        "role": role, 
        "content": content, 
        "timestamp": datetime.now().isoformat()
    }
    st.session_state.messages.append(message)
    
    if st.session_state.current_conversation_id:
        st.session_state.conversations[
            st.session_state.current_conversation_id
        ]["messages"] = st.session_state.messages""")
        
        with code_sections[2]:
            display_code_block("""# UI Components
def render_sidebar():
    with st.sidebar:
        st.title("💬 ChatGPT Clone")
        
        # New conversation button
        if st.button("+ New Chat", use_container_width=True):
            create_new_conversation()
            st.rerun()
        
        st.markdown("---")
        
        # Model settings
        st.subheader("🤖 Model Settings")
        available_models = get_available_models()
        selected_model = st.selectbox("Select Model:", available_models)
        temperature = st.slider("Temperature:", 0.0, 2.0, 0.7, 0.1)
        max_tokens = st.slider("Max Tokens:", 100, 4000, 1000, 100)
        
        return selected_model, temperature, max_tokens

def render_chat_interface():
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    return st.chat_input("Type your message here...")""")
        
        with code_sections[3]:
            display_code_block("""# Ollama integration
def get_available_models():
    try:
        models = ollama.list()
        return [model['name'] for model in models['models']]
    except:
        return ['llama3.2', 'mistral', 'codellama']

def generate_response(model, messages, temperature, max_tokens):
    try:
        # Prepare messages for API
        api_messages = []
        for msg in messages:
            if msg["role"] in ["user", "assistant"]:
                api_messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })
        
        # Stream response
        for chunk in ollama.chat(
            model=model,
            messages=api_messages,
            stream=True,
            options={
                "temperature": temperature,
                "num_predict": max_tokens
            }
        ):
            if 'message' in chunk and 'content' in chunk['message']:
                yield chunk['message']['content']
                
    except Exception as e:
        yield f"Error: {str(e)}\\n\\nPlease make sure Ollama is running."""")
    
    # Interactive demo
    st.markdown("### 🎮 Interactive Demo")
    
    # Mini chat demo
    if "chatbot_demo_messages" not in st.session_state:
        st.session_state.chatbot_demo_messages = []
    
    st.markdown("**Try the ChatGPT clone interface:**")
    
    # Demo settings
    demo_col1, demo_col2 = st.columns([3, 1])
    
    with demo_col2:
        demo_model = st.selectbox("Model:", ["llama3.2", "mistral"], key="chatbot_demo_model")
        demo_temp = st.slider("Temperature:", 0.0, 2.0, 0.7, 0.1, key="chatbot_demo_temp")
    
    with demo_col1:
        # Display demo messages
        for message in st.session_state.chatbot_demo_messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Demo chat input
        if demo_prompt := st.chat_input("Try the demo (simulated responses)"):
            # Add user message
            st.session_state.chatbot_demo_messages.append({"role": "user", "content": demo_prompt})
            
            with st.chat_message("user"):
                st.markdown(demo_prompt)
            
            # Generate demo response
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                demo_responses = [
                    f"Thank you for your message: '{demo_prompt}'. This is a simulated response using {demo_model} with temperature {demo_temp}.",
                    f"I understand you wrote: '{demo_prompt}'. In the actual app, this would be a real AI-generated response.",
                    f"That's an interesting question: '{demo_prompt}'. The real ChatGPT clone would provide detailed, context-aware responses."
                ]
                
                selected_response = demo_responses[len(st.session_state.chatbot_demo_messages) % len(demo_responses)]
                
                # Simulate streaming
                displayed = ""
                for word in selected_response.split():
                    displayed += word + " "
                    message_placeholder.markdown(displayed + "▌")
                    time.sleep(0.05)
                
                message_placeholder.markdown(displayed)
                
            st.session_state.chatbot_demo_messages.append({"role": "assistant", "content": displayed.strip()})
    
    # Clear demo button
    if st.button("🗑️ Clear Demo Chat"):
        st.session_state.chatbot_demo_messages = []
        st.rerun()
    
    st.markdown('<div class="highlight-box">', unsafe_allow_html=True)
    st.markdown("### ✨ Advanced Features Included")
    st.markdown("""
    - **Multiple conversation management** - Create, switch, and delete chats
    - **Model and parameter customization** - Choose models and adjust settings
    - **Persistent chat history** - Conversations saved in session state
    - **Real-time streaming** - See responses generate in real-time
    - **Modern UI design** - Clean, professional interface
    - **Error handling and recovery** - Graceful error management
    - **Export/import functionality** - Backup and restore conversations
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("✅ Mark Lesson Complete", key="complete_chatbot"):
        mark_lesson_complete("chatbot")
        st.success("ChatGPT clone completed! 🎉")
        time.sleep(1)
        st.rerun()

elif lesson_id == "advanced":
    st.markdown('<div class="lesson-card">', unsafe_allow_html=True)
    st.title("🚀 Advanced Features & Optimization")
    
    # Feature categories
    feature_tabs = st.tabs(["System Prompts", "File Processing", "Voice Input", "Performance", "Multi-Model"])
    
    with feature_tabs[0]:
        st.markdown("### 🎭 System Prompts & Personas")
        
        if st.session_state.show_code_examples:
            display_code_block("""# System prompts for different personas
PERSONAS = {
    "Assistant": "You are a helpful AI assistant. Provide clear and concise answers.",
    "Code Expert": "You are a senior software engineer. Help with coding questions.",
    "Creative Writer": "You are a creative writing assistant. Help with storytelling.",
    "Analyst": "You are a business analyst. Provide data-driven insights.",
    "Teacher": "You are a patient teacher. Explain concepts clearly with examples."
}

# Persona selection
persona = st.selectbox("Choose AI Persona:", list(PERSONAS.keys()))
system_prompt = PERSONAS[persona]

# Custom system prompt
if st.checkbox("Use custom system prompt"):
    system_prompt = st.text_area("Enter custom system prompt:", value=system_prompt)

def chat_with_system_prompt(model, messages, system_prompt):
    # Add system message at the beginning
    api_messages = [{"role": "system", "content": system_prompt}]
    api_messages.extend(messages)
    return ollama.chat(model=model, messages=api_messages, stream=True)""")
        
        # Interactive persona demo
        st.markdown("**Try Different Personas:**")
        demo_personas = {
            "Assistant": "You are a helpful AI assistant.",
            "Code Expert": "You are a senior software engineer.",
            "Creative Writer": "You are a creative writing assistant.",
            "Teacher": "You are a patient teacher."
        }
        
        selected_persona = st.selectbox("Choose Persona:", list(demo_personas.keys()), key="persona_demo")
        st.info(f"**System Prompt:** {demo_personas[selected_persona]}")
        
        persona_prompt = st.text_input("Ask a question to test the persona:", key="persona_question")
        if st.button("Test Persona") and persona_prompt:
            st.success(f"**{selected_persona} Response:** This would be a response tailored to the {selected_persona.lower()} persona for your question: '{persona_prompt}'")
    
    with feature_tabs[1]:
        st.markdown("### 📁 File Upload & Processing")
        
        if st.session_state.show_code_examples:
            display_code_block("""# File processing capabilities
uploaded_file = st.file_uploader(
    "Upload a document", 
    type=['txt', 'md', 'py', 'js', 'html', 'css', 'json']
)

if uploaded_file:
    # Read file content
    file_content = uploaded_file.read().decode('utf-8')
    
    st.text_area("File content:", value=file_content, height=200, disabled=True)
    
    # Analysis options
    analysis_type = st.selectbox(
        "Choose analysis type:",
        ["Summarize", "Code Review", "Explain", "Translate", "Custom"]
    )
    
    if analysis_type == "Custom":
        custom_prompt = st.text_input("Enter custom analysis prompt:")
        prompt = f"{custom_prompt}\\n\\nFile content:\\n{file_content}"
    else:
        prompts = {
            "Summarize": "Please provide a summary of this file:",
            "Code Review": "Please review this code and suggest improvements:",
            "Explain": "Please explain what this file does:",
            "Translate": "Please translate this content:"
        }
        prompt = f"{prompts[analysis_type]}\\n\\nFile content:\\n{file_content}"
    
    if st.button("Analyze File"):
        # Process with AI model
        st.info("In the real app, this would analyze your file with the selected AI model.")""")
        
        # Interactive file upload demo
        st.markdown("**Try File Upload:**")
        demo_file = st.file_uploader("Upload a demo file", type=['txt', 'md', 'py'], key="demo_file_upload")
        
        if demo_file:
            file_content = demo_file.read().decode('utf-8')
            st.text_area("File Preview:", value=file_content[:500] + "..." if len(file_content) > 500 else file_content, height=150, disabled=True)
            
            analysis_options = ["Summarize", "Code Review", "Explain"]
            selected_analysis = st.selectbox("Analysis Type:", analysis_options, key="demo_analysis")
            
            if st.button("Analyze Demo File"):
                st.success(f"**Analysis Result:** This file would be analyzed using the '{selected_analysis}' method with your chosen AI model.")
    
    with feature_tabs[2]:
        st.markdown("### 🎤 Voice Input Integration")
        
        if st.session_state.show_code_examples:
            display_code_block("""# Voice input using speech recognition
# pip install SpeechRecognition pyaudio

import speech_recognition as sr
from io import BytesIO

def transcribe_audio(audio_bytes):
    try:
        r = sr.Recognizer()
        audio_file = sr.AudioFile(BytesIO(audio_bytes))
        with audio_file as source:
            audio = r.record(source)
        text = r.recognize_google(audio)
        return text
    except Exception as e:
        return f"Error transcribing audio: {str(e)}"

# Audio input widget
audio_bytes = st.audio_input("Record your voice message")

if audio_bytes:
    st.audio(audio_bytes, format="audio/wav")
    
    if st.button("Transcribe & Send"):
        with st.spinner("Transcribing audio..."):
            transcribed_text = transcribe_audio(audio_bytes)
            st.write(f"Transcribed: {transcribed_text}")
            # Use transcribed_text as prompt for AI""")
        
        # Voice input demo
        st.markdown("**Try Voice Input:**")
        
        # Simulated audio input
        if st.button("🎤 Simulate Voice Recording"):
            st.audio("data:audio/wav;base64,UklGRnoGAABXQVZFZm10IBAAAAABAAEA...", format="audio/wav")
            st.info("In the real app, this would record your voice and transcribe it to text for AI processing.")
    
    with feature_tabs[3]:
        st.markdown("### ⚡ Performance Optimization")
        
        if st.session_state.show_code_examples:
            display_code_block("""# Caching and performance improvements
import streamlit as st
from functools import lru_cache

@st.cache_data(ttl=3600)  # Cache for 1 hour
def get_model_info(model_name):
    try:
        return ollama.show(model_name)
    except:
        return None

@st.cache_data
def load_conversation_preview(conversation_id, max_length=100):
    if conversation_id in st.session_state.conversations:
        messages = st.session_state.conversations[conversation_id]["messages"]
        if messages:
            last_message = messages[-1]["content"]
            return (last_message[:max_length] + "..." 
                   if len(last_message) > max_length 
                   else last_message)
    return "New conversation"

# Memory optimization
def cleanup_old_conversations(max_conversations=50):
    if len(st.session_state.conversations) > max_conversations:
        sorted_convs = sorted(
            st.session_state.conversations.items(),
            key=lambda x: x[1]["created_at"],
            reverse=True
        )
        st.session_state.conversations = dict(sorted_convs[:max_conversations])""")
        
        # Performance metrics
        st.markdown("**Performance Tips:**")
        
        perf_col1, perf_col2 = st.columns(2)
        
        with perf_col1:
            st.markdown("""
            **Caching:**
            - Use `@st.cache_data` for expensive operations
            - Cache model information and static data
            - Set appropriate TTL (time-to-live) values
            """)
        
        with perf_col2:
            st.markdown("""
            **Memory Management:**
            - Limit conversation history
            - Clean up old sessions
            - Optimize message storage
            """)
    
    with feature_tabs[4]:
        st.markdown("### 🔄 Multi-Model Comparison")
        
        if st.session_state.show_code_examples:
            display_code_block("""# Compare responses from multiple models
def compare_models(prompt, models=['llama3.2', 'mistral']):
    responses = {}
    
    for model in models:
        try:
            response = ollama.chat(
                model=model,
                messages=[{'role': 'user', 'content': prompt}]
            )
            responses[model] = response['message']['content']
        except Exception as e:
            responses[model] = f"Error: {str(e)}"
    
    return responses

# UI for model comparison
if st.checkbox("🔄 Compare Multiple Models"):
    available_models = get_available_models()
    selected_models = st.multiselect(
        "Select models to compare:",
        available_models,
        default=available_models[:2] if len(available_models) >= 2 else available_models
    )
    
    comparison_prompt = st.text_area("Enter prompt for comparison:")
    
    if st.button("Compare Models") and comparison_prompt and selected_models:
        with st.spinner("Getting responses from all models..."):
            responses = compare_models(comparison_prompt, selected_models)
            
            # Display responses in columns
            cols = st.columns(len(selected_models))
            
            for i, (model, response) in enumerate(responses.items()):
                with cols[i]:
                    st.subheader(f"🤖 {model}")
                    st.write(response)""")
        
        # Interactive model comparison demo
        st.markdown("**Try Model Comparison:**")
        
        demo_models = ["llama3.2", "mistral", "codellama"]
        selected_demo_models = st.multiselect(
            "Select models for comparison:",
            demo_models,
            default=demo_models[:2],
            key="comparison_models"
        )
        
        comparison_question = st.text_input("Enter question for comparison:", key="comparison_question")
        
        if st.button("Compare Demo Models") and comparison_question and selected_demo_models:
            st.markdown("**Comparison Results:**")
            
            cols = st.columns(len(selected_demo_models))
            
            for i, model in enumerate(selected_demo_models):
                with cols[i]:
                    st.markdown(f"**🤖 {model}**")
                    st.info(f"Simulated response from {model} for: '{comparison_question}'. Each model would provide its unique perspective and style.")
    
    st.markdown('<div class="highlight-box">', unsafe_allow_html=True)
    st.markdown("### 🎯 Advanced Features Summary")
    st.markdown("""
    - **System Prompts:** Customize AI behavior with personas and custom instructions
    - **File Processing:** Upload and analyze documents with AI
    - **Voice Input:** Speech-to-text integration for hands-free interaction
    - **Performance Optimization:** Caching, memory management, and efficient data handling
    - **Model Comparison:** Side-by-side evaluation of different AI models
    - **Export/Import:** Backup and restore conversation data
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("✅ Mark Lesson Complete", key="complete_advanced"):
        mark_lesson_complete("advanced")
        st.success("Advanced features mastered! 🎉")
        time.sleep(1)
        st.rerun()

elif lesson_id == "deployment":
    st.markdown('<div class="lesson-card">', unsafe_allow_html=True)
    st.title("🌐 Deployment & Production")
    
    deployment_tabs = st.tabs(["Preparation", "Docker", "Cloud Platforms", "Monitoring", "Security"])
    
    with deployment_tabs[0]:
        st.markdown("### 🛠️ Preparing for Production")
        
        if st.session_state.show_code_examples:
            display_code_block("""# requirements.txt
streamlit>=1.28.0
ollama>=0.1.7
requests>=2.31.0
python-dotenv>=1.0.0
SpeechRecognition>=3.10.0
pyaudio>=0.2.11
pandas>=2.0.0
uuid>=1.30""", "text")
            
            display_code_block("""# .env file for configuration
OLLAMA_HOST=localhost:11434
DEFAULT_MODEL=llama3.2
MAX_CONVERSATIONS=100
ENABLE_VOICE_INPUT=true
ENABLE_FILE_UPLOAD=true
ADMIN_PASSWORD=your_secure_password""", "bash")
            
            display_code_block("""# config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OLLAMA_HOST = os.getenv('OLLAMA_HOST', 'localhost:11434')
    DEFAULT_MODEL = os.getenv('DEFAULT_MODEL', 'llama3.2')
    MAX_CONVERSATIONS = int(os.getenv('MAX_CONVERSATIONS', 100))
    ENABLE_VOICE_INPUT = os.getenv('ENABLE_VOICE_INPUT', 'true').lower() == 'true'
    ENABLE_FILE_UPLOAD = os.getenv('ENABLE_FILE_UPLOAD', 'true').lower() == 'true'
    ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'admin')""")
        
        # Preparation checklist
        st.markdown("**🔧 Production Checklist:**")
        
        checklist_items = [
            "Environment variables configured",
            "Dependencies pinned in requirements.txt",
            "Error handling implemented",
            "Logging configured",
            "Rate limiting added",
            "Security headers configured",
            "Health checks implemented",
            "Monitoring enabled"
        ]
        
        checklist_col1, checklist_col2 = st.columns(2)
        
        for i, item in enumerate(checklist_items):
            with checklist_col1 if i % 2 == 0 else checklist_col2:
                st.checkbox(f"✅ {item}", key=f"checklist_{i}")
    
    with deployment_tabs[1]:
        st.markdown("### 🐳 Docker Deployment")
        
        if st.session_state.show_code_examples:
            display_code_block("""# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    portaudio19-dev \\
    python3-pyaudio \\
    curl \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose Streamlit port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run the application
CMD ["streamlit", "run", "chatgpt_clone.py", "--server.port=8501", "--server.address=0.0.0.0"]""", "dockerfile")
            
            display_code_block("""# docker-compose.yml
version: '3.8'

services:
  ollama:
    image: ollama/ollama:latest
    ports:
      - "11434:11434"
    volumes:
      - ollama:/root/.ollama
    restart: unless-stopped
    environment:
      - OLLAMA_ORIGINS=*

  streamlit-app:
    build: .
    ports:
      - "8501:8501"
    environment:
      - OLLAMA_HOST=ollama:11434
    depends_on:
      - ollama
    restart: unless-stopped

volumes:
  ollama:""", "yaml")
            
            display_code_block("""# Build and run with Docker
# Build the image
docker build -t streamlit-ollama-app .

# Run with docker-compose
docker-compose up -d

# View logs
docker-compose logs -f streamlit-app

# Stop services
docker-compose down""", "bash")
        
        # Docker deployment steps
        st.markdown("**🚀 Docker Deployment Steps:**")
        
        docker_steps = [
            "Create Dockerfile with all dependencies",
            "Set up docker-compose.yml for multi-service deployment",
            "Build and test locally",
            "Deploy to production server",
            "Set up monitoring and logging"
        ]
        
        for i, step in enumerate(docker_steps, 1):
            st.markdown(f'<span class="step-counter">{i}</span>**{step}**', unsafe_allow_html=True)
    
    with deployment_tabs[2]:
        st.markdown("### ☁️ Cloud Platform Deployment")
        
        platform_options = st.radio(
            "Choose deployment platform:",
            ["Streamlit Cloud", "AWS", "Google Cloud", "Azure", "DigitalOcean"]
        )
        
        if platform_options == "Streamlit Cloud":
            st.markdown('<div class="highlight-box">', unsafe_allow_html=True)
            st.markdown("**🚀 Streamlit Cloud Deployment**")
            st.markdown("""
            1. Push your code to GitHub
            2. Connect to Streamlit Cloud (share.streamlit.io)
            3. Deploy with one click
            
            **Note:** Ollama needs to run on a separate server as Streamlit Cloud doesn't support local model hosting.
            """)
            st.markdown('</div>', unsafe_allow_html=True)
        
        elif platform_options == "AWS":
            if st.session_state.show_code_examples:
                display_code_block("""# AWS EC2 deployment script
#!/bin/bash

# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Install Docker Compose
sudo apt install docker-compose -y

# Clone your repository
git clone https://github.com/yourusername/streamlit-ollama-app.git
cd streamlit-ollama-app

# Start services
docker-compose up -d

# Set up nginx reverse proxy (optional)
sudo apt install nginx -y
# Configure nginx for your domain""", "bash")
        
        elif platform_options == "Google Cloud":
            if st.session_state.show_code_examples:
                display_code_block("""# Google Cloud Run deployment
# Build and push to Container Registry
gcloud builds submit --tag gcr.io/PROJECT-ID/streamlit-app

# Deploy to Cloud Run
gcloud run deploy streamlit-app \\
  --image gcr.io/PROJECT-ID/streamlit-app \\
  --platform managed \\
  --region us-central1 \\
  --allow-unauthenticated \\
  --memory 2Gi \\
  --cpu 2""", "bash")
        
        elif platform_options == "Azure":
            st.markdown("**Azure Container Instances:**")
            st.markdown("""
            - Use Azure Container Instances for simple deployment
            - Azure App Service for web apps
            - Azure Kubernetes Service for scalable solutions
            """)
        
        elif platform_options == "DigitalOcean":
            st.markdown("**DigitalOcean Droplet:**")
            st.markdown("""
            - Create a droplet with Docker pre-installed
            - Use App Platform for managed deployment
            - Set up load balancers for high availability
            """)
    
    with deployment_tabs[3]:
        st.markdown("### 📊 Monitoring & Analytics")
        
        if st.session_state.show_code_examples:
            display_code_block("""# monitoring.py
import streamlit as st
import time
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def track_usage(event_type, details=None):
    \"\"\"Track application usage\"\"\"
    if "usage_stats" not in st.session_state:
        st.session_state.usage_stats = []
    
    event = {
        "timestamp": datetime.now().isoformat(),
        "event_type": event_type,
        "details": details or {},
        "session_id": st.session_state.get("session_id", "unknown")
    }
    
    st.session_state.usage_stats.append(event)
    logger.info(f"Event: {event_type} - {details}")

def log_error(error, context=""):
    \"\"\"Log errors for monitoring\"\"\"
    logger.error(f"Error in {context}: {str(error)}")
    
    # In production, send to monitoring service
    # send_to_monitoring_service(error, context)

# Usage examples
track_usage("message_sent", {"model": "llama3.2", "length": len(prompt)})
track_usage("conversation_created")
track_usage("model_switched", {"from": "llama3.2", "to": "mistral"})""")
        
        # Monitoring metrics
        st.markdown("**📈 Key Metrics to Track:**")
        
        metrics_col1, metrics_col2 = st.columns(2)
        
        with metrics_col1:
            st.markdown("""
            **Usage Metrics:**
            - Messages sent per day
            - Active users
            - Model usage patterns
            - Session duration
            """)
        
        with metrics_col2:
            st.markdown("""
            **Performance Metrics:**
            - Response time
            - Error rates
            - Memory usage
            - CPU utilization
            """)
        
        # Sample monitoring dashboard
        st.markdown("**📊 Sample Metrics Dashboard:**")
        
        dashboard_col1, dashboard_col2, dashboard_col3, dashboard_col4 = st.columns(4)
        
        with dashboard_col1:
            st.metric("Daily Users", "1,234", "12%")
        with dashboard_col2:
            st.metric("Messages Today", "5,678", "8%")
        with dashboard_col3:
            st.metric("Avg Response Time", "2.3s", "-0.2s")
        with dashboard_col4:
            st.metric("Error Rate", "0.5%", "-0.1%")
    
    with deployment_tabs[4]:
        st.markdown("### 🔒 Security Considerations")
        
        if st.session_state.show_code_examples:
            display_code_block("""# security.py
import streamlit as st
import hashlib
import time
from functools import wraps

def rate_limit(max_requests=10, window=3600):
    \"\"\"Simple rate limiting decorator\"\"\"
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user_id = st.session_state.get("user_id", "anonymous")
            
            if f"rate_limit_{user_id}" not in st.session_state:
                st.session_state[f"rate_limit_{user_id}"] = {
                    "count": 0, 
                    "reset_time": time.time() + window
                }
            
            current_time = time.time()
            rate_data = st.session_state[f"rate_limit_{user_id}"]
            
            if current_time > rate_data["reset_time"]:
                rate_data["count"] = 0
                rate_data["reset_time"] = current_time + window
            
            if rate_data["count"] >= max_requests:
                st.error("Rate limit exceeded. Please try again later.")
                return None
            
            rate_data["count"] += 1
            return func(*args, **kwargs)
        
        return wrapper
    return decorator

def sanitize_input(text):
    \"\"\"Sanitize user input\"\"\"
    # Remove potentially harmful content
    import re
    
    # Remove script tags
    text = re.sub(r'<script.*?</script>', '', text, flags=re.DOTALL | re.IGNORECASE)
    
    # Remove other HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    
    # Limit length
    if len(text) > 10000:
        text = text[:10000] + "... [truncated]"
    
    return text

def require_auth():
    \"\"\"Simple authentication check\"\"\"
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    
    if not st.session_state.authenticated:
        password = st.text_input("Enter password:", type="password")
        if st.button("Login"):
            if password == st.secrets.get("ADMIN_PASSWORD", "admin"):
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Invalid password")
        return False
    
    return True""")
        
        st.markdown('<div class="warning-box">', unsafe_allow_html=True)
        st.markdown("**🔒 Security Best Practices:**")
        st.markdown("""
        - **Never expose Ollama directly** to the internet
        - **Use HTTPS in production** with valid SSL certificates
        - **Implement proper authentication** if handling sensitive data
        - **Sanitize user inputs** to prevent injection attacks
        - **Set up proper firewall rules** to restrict access
        - **Use environment variables** for sensitive configuration
        - **Implement rate limiting** to prevent abuse
        - **Log security events** for monitoring
        - **Keep dependencies updated** to patch security vulnerabilities
        - **Use secrets management** for passwords and API keys
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Final project showcase
    st.markdown("### 🏆 Course Completion")
    
    st.markdown('<div class="project-card">', unsafe_allow_html=True)
    st.markdown("### 🎉 Congratulations!")
    st.markdown("""
    You've successfully completed the **Streamlit + Ollama Course**! You now have the comprehensive skills to:
    
    ✅ **Build interactive AI-powered web applications** with Streamlit
    ✅ **Integrate local AI models** using Ollama for privacy and control
    ✅ **Create production-ready chat applications** with advanced features
    ✅ **Deploy applications to cloud platforms** for public access
    ✅ **Implement security, monitoring, and optimization** best practices
    ✅ **Handle advanced features** like voice input, file processing, and multi-model comparison
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("### 🚀 Next Steps & Resources")
    
    next_steps_col1, next_steps_col2 = st.columns(2)
    
    with next_steps_col1:
        st.markdown("""
        **🎯 Project Ideas:**
        - Personal AI assistant
        - Code review tool
        - Document analyzer
        - Creative writing helper
        - Customer support chatbot
        """)
    
    with next_steps_col2:
        st.markdown("""
        **📚 Continue Learning:**
        - Explore more Ollama models
        - Add database integration
        - Implement user authentication
        - Build mobile-responsive UI
        - Add real-time collaboration
        """)
    
    # Course completion certificate
    if st.button("🎓 Generate Course Completion Certificate"):
        st.balloons()
        st.markdown('<div class="success-box">', unsafe_allow_html=True)
        st.markdown(f"""
        ### 🎓 Certificate of Completion
        
        **This certifies that you have successfully completed the**
        
        # Streamlit + Ollama Course
        **Master AI-Powered Web Applications with Python**
        
        **Completed on:** {datetime.now().strftime("%B %d, %Y")}
        
        **Course Progress:** {get_progress_percentage()}% Complete
        
        *You are now equipped to build, deploy, and maintain AI-powered web applications using Streamlit and Ollama!*
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("✅ Mark Lesson Complete", key="complete_deployment"):
        mark_lesson_complete("deployment")
        st.success("Course completed! 🎉🎊")
        st.balloons()
        time.sleep(1)
        st.rerun()

# Navigation buttons
col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    if st.session_state.current_lesson > 0:
        if st.button("⬅️ Previous Lesson"):
            st.session_state.current_lesson -= 1
            st.rerun()

with col3:
    if st.session_state.current_lesson < len(LESSONS) - 1:
        if st.button("Next Lesson ➡️"):
            st.session_state.current_lesson += 1
            st.rerun()

# Footer
st.markdown("---")
st.markdown("### 💡 Course Information")

footer_col1, footer_col2, footer_col3 = st.columns(3)

with footer_col1:
    st.markdown("""
    **🎯 Course Stats:**
    - 8 comprehensive lessons
    - 50+ code examples
    - 3 embedded videos
    - Interactive demos
    """)

with footer_col2:
    st.markdown("""
    **🛠️ Technologies:**
    - Streamlit for web apps
    - Ollama for local AI
    - Python for backend
    - Docker for deployment
    """)

with footer_col3:
    st.markdown("""
    **📚 Learning Outcomes:**
    - Full-stack AI applications
    - Production deployment
    - Best practices & security
    - Advanced optimizations
    """)

st.markdown("---")
st.markdown("**Built with ❤️ using Streamlit** | Course Progress: {}%".format(get_progress_percentage()))

# Auto-save progress
if st.session_state.lesson_progress:
    st.session_state["last_activity"] = datetime.now().isoformat()
