"""
MicDrop - AI Public Speaking Coach
Main Streamlit application entry point
"""

import streamlit as st
import os

# Page configuration
st.set_page_config(
    page_title="MicDrop - AI Public Speaking Coach",
    page_icon="🎤",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .sub-header {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    </style>
""", unsafe_allow_html=True)

def main():
    """Main application function"""
    
    # Header
    st.markdown('<h1 class="main-header">🎤 MicDrop</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">AI-Powered Public Speaking Coach</p>', unsafe_allow_html=True)
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Choose Analysis Type",
        ["🏠 Home", "🎙️ Voice Analysis", "📝 Language Analysis", "👤 Body Language Analysis", "📊 Comprehensive Report"]
    )
    
    # Route to appropriate page
    if page == "🏠 Home":
        show_home()
    elif page == "🎙️ Voice Analysis":
        from page_modules import voice_analysis
        voice_analysis.show()
    elif page == "📝 Language Analysis":
        from page_modules import language_analysis
        language_analysis.show()
    elif page == "👤 Body Language Analysis":
        from page_modules import body_language_analysis
        body_language_analysis.show()
    elif page == "📊 Comprehensive Report":
        from page_modules import comprehensive_report
        comprehensive_report.show()

def show_home():
    """Display home page with instructions"""
    
    st.markdown("## Welcome to MicDrop! 🎤")
    
    st.markdown("""
    **MicDrop** is your AI-powered public speaking coach that provides comprehensive 
    feedback on three key aspects of your presentation:
    
    ### 🎙️ Voice Analysis
    - **Pace**: Words per minute, speaking rate
    - **Pitch**: Average pitch and variation
    - **Pauses**: Frequency and duration
    - **Volume**: Consistency and variation
    - **Clarity**: Articulation quality
    
    ### 📝 Language Analysis
    - **Clarity**: Sentence structure and complexity
    - **Word Choice**: Vocabulary diversity
    - **Filler Words**: Detection and frequency
    - **Structure**: Organization and coherence
    - **Tone**: Formality and engagement
    
    ### 👤 Body Language Analysis
    - **Posture**: Body alignment and stance
    - **Gestures**: Hand movements and frequency
    - **Eye Contact**: Gaze direction
    - **Facial Expressions**: Engagement indicators
    - **Presence**: Overall stage presence
    
    ---
    
    ### 🚀 Getting Started
    
    1. **Choose an analysis type** from the sidebar
    2. **Upload or record** your audio/video
    3. **Wait for processing** (usually < 30 seconds)
    4. **Review your feedback** and recommendations
    5. **Practice and improve!**
    
    ---
    
    ### 💡 Tips for Best Results
    
    - **Audio Quality**: Use a quiet environment with minimal background noise
    - **Video Quality**: Ensure good lighting and clear view of your body
    - **Duration**: 30 seconds to 5 minutes works best
    - **Format**: MP3, WAV, MP4, or WebM formats are supported
    """)
    
    # Quick stats or demo section
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Analysis Types", "3")
    with col2:
        st.metric("Supported Formats", "4+")
    with col3:
        st.metric("Processing Time", "< 30s")

if __name__ == "__main__":
    main()

