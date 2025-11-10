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

# Custom CSS for ultra-modern, aesthetic styling
st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Poppins:wght@400;500;600;700;800&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    /* Animated Background Gradient */
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .main {
        background: linear-gradient(-45deg, #f8fafc, #ffffff, #f1f5f9, #ffffff);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
    }
    
    /* Main Header with Animated Gradient */
    .main-header {
        font-size: 4.5rem;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        background-size: 200% 200%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
        letter-spacing: -0.03em;
        animation: gradient 3s ease infinite;
        text-shadow: 0 0 40px rgba(102, 126, 234, 0.3);
        position: relative;
    }
    
    .main-header::after {
        content: '';
        position: absolute;
        top: 0;
        left: 50%;
        transform: translateX(-50%);
        width: 200px;
        height: 200px;
        background: radial-gradient(circle, rgba(102, 126, 234, 0.1) 0%, transparent 70%);
        border-radius: 50%;
        filter: blur(60px);
        z-index: -1;
    }
    
    .sub-header {
        text-align: center;
        color: #64748b;
        margin-bottom: 3rem;
        font-size: 1.3rem;
        font-weight: 500;
        letter-spacing: 0.01em;
    }
    
    /* Sidebar Styling - Glassmorphism */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(30, 41, 59, 0.95) 0%, rgba(15, 23, 42, 0.98) 100%);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 4px 0 24px rgba(0, 0, 0, 0.1);
    }
    
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
        color: white;
    }
    
    [data-testid="stSidebar"] .stRadio label {
        color: rgba(255, 255, 255, 0.9);
        font-weight: 500;
        padding: 0.875rem 1rem;
        border-radius: 0.75rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        margin: 0.25rem 0;
        border: 1px solid transparent;
    }
    
    [data-testid="stSidebar"] .stRadio label:hover {
        background: rgba(255, 255, 255, 0.08);
        border-color: rgba(255, 255, 255, 0.1);
        transform: translateX(4px);
    }
    
    [data-testid="stSidebar"] .stRadio input:checked + label {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.9) 0%, rgba(118, 75, 162, 0.9) 100%);
        color: white;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
        border-color: rgba(102, 126, 234, 0.5);
    }
    
    /* Metric Cards - Glassmorphism */
    .metric-card {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        padding: 1.5rem;
        border-radius: 1.25rem;
        margin: 0.5rem 0;
        border: 1px solid rgba(255, 255, 255, 0.5);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .metric-card:hover {
        transform: translateY(-6px) scale(1.02);
        box-shadow: 0 16px 48px rgba(102, 126, 234, 0.2);
        border-color: rgba(102, 126, 234, 0.3);
        background: rgba(255, 255, 255, 0.9);
    }
    
    /* Feature Cards - Modern Glassmorphism */
    .feature-card {
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        padding: 2.5rem;
        border-radius: 1.5rem;
        border: 1px solid rgba(255, 255, 255, 0.6);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1), 
                    0 0 0 1px rgba(255, 255, 255, 0.5) inset;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        margin-bottom: 1.5rem;
        position: relative;
        overflow: hidden;
    }
    
    .feature-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.4), transparent);
        transition: left 0.5s;
    }
    
    .feature-card:hover::before {
        left: 100%;
    }
    
    .feature-card:hover {
        box-shadow: 0 20px 60px rgba(102, 126, 234, 0.15),
                    0 0 0 1px rgba(102, 126, 234, 0.2) inset;
        transform: translateY(-8px) scale(1.01);
        border-color: rgba(102, 126, 234, 0.4);
    }
    
    .feature-card h3 {
        color: #1e293b;
        margin-bottom: 1rem;
        font-weight: 700;
        font-size: 1.5rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* Buttons - Modern with Glow Effect */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 0.75rem;
        padding: 0.75rem 2.5rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 14px rgba(102, 126, 234, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.3);
        transform: translate(-50%, -50%);
        transition: width 0.6s, height 0.6s;
    }
    
    .stButton > button:hover::before {
        width: 300px;
        height: 300px;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.05);
        box-shadow: 0 8px 24px rgba(102, 126, 234, 0.5);
    }
    
    .stButton > button:active {
        transform: translateY(-1px) scale(1.02);
    }
    
    /* File Uploader - Modern Design */
    [data-testid="stFileUploader"] {
        border: 2px dashed rgba(102, 126, 234, 0.3);
        border-radius: 1.25rem;
        padding: 3rem 2rem;
        background: rgba(248, 250, 252, 0.6);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    [data-testid="stFileUploader"]::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(102, 126, 234, 0.1), transparent);
        transform: rotate(45deg);
        transition: all 0.6s;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: #667eea;
        background: rgba(241, 245, 249, 0.8);
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.15);
    }
    
    [data-testid="stFileUploader"]:hover::before {
        top: 50%;
        left: 50%;
    }
    
    /* Headers - Modern Typography */
    h1, h2, h3 {
        color: #1e293b;
        font-weight: 700;
        letter-spacing: -0.02em;
    }
    
    h2 {
        margin-top: 2.5rem;
        margin-bottom: 1.5rem;
        font-size: 2rem;
        background: linear-gradient(135deg, #1e293b 0%, #475569 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    h3 {
        font-size: 1.5rem;
        font-weight: 600;
    }
    
    /* Success/Info/Warning Messages - Modern Cards */
    .stSuccess {
        border-left: 4px solid #10b981;
        border-radius: 0.75rem;
        background: rgba(16, 185, 129, 0.05);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.1);
    }
    
    .stInfo {
        border-left: 4px solid #3b82f6;
        border-radius: 0.75rem;
        background: rgba(59, 130, 246, 0.05);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.1);
    }
    
    .stWarning {
        border-left: 4px solid #f59e0b;
        border-radius: 0.75rem;
        background: rgba(245, 158, 11, 0.05);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        box-shadow: 0 4px 12px rgba(245, 158, 11, 0.1);
    }
    
    /* Metrics - Enhanced */
    [data-testid="stMetricValue"] {
        font-size: 2.25rem;
        font-weight: 800;
        background: linear-gradient(135deg, #1e293b 0%, #475569 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    [data-testid="stMetricLabel"] {
        font-weight: 600;
        color: #64748b;
    }
    
    /* Expanders - Modern Design */
    [data-testid="stExpander"] {
        border: 1px solid rgba(226, 232, 240, 0.8);
        border-radius: 1rem;
        margin-bottom: 1.5rem;
        background: rgba(255, 255, 255, 0.5);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.05);
        transition: all 0.3s ease;
    }
    
    [data-testid="stExpander"]:hover {
        box-shadow: 0 8px 24px rgba(102, 126, 234, 0.1);
        border-color: rgba(102, 126, 234, 0.3);
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom scrollbar - Modern */
    ::-webkit-scrollbar {
        width: 12px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(241, 245, 249, 0.5);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #cbd5e1 0%, #94a3b8 100%);
        border-radius: 10px;
        border: 2px solid rgba(241, 245, 249, 0.5);
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #94a3b8 0%, #667eea 100%);
    }
    
    /* Main container padding */
    .main .block-container {
        padding-top: 4rem;
        padding-bottom: 4rem;
        max-width: 1400px;
    }
    
    /* Gradient text utility */
    .gradient-text {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* Animated gradient background for sections */
    @keyframes shimmer {
        0% { background-position: -1000px 0; }
        100% { background-position: 1000px 0; }
    }
    
    .animated-bg {
        background: linear-gradient(90deg, 
            rgba(102, 126, 234, 0.05) 0%, 
            rgba(118, 75, 162, 0.1) 50%, 
            rgba(102, 126, 234, 0.05) 100%);
        background-size: 2000px 100%;
        animation: shimmer 3s infinite;
    }
    
    /* Modern card hover effects */
    .modern-card {
        position: relative;
        overflow: hidden;
    }
    
    .modern-card::after {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, 
            transparent, 
            rgba(255, 255, 255, 0.4), 
            transparent);
        transition: left 0.5s;
    }
    
    .modern-card:hover::after {
        left: 100%;
    }
    
    /* Smooth page transitions */
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .main .block-container > div {
        animation: fadeIn 0.6s ease-out;
    }
    
    /* Modern input styling */
    input, textarea, select {
        border-radius: 0.75rem !important;
        border: 1px solid rgba(226, 232, 240, 0.8) !important;
        transition: all 0.3s ease !important;
    }
    
    input:focus, textarea:focus, select:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
    }
    </style>
""", unsafe_allow_html=True)

def main():
    """Main application function"""
    
    # Header
    st.markdown('<h1 class="main-header">🎤 MicDrop</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">AI-Powered Public Speaking Coach</p>', unsafe_allow_html=True)
    
    # Sidebar navigation with modern header
    st.sidebar.markdown("""
    <div style='text-align: center; padding: 1.5rem 0 2rem 0; border-bottom: 1px solid rgba(255, 255, 255, 0.1); margin-bottom: 1.5rem;'>
        <h2 style='color: white; font-size: 1.5rem; font-weight: 700; margin: 0; letter-spacing: -0.02em;'>
            🎤 MicDrop
        </h2>
        <p style='color: rgba(255, 255, 255, 0.7); font-size: 0.85rem; margin: 0.5rem 0 0 0;'>
            Navigation
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    page = st.sidebar.radio(
        "Choose Analysis Type",
        ["🏠 Home", "🎙️ Voice Analysis", "📝 Language Analysis", "👤 Body Language Analysis", "📊 Comprehensive Report"],
        label_visibility="collapsed"
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
    
    # Quick stats
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Analysis Types", "3", help="Voice, Language, and Body Language")
    with col2:
        st.metric("Supported Formats", "8+", help="MP3, WAV, MP4, WebM, and more")
    with col3:
        st.metric("Processing Time", "< 30s", help="Fast AI-powered analysis")
    with col4:
        st.metric("Free & Open", "100%", help="No API keys or subscriptions needed")
    
    st.markdown("---")
    
    # Introduction
    st.markdown("""
    <div style='text-align: center; padding: 2rem 0;'>
        <h2 style='color: #1e293b; margin-bottom: 1rem;'>Transform Your Public Speaking Skills</h2>
        <p style='font-size: 1.1rem; color: #64748b; max-width: 800px; margin: 0 auto;'>
            Get comprehensive, AI-powered feedback on your voice, language, and body language. 
            Practice, improve, and become a confident speaker.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Feature Cards
    st.markdown("### 🎯 Analysis Features")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class='feature-card'>
            <h3 style='color: #667eea; margin-bottom: 1rem;'>🎙️ Voice Analysis</h3>
            <ul style='color: #475569; line-height: 1.8;'>
                <li><strong>Pace:</strong> Words per minute, speaking rate</li>
                <li><strong>Pitch:</strong> Average pitch and variation</li>
                <li><strong>Pauses:</strong> Frequency and duration</li>
                <li><strong>Volume:</strong> Consistency and variation</li>
                <li><strong>Clarity:</strong> Articulation quality</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='feature-card'>
            <h3 style='color: #667eea; margin-bottom: 1rem;'>📝 Language Analysis</h3>
            <ul style='color: #475569; line-height: 1.8;'>
                <li><strong>Clarity:</strong> Sentence structure and complexity</li>
                <li><strong>Word Choice:</strong> Vocabulary diversity</li>
                <li><strong>Filler Words:</strong> Detection and frequency</li>
                <li><strong>Structure:</strong> Organization and coherence</li>
                <li><strong>Tone:</strong> Formality and engagement</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class='feature-card'>
            <h3 style='color: #667eea; margin-bottom: 1rem;'>👤 Body Language Analysis</h3>
            <ul style='color: #475569; line-height: 1.8;'>
                <li><strong>Posture:</strong> Body alignment and stance</li>
                <li><strong>Gestures:</strong> Hand movements and frequency</li>
                <li><strong>Eye Contact:</strong> Gaze direction</li>
                <li><strong>Facial Expressions:</strong> Engagement indicators</li>
                <li><strong>Presence:</strong> Overall stage presence</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Getting Started Section
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        ### 🚀 Getting Started
        
        1. **Choose an analysis type** from the sidebar
        2. **Upload or record** your audio/video
        3. **Wait for processing** (usually < 30 seconds)
        4. **Review your feedback** and recommendations
        5. **Practice and improve!**
        """)
    
    with col2:
        st.markdown("""
        ### 💡 Tips for Best Results
        
        - **Audio Quality**: Use a quiet environment with minimal background noise
        - **Video Quality**: Ensure good lighting and clear view of your body
        - **Duration**: 30 seconds to 5 minutes works best
        - **Format**: MP3, WAV, MP4, or WebM formats are supported
        """)
    
    st.markdown("---")
    
    # Call to Action - Modern Glassmorphism Card
    st.markdown("""
    <div class='feature-card modern-card' style='text-align: center; margin-top: 3rem; background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%); border: 1px solid rgba(102, 126, 234, 0.2);'>
        <h3 style='color: #1e293b; margin-bottom: 1rem; font-size: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;'>Ready to Transform Your Speaking Skills? 🚀</h3>
        <p style='color: #64748b; margin-bottom: 1.5rem; font-size: 1.1rem;'>Select an analysis type from the sidebar to get started with AI-powered feedback!</p>
        <div style='display: inline-block; padding: 0.5rem 1.5rem; background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%); border-radius: 0.75rem; border: 1px solid rgba(102, 126, 234, 0.3);'>
            <span style='color: #667eea; font-weight: 600;'>✨ Free • Fast • AI-Powered ✨</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

