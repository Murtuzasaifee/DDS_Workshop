import streamlit as st
import requests
import json
from datetime import datetime
import time

# Page configuration
st.set_page_config(
    page_title="AI Blog Generator",
    page_icon="✍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #2E86AB;
        font-size: 3rem;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    
    .blog-container {
        background-color: #f8f9fa;
        padding: 2rem;
        border-radius: 10px;
        border-left: 5px solid #2E86AB;
        margin: 1rem 0;
    }
    
    .quote-style {
        font-style: italic;
        font-size: 1.2rem;
        color: #495057;
        background-color: #e9ecef;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
        border-left: 4px solid #28a745;
    }
    
    .metadata-box {
        background-color: #e3f2fd;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #c3e6cb;
        margin: 1rem 0;
    }
    
    .error-message {
        background-color: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #f5c6cb;
        margin: 1rem 0;
    }
    
    .stButton > button {
        background-color: #2E86AB;
        color: white;
        border: none;
        padding: 0.5rem 2rem;
        border-radius: 5px;
        font-weight: bold;
        transition: background-color 0.3s;
    }
    
    .stButton > button:hover {
        background-color: #1f5f82;
    }
</style>
""", unsafe_allow_html=True)

# Main header
st.markdown('<h1 class="main-header">🤖 AI Blog Generator</h1>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # API endpoint (pre-configured)
    api_url = "https://meloito468.execute-api.us-east-1.amazonaws.com/blog_generator"
    st.text_input(
        "API Endpoint",
        value=api_url,
        disabled=True,
        help="Your AWS API Gateway endpoint"
    )
    
    st.markdown("---")
    
    # About section
    st.markdown("""
    ### 📝 About
    This app connects to your AWS Lambda function to generate AI-powered blog posts using Amazon Nova Premier.
    
    **Features:**
    - ✨ AI-powered content generation
    - 📊 Inspirational quotes integration
    - ☁️ Automatic S3 storage
    - 📱 Real-time preview
    - 🔗 AWS API Gateway integration
    """)

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.header("📝 Generate New Blog")
    
    # Topic input
    topic = st.text_input(
        "Blog Topic",
        placeholder="Enter your blog topic (e.g., 'AI in healthcare', 'Future of technology')",
        help="Provide a clear and specific topic for your blog post"
    )
    
    # Generate button
    if st.button("🚀 Generate Blog", type="primary"):
        if not topic:
            st.error("Please enter a blog topic!")
        else:
            with st.spinner("Generating your blog post... This may take a few moments."):
                try:
                    # API endpoint
                    api_url = "https://meloito468.execute-api.us-east-1.amazonaws.com/blog_generator"
                    
                    # Prepare the request payload
                    payload = {
                        "topic": topic
                    }
                    
                    # Make POST request to API Gateway
                    response = requests.post(
                        api_url,
                        json=payload,
                        headers={
                            'Content-Type': 'application/json',
                            'Accept': 'application/json'
                        },
                        timeout=60  # Increased timeout for Lambda cold starts
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        
                        # Store in session state
                        st.session_state.blog_result = result
                        st.session_state.generation_time = datetime.now()
                        
                        st.success("✅ Blog generated successfully!")
                        st.balloons()  # Fun animation on success
                        
                    else:
                        st.error(f"❌ API Error: {response.status_code}")
                        if response.text:
                            st.error(f"Response: {response.text}")
                        
                except requests.exceptions.Timeout:
                    st.error("⏰ Request timed out. The Lambda function might be experiencing a cold start. Please try again.")
                except requests.exceptions.RequestException as e:
                    st.error(f"🔗 Connection error: {str(e)}")
                except json.JSONDecodeError:
                    st.error("📄 Invalid JSON response from API")
                except Exception as e:
                    st.error(f"❌ Unexpected error: {str(e)}")

with col2:
    st.header("📊 Quick Stats")
    
    # Display some stats or recent activity
    if 'blog_result' in st.session_state:
        result = st.session_state.blog_result
        
        st.metric("Status", "✅ Success")
        st.metric("Word Count", len(result.get('content', '').split()))
        st.metric("Generated", st.session_state.generation_time.strftime("%H:%M:%S"))
    else:
        st.info("Generate a blog to see statistics")

# Display blog result if available
if 'blog_result' in st.session_state:
    st.markdown("---")
    st.header("📄 Generated Blog Post")
    
    result = st.session_state.blog_result
    
    # Extract quote from content (assuming it starts with a quote)
    content = result.get('content', '')
    if content.startswith('"') and '"' in content[1:]:
        quote_end = content.find('"', 1) + 1
        quote = content[:quote_end]
        main_content = content[quote_end:].strip()
    else:
        quote = ""
        main_content = content
    
    # Display quote if found
    if quote:
        st.markdown(f'<div class="quote-style">{quote}</div>', unsafe_allow_html=True)
    
    # Display main content
    st.markdown(f'<div class="blog-container">{main_content}</div>', unsafe_allow_html=True)
    
    # Metadata section
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="metadata-box">
            <strong>📝 Topic:</strong><br>
            {result.get('topic', 'N/A')}
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metadata-box">
            <strong>📁 File Name:</strong><br>
            {result.get('file_name', 'N/A')}
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metadata-box">
            <strong>⏰ Timestamp:</strong><br>
            {result.get('timestamp', 'N/A')}
        </div>
        """, unsafe_allow_html=True)
    
    # Download options
    st.markdown("---")
    st.subheader("💾 Download Options")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Download as text
        st.download_button(
            label="📄 Download as TXT",
            data=content,
            file_name=f"blog_{result.get('timestamp', 'generated')}.txt",
            mime="text/plain"
        )
    
    with col2:
        # Download as JSON
        st.download_button(
            label="📋 Download as JSON",
            data=json.dumps(result, indent=2),
            file_name=f"blog_data_{result.get('timestamp', 'generated')}.json",
            mime="application/json"
        )
    
    with col3:
        # Copy to clipboard button (using JavaScript)
        if st.button("📋 Copy Content"):
            st.code(content, language="text")
            st.info("💡 Select and copy the text above")

# Sample data section
st.markdown("---")
with st.expander("📋 View Sample Response Format"):
    sample_response = {
        "content": "\"If you can't fly then run, if you can't run then walk, if you can't walk then crawl, but whatever you do you have to keep moving forward.\" This quote embodies the relentless spirit of sports, now enhanced by AI. Artificial Intelligence is revolutionizing athletics, from performance analysis to fan engagement...",
        "message": "Blog generated successfully!!",
        "topic": "AI in sports",
        "file_name": "blogs/2025-06-10-08-19-13.txt",
        "timestamp": "2025-06-10-08-19-13"
    }
    st.json(sample_response)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6c757d; margin-top: 2rem;">
    <p>🚀 Powered by AWS API Gateway & Amazon Nova Premier | Built with Streamlit ❤️</p>
    <p><strong>API Endpoint:</strong> https://meloito468.execute-api.us-east-1.amazonaws.com/blog_generator</p>
</div>
""", unsafe_allow_html=True)