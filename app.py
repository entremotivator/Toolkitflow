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
        st.markdown("### Multi-Model Comparison")
        
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
if st.checkbox("Compare Multiple Models"):
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
                    st.subheader(f"{model}")
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
                    st.markdown(f"**{model}**")
                    st.info(f"Simulated response from {model} for: '{comparison_question}'. Each model would provide its unique perspective and style.")
    
    st.markdown('<div class="highlight-box">', unsafe_allow_html=True)
    st.markdown("### Advanced Features Summary")
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
    
    if st.button("Mark Lesson Complete", key="complete_advanced"):
        mark_lesson_complete("advanced")
        st.success("Advanced features mastered!")
        time.sleep(1)
        st.rerun()

elif lesson_id == "deployment":
    st.markdown('<div class="lesson-card">', unsafe_allow_html=True)
    st.title("Deployment & Production")
    
    deployment_tabs = st.tabs(["Preparation", "Docker", "Cloud Platforms", "Security"])
    
    with deployment_tabs[0]:
        st.markdown("### Preparing for Production")
        
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
        
        # Preparation checklist
        st.markdown("**Production Checklist:**")
        
        checklist_items = [
            "Environment variables configured",
            "Dependencies pinned in requirements.txt",
            "Error handling implemented",
            "Logging configured",
            "Security headers configured",
            "Health checks implemented"
        ]
        
        for i, item in enumerate(checklist_items):
            st.checkbox(f"{item}", key=f"checklist_{i}")
    
    with deployment_tabs[1]:
        st.markdown("### Docker Deployment")
        
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
    
    with deployment_tabs[2]:
        st.markdown("### Cloud Platform Deployment")
        
        platform_options = st.radio(
            "Choose deployment platform:",
            ["Streamlit Cloud", "AWS", "Google Cloud", "Azure"]
        )
        
        if platform_options == "Streamlit Cloud":
            st.markdown('<div class="highlight-box">', unsafe_allow_html=True)
            st.markdown("**Streamlit Cloud Deployment**")
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
docker-compose up -d""", "bash")
        
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
  --allow-unauthenticated""", "bash")
    
    with deployment_tabs[3]:
        st.markdown("### Security Considerations")
        
        if st.session_state.show_code_examples:
            display_code_block("""# security.py
import streamlit as st
import hashlib
import time
from functools import wraps

def rate_limit(max_requests=10, window=3600):
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
    return decorator""")
        
        st.markdown('<div class="warning-box">', unsafe_allow_html=True)
        st.markdown("**Security Best Practices:**")
        st.markdown("""
        - Never expose Ollama directly to the internet
        - Use HTTPS in production with valid SSL certificates
        - Implement proper authentication if handling sensitive data
        - Sanitize user inputs to prevent injection attacks
        - Set up proper firewall rules to restrict access
        - Use environment variables for sensitive configuration
        - Implement rate limiting to prevent abuse
        - Keep dependencies updated to patch security vulnerabilities
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Course completion
    st.markdown("### Course Completion")
    
    st.markdown('<div class="project-card">', unsafe_allow_html=True)
    st.markdown("### Congratulations!")
    st.markdown("""
    You've successfully completed the **Streamlit + Ollama Course**! You now have the comprehensive skills to:
    
    - Build interactive AI-powered web applications with Streamlit
    - Integrate local AI models using Ollama for privacy and control
    - Create production-ready chat applications with advanced features
    - Deploy applications to cloud platforms for public access
    - Implement security, monitoring, and optimization best practices
    - Handle advanced features like voice input, file processing, and multi-model comparison
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Course completion certificate
    if st.button("Generate Course Completion Certificate"):
        st.balloons()
        st.markdown('<div class="success-box">', unsafe_allow_html=True)
        st.markdown(f"""
        ### Certificate of Completion
        
        **This certifies that you have successfully completed the**
        
        # Streamlit + Ollama Course
        **Master AI-Powered Web Applications with Python**
        
        **Completed on:** {datetime.now().strftime("%B %d, %Y")}
        
        **Course Progress:** {get_progress_percentage()}% Complete
        
        *You are now equipped to build, deploy, and maintain AI-powered web applications using Streamlit and Ollama!*
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("Mark Lesson Complete", key="complete_deployment"):
        mark_lesson_complete("deployment")
        st.success("Course completed!")
        st.balloons()
        time.sleep(1)
        st.rerun()

# Navigation buttons
col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    if st.session_state.current_lesson > 0:
        if st.button("Previous Lesson"):
            st.session_state.current_lesson -= 1
            st.rerun()

with col3:
    if st.session_state.current_lesson < len(LESSONS) - 1:
        if st.button("Next Lesson"):
            st.session_state.current_lesson += 1
            st.rerun()

# Footer
st.markdown("---")
st.markdown("### Course Information")

footer_col1, footer_col2, footer_col3 = st.columns(3)

with footer_col1:
    st.markdown("""
    **Course Stats:**
    - 8 comprehensive lessons
    - 50+ code examples
    - Interactive demos
    - Production deployment
    """)

with footer_col2:
    st.markdown("""
    **Technologies:**
    - Streamlit for web apps
    - Ollama for local AI
    - Python for backend
    - Docker for deployment
    """)

with footer_col3:
    st.markdown("""
    **Learning Outcomes:**
    - Full-stack AI applications
    - Production deployment
    - Best practices & security
    - Advanced optimizations
    """)

st.markdown("---")
st.markdown("**Built with Streamlit** | Course Progress: {}%".format(get_progress_percentage()))

# Auto-save progress
if st.session_state.lesson_progress:
    st.session_state["last_activity"] = datetime.now().isoformat()# streamlit_ollama_course.py
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
    {"id": "intro", "title": "Introduction", "icon": "🎯"},
    {"id": "setup", "title": "Setup & Installation", "icon": "⚙️"},
    {"id": "streamlit_basics", "title": "Streamlit Basics", "icon": "🎨"},
    {"id": "ollama_setup", "title": "Ollama Setup", "icon": "🤖"},
    {"id": "integration", "title": "Integration", "icon": "🔗"},
    {"id": "chatbot", "title": "ChatGPT Clone", "icon": "💬"},
    {"id": "advanced", "title": "Advanced Features", "icon": "🚀"},
    {"id": "deployment", "title": "Deployment", "icon": "🌐"}
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
    
    st.markdown('<div class="code-block">', unsafe_allow_html=True)
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
    st.title("Course Navigation")
    
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
            f"{completed_icon} {current_icon} {lesson['icon']} {lesson['title']}", 
            key=f"nav_{lesson['id']}",
            use_container_width=True,
            type="primary" if i == st.session_state.current_lesson else "secondary"
        ):
            st.session_state.current_lesson = i
            st.rerun()
    
    st.markdown("---")
    
    # Settings
    st.subheader("Settings")
    st.session_state.show_code_examples = st.checkbox(
        "Show Code Examples", 
        value=st.session_state.show_code_examples
    )
    
    # Export/Import Progress
    st.subheader("Progress Management")
    
    # Export progress
    if st.button("Export Progress"):
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
    uploaded_progress = st.file_uploader("Import Progress", type=['json'])
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
    <h1>Streamlit + Ollama Course</h1>
    <h3>Master AI-Powered Web Applications with Python</h3>
    <p>Build ChatGPT-like applications with local AI models</p>
</div>
""", unsafe_allow_html=True)

# Lesson content based on current selection
lesson_id = current_lesson["id"]

if lesson_id == "intro":
    st.markdown('<div class="lesson-card">', unsafe_allow_html=True)
    st.title("Course Introduction")
    
    st.markdown('<div class="highlight-box">', unsafe_allow_html=True)
    st.markdown("### What You'll Learn")
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
        st.markdown("### Prerequisites")
        st.markdown("""
        - Basic Python knowledge
        - Understanding of web concepts
        - Python 3.8+ installed
        - 8GB+ RAM recommended for Ollama
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="warning-box">', unsafe_allow_html=True)
        st.markdown("### Required Tools")
        st.markdown("""
        - Python 3.8+
        - Code editor (VS Code recommended)
        - Terminal/Command prompt
        - Web browser
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="project-card">', unsafe_allow_html=True)
    st.markdown("### Course Objectives")
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
    
    if st.button("Mark Lesson Complete", key="complete_intro"):
        mark_lesson_complete("intro")
        st.success("Lesson completed!")
        time.sleep(1)
        st.rerun()

elif lesson_id == "setup":
    st.markdown('<div class="lesson-card">', unsafe_allow_html=True)
    st.title("Setup & Installation")
    
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
    st.markdown("**Pro Tip:** Always use virtual environments to avoid package conflicts and maintain clean project dependencies.")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Interactive verification
    st.markdown("### Interactive Verification")
    
    if st.button("Test Streamlit Import"):
        try:
            import streamlit as st_test
            st.success(f"Streamlit {st_test.__version__} imported successfully!")
        except ImportError:
            st.error("Streamlit not found. Please install it first.")
    
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
    
    if st.button("Mark Lesson Complete", key="complete_setup"):
        mark_lesson_complete("setup")
        st.success("Setup completed!")
        time.sleep(1)
        st.rerun()

elif lesson_id == "streamlit_basics":
    st.markdown('<div class="lesson-card">', unsafe_allow_html=True)
    st.title("Streamlit Fundamentals")
    
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
st.title("Welcome to Streamlit!")
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
    
    st.markdown("### Interactive Demo")
    
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
            import pandas as pd
            import numpy as np
            data = pd.DataFrame(
                np.random.randn(5, 3),
                columns=['A', 'B', 'C']
            )
            st.dataframe(data)
    
    st.markdown('<div class="highlight-box">', unsafe_allow_html=True)
    st.markdown("### Key Streamlit Concepts")
    st.markdown("""
    - **Widgets:** Interactive elements (buttons, sliders, inputs)
    - **Layout:** Columns, sidebars, containers  
    - **State Management:** Session state for persistence
    - **Caching:** @st.cache for performance
    - **Components:** Custom HTML/JavaScript components
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("Mark Lesson Complete", key="complete_streamlit_basics"):
        mark_lesson_complete("streamlit_basics")
        st.success("Streamlit basics mastered!")
        time.sleep(1)
        st.rerun()

elif lesson_id == "ollama_setup":
    st.markdown('<div class="lesson-card">', unsafe_allow_html=True)
    st.title("Ollama Setup & Configuration")
    
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
    st.markdown("**System Requirements:** Ollama requires significant RAM. For Llama 3.2 (7B), you need at least 8GB RAM. Larger models require more memory.")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Step 3
    st.markdown('<span class="step-counter">3</span>**Python Integration Setup**', unsafe_allow_html=True)
    
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
    print("Ollama is working correctly!")
    
except Exception as e:
    print(f"Error: {e}")
    print("Make sure Ollama is running and llama3.2 is installed")""")
    
    # Interactive test section
    st.markdown("### Test Your Ollama Setup")
    
    if st.button("Test Ollama Connection"):
        try:
            import ollama
            models = ollama.list()
            st.success("Ollama connected successfully!")
            st.json(models)
        except Exception as e:
            st.error(f"Connection failed: {str(e)}")
            st.info("Make sure Ollama is installed and running")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("Mark Lesson Complete", key="complete_ollama_setup"):
        mark_lesson_complete("ollama_setup")
        st.success("Ollama setup completed!")
        time.sleep(1)
        st.rerun()

elif lesson_id == "integration":
    st.markdown('<div class="lesson-card">', unsafe_allow_html=True)
    st.title("Streamlit + Ollama Integration")
    
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

st.title("Streamlit + Ollama Integration")

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
    st.markdown("### Live Demo")
    
    demo_models = ['llama3.2', 'mistral', 'codellama', 'phi3']
    demo_model = st.selectbox("Choose Model for Demo:", demo_models, key="demo_model")
    demo_input = st.text_area("Enter your message:", height=100, key="demo_input")
    
    if st.button("Send Demo Message", type="primary", key="demo_send"):
        if demo_input:
            try:
                with st.spinner(f"Getting response from {demo_model}..."):
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
    for chunk in ollama.chat(
        model=model,
        messages=messages,
        stream=True
    ):
        yield chunk['message']['content']

st.title("Streaming AI Chat")

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
    st.markdown("### Key Features Implemented")
    st.markdown("""
    - **Real-time streaming responses** - See text appear as it's generated
    - **Chat history persistence** - Messages stay between interactions  
    - **Model selection** - Switch between different AI models
    - **Error handling** - Graceful handling of connection issues
    - **Modern chat UI** - Clean, ChatGPT-like interface
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("Mark Lesson Complete", key="complete_integration"):
        mark_lesson_complete("integration")
        st.success("Integration mastered!")
        time.sleep(1)
        st.rerun()

elif lesson_id == "chatbot":
    st.markdown('<div class="lesson-card">', unsafe_allow_html=True)
    st.title("Build a Complete ChatGPT Clone")
    
    st.markdown('<div class="project-card">', unsafe_allow_html=True)
    st.markdown("### Project: Full-Featured ChatGPT Clone")
    st.markdown("Create a production-ready ChatGPT-like application with conversation management, multiple models, and advanced features.")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Complete code example
    if st.session_state.show_code_examples:
        st.markdown("### Complete ChatGPT Clone Code")
        
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
st.markdown('''
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
''', unsafe_allow_html=True)""")
        
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
        st.title("ChatGPT Clone")
        
        # New conversation button
        if st.button("+ New Chat", use_container_width=True):
            create_new_conversation()
            st.rerun()
        
        st.markdown("---")
        
        # Model settings
        st.subheader("Model Settings")
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
