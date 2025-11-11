"""
MicDrop - AI Public Speaking Coach
Main Streamlit application entry point
"""

import streamlit as st
import os
import base64
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="MicDrop - AI Public Speaking Coach",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Function to get background image as base64
@st.cache_data
def get_background_image_base64():
    """Load background image and convert to base64 for CSS"""
    # Try multiple path resolutions for Streamlit
    possible_paths = [
        Path(__file__).parent / "assets",
        Path.cwd() / "assets",
        Path("assets"),
    ]
    
    # Try different image formats
    for ext in ['.jpg', '.jpeg', '.png', '.webp']:
        for filename in ['background', 'bg', 'background-image']:
            for assets_dir in possible_paths:
                img_path = assets_dir / f"{filename}{ext}"
                if img_path.exists():
                    try:
                        with open(img_path, "rb") as img_file:
                            encoded = base64.b64encode(img_file.read()).decode()
                            return f"data:image/{ext[1:]};base64,{encoded}"
                    except Exception as e:
                        # Silently continue to next path
                        continue
    return None

# Get background image
background_image = get_background_image_base64()

# Store in session state for debugging
if 'bg_image_loaded' not in st.session_state:
    st.session_state.bg_image_loaded = background_image is not None

# Debug: Check if image was found
if background_image:
    # Image found - use it
    background_css = f"""
        background-image: url('{background_image}');
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
"""
else:
    # Fallback gradient
    background_css = """
        background: linear-gradient(-45deg, #f3f4f6, #ede9fe, #faf5ff, #f3e8ff, #e9d5ff);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
"""

st.markdown(f"""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Poppins:wght@400;500;600;700;800&display=swap');
    
    /* Import Material Icons */
    @import url('https://fonts.googleapis.com/icon?family=Material+Icons');
    
    /* Global Styles */
    * {{
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }}
    
    /* Modern Icon Styles */
    .icon {{
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 1.2em;
        height: 1.2em;
        vertical-align: middle;
        margin-right: 0.3em;
    }}
    
    .icon svg {{
        width: 100%;
        height: 100%;
        fill: currentColor;
    }}
    
    .icon-large {{
        width: 1.5em;
        height: 1.5em;
    }}
    
    .icon-xl {{
        width: 2em;
        height: 2em;
    }}
    
    /* Animated Background Gradient */
    @keyframes gradient {{
        0% {{ background-position: 0% 50%; }}
        50% {{ background-position: 100% 50%; }}
        100% {{ background-position: 0% 50%; }}
    }}
    
    /* Apply background to body and html */
    body, html {{
{background_css}
        margin: 0;
        padding: 0;
        min-height: 100vh;
        width: 100%;
    }}
    
    /* Apply background to Streamlit app container */
    .stApp {{
{background_css}
        position: relative;
        min-height: 100vh;
        width: 100%;
    }}
    
    /* Ensure root is transparent */
    #root {{
        background: transparent !important;
    }}
    
    /* App view container - make transparent */
    [data-testid="stAppViewContainer"] {{
        background: transparent !important;
    }}
    
    /* Main content area */
    .main {{
        background: transparent !important;
        position: relative;
    }}
    
    /* Add subtle overlay for better text readability (only if image exists) */
    .stApp::before {{
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(15, 12, 41, 0.1);
        pointer-events: none;
        z-index: 0;
    }}
    
    .main .block-container {{
        position: relative;
        z-index: 1;
        background: transparent !important;
    }}
    
    /* Make all containers transparent to show background */
    .block-container, .element-container, [data-testid="column"], [data-testid="stColumn"] {{
        background: transparent !important;
    }}
    
    /* Main Header with Dark Purple Animated Gradient */
    .main-header {{
        font-size: 4.5rem;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(135deg, #2a0040 0%, #4a0064 50%, #6a0088 100%);
        background-size: 200% 200%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
        letter-spacing: -0.03em;
        animation: gradient 5s ease infinite;
        text-shadow: 0 0 40px rgba(42, 0, 64, 0.6);
        position: relative;
    }}
    
    .main-header::after {{
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 200px;
        height: 200px;
        background: radial-gradient(circle, rgba(255, 140, 0, 0.8) 0%, rgba(255, 200, 0, 0.6) 30%, rgba(255, 140, 0, 0.3) 60%, transparent 100%);
        border-radius: 50%;
        filter: blur(40px);
        z-index: -1;
        opacity: 0;
        animation: gradientGlow 2s ease-out forwards;
        animation-delay: 1s;
    }}
    
    @keyframes gradientGlow {{
        0% {{
            width: 200px;
            height: 200px;
            opacity: 0;
            transform: translate(-50%, -50%) scale(0.5);
        }}
        50% {{
            opacity: 1;
        }}
        100% {{
            width: 600px;
            height: 600px;
            opacity: 0.8;
            transform: translate(-50%, -50%) scale(1);
        }}
    }}
    
    .sub-header {{
        text-align: center;
        color: #2a0040;
        margin-bottom: 3rem;
        font-size: 1.3rem;
        font-weight: 500;
        letter-spacing: 0.01em;
    }}
    
    /* Sidebar Styling - Dark Purple Glassmorphism */
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, rgba(42, 0, 64, 0.95) 0%, rgba(42, 0, 64, 0.98) 100%);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 4px 0 24px rgba(42, 0, 64, 0.5);
        z-index: 9999 !important;
    }}
    
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {{
        color: white;
    }}
    
    [data-testid="stSidebar"] .stRadio label {{
        color: rgba(255, 255, 255, 0.9);
        font-weight: 500;
        padding: 0.875rem 1rem;
        border-radius: 0.75rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        margin: 0.25rem 0;
        border: 1px solid transparent;
    }}
    
    [data-testid="stSidebar"] .stRadio label:hover {{
        background: rgba(255, 255, 255, 0.08);
        border-color: rgba(255, 255, 255, 0.1);
        transform: translateX(4px);
    }}
    
    [data-testid="stSidebar"] .stRadio input:checked + label {{
        background: linear-gradient(135deg, rgba(74, 0, 100, 0.9) 0%, rgba(106, 0, 136, 0.9) 100%);
        color: white;
        box-shadow: 0 4px 12px rgba(42, 0, 64, 0.7);
        border-color: rgba(74, 0, 100, 0.8);
    }}
    
    /* Metric Cards - Dark Purple Glassmorphism */
    .metric-card {{
        background: rgba(42, 0, 64, 0.7);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        padding: 1.5rem;
        border-radius: 1.25rem;
        margin: 0.5rem 0;
        border: 1px solid rgba(74, 0, 100, 0.5);
        box-shadow: 0 8px 32px rgba(42, 0, 64, 0.3);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }}
    
    .metric-card:hover {{
        transform: translateY(-6px) scale(1.02);
        box-shadow: 0 16px 48px rgba(42, 0, 64, 0.5);
        border-color: rgba(74, 0, 100, 0.7);
        background: rgba(42, 0, 64, 0.85);
    }}
    
    /* Feature Cards - Dark Purple Glassmorphism */
    .feature-card {{
        background: rgba(42, 0, 64, 0.8);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        padding: 2.5rem;
        border-radius: 1.5rem;
        border: 1px solid rgba(74, 0, 100, 0.6);
        box-shadow: 0 8px 32px rgba(42, 0, 64, 0.4), 
                    0 0 0 1px rgba(74, 0, 100, 0.4) inset;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        margin-bottom: 1.5rem;
        position: relative;
        overflow: hidden;
    }}
    
    .feature-card::before {{
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(74, 0, 100, 0.4), transparent);
        transition: left 0.5s;
    }}
    
    .feature-card:hover::before {{
        left: 100%;
    }}
    
    .feature-card:hover {{
        box-shadow: 0 20px 60px rgba(42, 0, 64, 0.6),
                    0 0 0 1px rgba(74, 0, 100, 0.6) inset;
        transform: translateY(-8px) scale(1.01);
        border-color: rgba(74, 0, 100, 0.8);
        background: rgba(42, 0, 64, 0.9);
    }}
    
    .feature-card h3 {{
        color: #ffffff;
        margin-bottom: 1rem;
        font-weight: 700;
        font-size: 1.5rem;
        background: linear-gradient(135deg, #ffffff 0%, #e0d0ff 50%, #c0a0ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }}
    
    /* Buttons - Dark Purple with Glow Effect */
    .stButton > button {{
        background: linear-gradient(135deg, #2a0040 0%, #4a0064 50%, #6a0088 100%);
        color: white;
        border: none;
        border-radius: 0.75rem;
        padding: 0.75rem 2.5rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 14px rgba(42, 0, 64, 0.6);
        position: relative;
        overflow: hidden;
    }}
    
    .stButton > button::before {{
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
    }}
    
    .stButton > button:hover::before {{
        width: 300px;
        height: 300px;
    }}
    
    .stButton > button:hover {{
        transform: translateY(-3px) scale(1.05);
        box-shadow: 0 8px 24px rgba(42, 0, 64, 0.8);
    }}
    
    .stButton > button:active {{
        transform: translateY(-1px) scale(1.02);
    }}
    
    /* File Uploader - Dark Purple Design */
    [data-testid="stFileUploader"] {{
        border: 2px dashed rgba(74, 0, 100, 0.6);
        border-radius: 1.25rem;
        padding: 3rem 2rem;
        background: rgba(42, 0, 64, 0.6);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }}
    
    [data-testid="stFileUploader"]::before {{
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(74, 0, 100, 0.3), transparent);
        transform: rotate(45deg);
        transition: all 0.6s;
    }}
    
    [data-testid="stFileUploader"]:hover {{
        border-color: #4a0064;
        background: rgba(42, 0, 64, 0.8);
        box-shadow: 0 8px 32px rgba(42, 0, 64, 0.4);
    }}
    
    [data-testid="stFileUploader"]:hover::before {{
        top: 50%;
        left: 50%;
    }}
    
    /* Headers - Modern Typography */
    h1, h2, h3 {{
        color: #ffffff;
        font-weight: 700;
        letter-spacing: -0.02em;
    }}
    
    h2 {{
        margin-top: 2.5rem;
        margin-bottom: 1.5rem;
        font-size: 2rem;
        background: linear-gradient(135deg, #2a0040 0%, #4a0064 50%, #6a0088 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }}
    
    h3 {{
        font-size: 1.5rem;
        font-weight: 600;
    }}
    
    /* Success/Info/Warning Messages - Modern Cards */
    .stSuccess {{
        border-left: 4px solid #10b981;
        border-radius: 0.75rem;
        background: rgba(16, 185, 129, 0.05);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.1);
    }}
    
    .stInfo {{
        border-left: 4px solid #4a0064;
        border-radius: 0.75rem;
        background: rgba(42, 0, 64, 0.2);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        box-shadow: 0 4px 12px rgba(42, 0, 64, 0.3);
    }}
    
    .stWarning {{
        border-left: 4px solid #f59e0b;
        border-radius: 0.75rem;
        background: rgba(245, 158, 11, 0.05);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        box-shadow: 0 4px 12px rgba(245, 158, 11, 0.1);
    }}
    
    /* Metrics - Dark Purple Theme */
    [data-testid="stMetricValue"] {{
        font-size: 2.25rem;
        font-weight: 800;
        background: linear-gradient(135deg, #2a0040 0%, #4a0064 50%, #6a0088 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }}
    
    [data-testid="stMetricLabel"] {{
        font-weight: 600;
        color: #2a0040;
    }}
    
    /* Expanders - Dark Purple Design */
    [data-testid="stExpander"] {{
        border: 1px solid rgba(74, 0, 100, 0.5);
        border-radius: 1rem;
        margin-bottom: 1.5rem;
        background: rgba(42, 0, 64, 0.6);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        box-shadow: 0 4px 16px rgba(42, 0, 64, 0.3);
        transition: all 0.3s ease;
    }}
    
    [data-testid="stExpander"]:hover {{
        box-shadow: 0 8px 24px rgba(42, 0, 64, 0.4);
        border-color: rgba(74, 0, 100, 0.7);
        background: rgba(42, 0, 64, 0.75);
    }}
    
    /* Hide Streamlit branding */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    
    /* Custom scrollbar - Dark Purple */
    ::-webkit-scrollbar {{
        width: 12px;
    }}
    
    ::-webkit-scrollbar-track {{
        background: rgba(42, 0, 64, 0.3);
        border-radius: 10px;
    }}
    
    ::-webkit-scrollbar-thumb {{
        background: linear-gradient(135deg, #6a0088 0%, #4a0064 100%);
        border-radius: 10px;
        border: 2px solid rgba(42, 0, 64, 0.3);
    }}
    
    ::-webkit-scrollbar-thumb:hover {{
        background: linear-gradient(135deg, #4a0064 0%, #2a0040 100%);
    }}
    
    /* Main container padding */
    .main .block-container {{
        padding-top: 4rem;
        padding-bottom: 4rem;
        max-width: 1400px;
    }}
    
    /* Gradient text utility */
    .gradient-text {{
        background: linear-gradient(135deg, #2a0040 0%, #4a0064 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }}
    
    /* Animated gradient background for sections */
    @keyframes shimmer {{
        0% {{ background-position: -1000px 0; }}
        100% {{ background-position: 1000px 0; }}
    }}
    
    .animated-bg {{
        background: linear-gradient(90deg, 
            rgba(42, 0, 64, 0.2) 0%, 
            rgba(74, 0, 100, 0.3) 50%, 
            rgba(42, 0, 64, 0.2) 100%);
        background-size: 2000px 100%;
        animation: shimmer 3s infinite;
    }}
    
    /* Modern card hover effects */
    .modern-card {{
        position: relative;
        overflow: hidden;
    }}
    
    .modern-card::after {{
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
    }}
    
    .modern-card:hover::after {{
        left: 100%;
    }}
    
    /* Smooth page transitions */
    @keyframes fadeIn {{
        from {{
            opacity: 0;
            transform: translateY(20px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}
    
    .main .block-container > div {{
        animation: fadeIn 0.6s ease-out;
    }}
    
    /* Modern input styling */
    input, textarea, select {{
        border-radius: 0.75rem !important;
        border: 1px solid rgba(226, 232, 240, 0.8) !important;
        transition: all 0.3s ease !important;
    }}
    
    input:focus, textarea:focus, select:focus {{
        border-color: #4a0064 !important;
        box-shadow: 0 0 0 3px rgba(42, 0, 64, 0.3) !important;
    }}
    
    /* Curtain Animation Styles */
    .curtain-container {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100vh;
        z-index: 9998;
        pointer-events: none;
        overflow: hidden;
    }}
    
    /* Position curtains to account for sidebar */
    .curtain-left, .curtain-right {{
        position: absolute;
        top: 0;
        height: 100%;
        background: linear-gradient(90deg, 
            #1a0026 0%, 
            #2a0040 8%, 
            #1a0026 16%, 
            #2a0040 24%,
            #1a0026 32%,
            #2a0040 40%,
            #1a0026 48%,
            #2a0040 56%,
            #1a0026 64%,
            #2a0040 72%,
            #1a0026 80%,
            #2a0040 88%,
            #1a0026 96%,
            #2a0040 100%);
        background-size: 100% 100%;
        box-shadow: inset 0 0 50px rgba(0, 0, 0, 0.8),
                    0 0 30px rgba(0, 0, 0, 0.5);
        display: flex;
        align-items: center;
        justify-content: center;
        overflow: hidden;
    }}
    
    /* Curtain positioning - Initial CSS positioning, JavaScript will refine */
    .curtain-left {{
        left: calc(21rem - 150px);  /* Start well before sidebar edge to cover gap */
        width: calc((100vw - 21rem) * 0.47 + 150px);  /* 47% of main content + extra to cover gap */
        border-right: 3px solid rgba(0, 0, 0, 0.5);
    }}
    
    .curtain-right {{
        left: calc(21rem + (100vw - 21rem) * 0.47);  /* Start from 47% point (slightly right) */
        width: calc((100vw - 21rem) * 0.53);  /* 53% of main content */
        border-left: 3px solid rgba(0, 0, 0, 0.5);
    }}
    
    /* Curtain creases/folds - vertical pleats */
    .curtain-left::before, .curtain-right::before {{
        content: '';
        position: absolute;
        top: 0;
        width: 100%;
        height: 100%;
        background: repeating-linear-gradient(
            90deg,
            rgba(0, 0, 0, 0.3) 0px,
            rgba(0, 0, 0, 0.3) 2px,
            transparent 2px,
            transparent 30px,
            rgba(0, 0, 0, 0.2) 30px,
            rgba(0, 0, 0, 0.2) 32px,
            transparent 32px,
            transparent 60px
        );
        box-shadow: 
            inset -15px 0 20px -10px rgba(0, 0, 0, 0.6),
            inset 15px 0 20px -10px rgba(0, 0, 0, 0.6),
            inset -30px 0 25px -15px rgba(0, 0, 0, 0.4),
            inset 30px 0 25px -15px rgba(0, 0, 0, 0.4),
            inset -45px 0 30px -20px rgba(0, 0, 0, 0.3),
            inset 45px 0 30px -20px rgba(0, 0, 0, 0.3);
    }}
    
    /* Additional crease layers for depth */
    .curtain-left::after, .curtain-right::after {{
        content: '';
        position: absolute;
        top: 0;
        width: 100%;
        height: 100%;
        background: repeating-linear-gradient(
            90deg,
            transparent 0px,
            transparent 28px,
            rgba(0, 0, 0, 0.15) 28px,
            rgba(0, 0, 0, 0.15) 30px,
            transparent 30px,
            transparent 58px,
            rgba(0, 0, 0, 0.1) 58px,
            rgba(0, 0, 0, 0.1) 60px,
            transparent 60px
        );
    }}
    
    /* Curtain tassels/fringe at bottom - using separate element */
    .curtain-fringe {{
        position: absolute;
        bottom: 0;
        width: 100%;
        height: 30px;
        background: repeating-linear-gradient(
            90deg,
            #1a0026 0px,
            #2a0040 2px,
            #1a0026 4px,
            #2a0040 6px,
            #1a0026 8px
        );
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.5);
        z-index: 2;
    }}
    
    .curtain-left .curtain-fringe {{
        left: 0;
    }}
    
    .curtain-right .curtain-fringe {{
        right: 0;
    }}
    
    /* Stage/platform at bottom */
    .stage-platform {{
        position: absolute;
        bottom: 0;
        left: 0;
        width: 100%;
        height: 80px;
        background: linear-gradient(to top, 
            rgba(0, 0, 0, 0.8) 0%,
            rgba(20, 0, 30, 0.6) 50%,
            rgba(42, 0, 64, 0.4) 100%);
        z-index: 1;
        box-shadow: 0 -10px 30px rgba(0, 0, 0, 0.5);
    }}
    
    /* Curtain opening animation */
    @keyframes openCurtains {{
        0% {{
            transform: translateX(0);
        }}
        100% {{
            transform: translateX(-110%);  /* Slightly more than 100% to ensure hiding, closer to right speed */
        }}
    }}
    
    @keyframes openCurtainsRight {{
        0% {{
            transform: translateX(0);
        }}
        100% {{
            transform: translateX(100%);
        }}
    }}
    
    .curtain-left.open {{
        animation: openCurtains 3.5s ease-in-out forwards;
        animation-delay: 0.5s;
    }}
    
    .curtain-right.open {{
        animation: openCurtainsRight 3.5s ease-in-out forwards;
        animation-delay: 0.5s;
    }}
    
    /* Hide curtains after animation */
    .curtain-container.hidden {{
        display: none;
    }}
    
    /* Content fade-in after curtains open */
    @keyframes fadeInContent {{
        from {{
            opacity: 0;
            transform: translateY(20px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}
    
    .main-content {{
        animation: fadeInContent 1.5s ease-out forwards;
        animation-delay: 1s;
        opacity: 0;
    }}
    
    .main-content.visible {{
        opacity: 1;
    }}
    </style>
""", unsafe_allow_html=True)

def main():
    """Main application function"""
    
    # Debug: Show if background image was loaded (only on first run)
    if 'bg_debug_shown' not in st.session_state:
        if background_image:
            st.sidebar.success("✅ Background image loaded!")
        else:
            st.sidebar.info("ℹ️ Using gradient background (image not found)")
        st.session_state.bg_debug_shown = True
    
    # Curtain animation - only show on first load
    if 'curtains_shown' not in st.session_state:
        st.markdown("""
        <div class="curtain-container" id="curtainContainer">
            <div class="curtain-left open">
                <div class="curtain-fringe"></div>
            </div>
            <div class="curtain-right open">
                <div class="curtain-fringe"></div>
            </div>
            <div class="stage-platform"></div>
        </div>
        <script>
            (function() {{
                // Function to position curtains based on sidebar width
                function positionCurtains() {{
                    var sidebar = document.querySelector('[data-testid="stSidebar"]');
                    var curtainLeft = document.querySelector('.curtain-left');
                    var curtainRight = document.querySelector('.curtain-right');
                    
                    if (!curtainLeft || !curtainRight) {{
                        // Retry if elements not found yet
                        setTimeout(positionCurtains, 50);
                        return;
                    }}
                    
                    // Get sidebar width (default to 21rem if not found)
                    var sidebarWidth = 21 * 16; // 21rem in pixels (assuming 16px base)
                    if (sidebar) {{
                        var sidebarRect = sidebar.getBoundingClientRect();
                        sidebarWidth = sidebarRect.width || sidebarWidth;
                    }}
                    
                    // Calculate main content area width
                    var viewportWidth = window.innerWidth;
                    var mainContentWidth = viewportWidth - sidebarWidth;
                    var leftCurtainBaseWidth = mainContentWidth * 0.47;  // 47% - center slightly to the right
                    var extraWidthLeft = 150;  // Extra to extend left and cover gap
                    var leftCurtainWidth = leftCurtainBaseWidth + extraWidthLeft;
                    var rightCurtainWidth = mainContentWidth * 0.53;  // 53% - slightly narrower
                    
                    // Ensure we have valid dimensions
                    if (mainContentWidth > 0 && leftCurtainWidth > 0 && rightCurtainWidth > 0) {{
                        // Position left curtain: starts well before sidebar edge to cover gap,
                        // covers 47% of main content + extra (center slightly to the right)
                        curtainLeft.style.left = (sidebarWidth - extraWidthLeft) + 'px';
                        curtainLeft.style.width = leftCurtainWidth + 'px';
                        
                        // Position right curtain: starts from 47% point (center slightly to the right),
                        // covers 53% of main content area
                        curtainRight.style.left = (sidebarWidth + leftCurtainBaseWidth) + 'px';
                        curtainRight.style.width = rightCurtainWidth + 'px';
                    }}
                }}
                
                // Wait for DOM to be ready, then position curtains
                if (document.readyState === 'loading') {{
                    document.addEventListener('DOMContentLoaded', function() {{
                        positionCurtains();
                        // Also position after a short delay to ensure everything is rendered
                        setTimeout(positionCurtains, 100);
                    }});
                }} else {{
                    // DOM already ready
                    positionCurtains();
                    setTimeout(positionCurtains, 100);
                }}
                
                // Position on resize
                window.addEventListener('resize', positionCurtains);
                
                // Hide curtains after animation completes (3.5s animation + 0.5s delay + 0.5s buffer)
                setTimeout(function() {{
                    var container = document.getElementById('curtainContainer');
                    if (container) {{
                        container.style.display = 'none';
                    }}
                }}, 4500);
                
                // Show content as curtains start opening (0.5s delay + 0.5s into animation)
                setTimeout(function() {{
                    var contentElements = document.querySelectorAll('.main-content');
                    contentElements.forEach(function(el) {{
                        el.style.opacity = '1';
                        el.style.transform = 'translateY(0)';
                    }});
                }}, 1000);
            }})();
        </script>
        """, unsafe_allow_html=True)
        st.session_state.curtains_shown = True
    
    # Header with curtain reveal effect
    st.markdown('''
    <div class="main-content">
        <h1 class="main-header">
            <svg class="icon icon-xl" style="display: inline-block; vertical-align: middle; margin-right: 0.5rem;" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3z" fill="currentColor"/>
                <path d="M17 11c0 2.76-2.24 5-5 5s-5-2.24-5-5H5c0 3.53 2.61 6.43 6 6.92V21h2v-3.08c3.39-.49 6-3.39 6-6.92h-2z" fill="currentColor"/>
            </svg>
            MicDrop
        </h1>
    </div>
    ''', unsafe_allow_html=True)
    st.markdown('<div class="main-content"><p class="sub-header">AI-Powered Public Speaking Coach</p></div>', unsafe_allow_html=True)
    
    # Sidebar navigation with modern header
    st.sidebar.markdown("""
    <div style='text-align: center; padding: 1.5rem 0 2rem 0; border-bottom: 1px solid rgba(255, 255, 255, 0.1); margin-bottom: 1.5rem;'>
        <h2 style='color: white; font-size: 1.5rem; font-weight: 700; margin: 0; letter-spacing: -0.02em; display: flex; align-items: center; justify-content: center; gap: 0.5rem;'>
            <svg style="width: 1.5rem; height: 1.5rem; fill: currentColor;" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3z" fill="currentColor"/>
                <path d="M17 11c0 2.76-2.24 5-5 5s-5-2.24-5-5H5c0 3.53 2.61 6.43 6 6.92V21h2v-3.08c3.39-.49 6-3.39 6-6.92h-2z" fill="currentColor"/>
            </svg>
            MicDrop
        </h2>
        <p style='color: rgba(255, 255, 255, 0.7); font-size: 0.85rem; margin: 0.5rem 0 0 0;'>
            Navigation
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize page state
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Home"
    
    # Navigation with SVG icons using CSS data URIs
    st.sidebar.markdown("""
    <style>
    /* Base button styles */
    [data-testid="stSidebar"] .stButton > button {
        width: 100%;
        text-align: left;
        padding: 0.75rem 1rem 0.75rem 3rem !important;
        background: transparent !important;
        border: 1px solid transparent !important;
        color: rgba(255, 255, 255, 0.9) !important;
        border-radius: 0.5rem !important;
        transition: all 0.3s ease !important;
        margin-bottom: 0.5rem !important;
        box-shadow: none !important;
        font-weight: 500 !important;
        position: relative !important;
    }
    [data-testid="stSidebar"] .stButton > button:hover {
        background: rgba(255, 255, 255, 0.1) !important;
        border-color: rgba(255, 255, 255, 0.2) !important;
        transform: translateX(4px) !important;
    }
    [data-testid="stSidebar"] .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, rgba(74, 0, 100, 0.9) 0%, rgba(106, 0, 136, 0.9) 100%) !important;
        border-color: rgba(74, 0, 100, 0.8) !important;
        color: white !important;
        box-shadow: 0 4px 12px rgba(42, 0, 64, 0.7) !important;
    }
    
    /* Add icons using ::before pseudo-elements with SVG data URIs */
    [data-testid="stSidebar"] .stButton > button::before {
        content: '';
        position: absolute;
        left: 1rem;
        top: 50%;
        transform: translateY(-50%);
        width: 1.2rem;
        height: 1.2rem;
        background-size: contain;
        background-repeat: no-repeat;
        background-position: center;
        opacity: 0.9;
    }
    
    /* Home icon */
    [data-testid="stSidebar"] button[data-testid*="nav_Home"]::before {
        background-image: url('data:image/svg+xml;utf8,<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z" fill="rgba(255,255,255,0.9)"/></svg>');
    }
    
    /* Voice Analysis icon */
    [data-testid="stSidebar"] button[data-testid*="nav_Voice"]::before {
        background-image: url('data:image/svg+xml;utf8,<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3z" fill="rgba(255,255,255,0.9)"/><path d="M17 11c0 2.76-2.24 5-5 5s-5-2.24-5-5H5c0 3.53 2.61 6.43 6 6.92V21h2v-3.08c3.39-.49 6-3.39 6-6.92h-2z" fill="rgba(255,255,255,0.9)"/></svg>');
    }
    
    /* Language Analysis icon */
    [data-testid="stSidebar"] button[data-testid*="nav_Language"]::before {
        background-image: url('data:image/svg+xml;utf8,<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25zM20.71 7.04c.39-.39.39-1.02 0-1.41l-2.34-2.34c-.39-.39-1.02-.39-1.41 0l-1.83 1.83 3.75 3.75 1.83-1.83z" fill="rgba(255,255,255,0.9)"/></svg>');
    }
    
    /* Body Language Analysis icon */
    [data-testid="stSidebar"] button[data-testid*="nav_Body"]::before {
        background-image: url('data:image/svg+xml;utf8,<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z" fill="rgba(255,255,255,0.9)"/></svg>');
    }
    
    /* Comprehensive Report icon */
    [data-testid="stSidebar"] button[data-testid*="nav_Comprehensive"]::before {
        background-image: url('data:image/svg+xml;utf8,<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zM9 17H7v-7h2v7zm4 0h-2V7h2v10zm4 0h-2v-4h2v4z" fill="rgba(255,255,255,0.9)"/></svg>');
    }
    
    /* Make icons white on active buttons */
    [data-testid="stSidebar"] button[kind="primary"]::before {
        opacity: 1;
    }
    [data-testid="stSidebar"] button[kind="primary"][data-testid*="nav_Home"]::before {
        background-image: url('data:image/svg+xml;utf8,<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z" fill="white"/></svg>');
    }
    [data-testid="stSidebar"] button[kind="primary"][data-testid*="nav_Voice"]::before {
        background-image: url('data:image/svg+xml;utf8,<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3z" fill="white"/><path d="M17 11c0 2.76-2.24 5-5 5s-5-2.24-5-5H5c0 3.53 2.61 6.43 6 6.92V21h2v-3.08c3.39-.49 6-3.39 6-6.92h-2z" fill="white"/></svg>');
    }
    [data-testid="stSidebar"] button[kind="primary"][data-testid*="nav_Language"]::before {
        background-image: url('data:image/svg+xml;utf8,<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25zM20.71 7.04c.39-.39.39-1.02 0-1.41l-2.34-2.34c-.39-.39-1.02-.39-1.41 0l-1.83 1.83 3.75 3.75 1.83-1.83z" fill="white"/></svg>');
    }
    [data-testid="stSidebar"] button[kind="primary"][data-testid*="nav_Body"]::before {
        background-image: url('data:image/svg+xml;utf8,<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z" fill="white"/></svg>');
    }
    [data-testid="stSidebar"] button[kind="primary"][data-testid*="nav_Comprehensive"]::before {
        background-image: url('data:image/svg+xml;utf8,<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zM9 17H7v-7h2v7zm4 0h-2V7h2v10zm4 0h-2v-4h2v4z" fill="white"/></svg>');
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Define navigation items (button keys must match CSS selectors)
    nav_items = {
        "Home": "Home",
        "Voice Analysis": "Voice Analysis",
        "Language Analysis": "Language Analysis",
        "Body Language Analysis": "Body Language Analysis",
        "Comprehensive Report": "Comprehensive Report"
    }
    
    # Create navigation buttons
    for page_name, label in nav_items.items():
        is_active = st.session_state.current_page == page_name
        
        # Create button - CSS will add the icon
        if st.sidebar.button(label, key=f"nav_{page_name}", use_container_width=True, type="primary" if is_active else "secondary"):
            st.session_state.current_page = page_name
            st.rerun()
    
    # Use the current page from session state
    page = st.session_state.current_page
    
    # Route to appropriate page
    if page == "Home":
        show_home()
    elif page == "Voice Analysis":
        from page_modules import voice_analysis
        voice_analysis.show()
    elif page == "Language Analysis":
        from page_modules import language_analysis
        language_analysis.show()
    elif page == "Body Language Analysis":
        from page_modules import body_language_analysis
        body_language_analysis.show()
    elif page == "Comprehensive Report":
        from page_modules import comprehensive_report
        comprehensive_report.show()

def show_home():
    """Display home page with instructions"""
    
    # Wrap content in main-content div for fade-in effect
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    
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
        <h2 style='color: #ffffff; margin-bottom: 1rem;'>Transform Your Public Speaking Skills</h2>
        <p style='font-size: 1.1rem; color: rgba(255, 255, 255, 0.9); max-width: 800px; margin: 0 auto;'>
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
            <h3 style='color: #ffffff; margin-bottom: 1rem; background: linear-gradient(135deg, #ffffff 0%, #e0d0ff 50%, #c0a0ff 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; display: flex; align-items: center; gap: 0.5rem;'>
                <svg style="width: 1.5rem; height: 1.5rem; fill: currentColor;" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3z" fill="currentColor"/>
                    <path d="M17 11c0 2.76-2.24 5-5 5s-5-2.24-5-5H5c0 3.53 2.61 6.43 6 6.92V21h2v-3.08c3.39-.49 6-3.39 6-6.92h-2z" fill="currentColor"/>
                </svg>
                Voice Analysis
            </h3>
            <ul style='color: rgba(255, 255, 255, 0.9); line-height: 1.8;'>
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
            <h3 style='color: #ffffff; margin-bottom: 1rem; background: linear-gradient(135deg, #ffffff 0%, #e0d0ff 50%, #c0a0ff 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; display: flex; align-items: center; gap: 0.5rem;'>
                <svg style="width: 1.5rem; height: 1.5rem; fill: currentColor;" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25zM20.71 7.04c.39-.39.39-1.02 0-1.41l-2.34-2.34c-.39-.39-1.02-.39-1.41 0l-1.83 1.83 3.75 3.75 1.83-1.83z" fill="currentColor"/>
                </svg>
                Language Analysis
            </h3>
            <ul style='color: rgba(255, 255, 255, 0.9); line-height: 1.8;'>
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
            <h3 style='color: #ffffff; margin-bottom: 1rem; background: linear-gradient(135deg, #ffffff 0%, #e0d0ff 50%, #c0a0ff 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; display: flex; align-items: center; gap: 0.5rem;'>
                <svg style="width: 1.5rem; height: 1.5rem; fill: currentColor;" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z" fill="currentColor"/>
                </svg>
                Body Language Analysis
            </h3>
            <ul style='color: rgba(255, 255, 255, 0.9); line-height: 1.8;'>
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
    
    # Call to Action - Dark Purple Glassmorphism Card
    st.markdown("""
    <div class='feature-card modern-card' style='text-align: center; margin-top: 3rem; background: linear-gradient(135deg, rgba(42, 0, 64, 0.3) 0%, rgba(74, 0, 100, 0.3) 100%); border: 1px solid rgba(74, 0, 100, 0.5);'>
        <h3 style='margin-bottom: 1rem; font-size: 2rem; background: linear-gradient(135deg, #ffffff 0%, #e0d0ff 50%, #c0a0ff 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;'>Ready to Transform Your Speaking Skills? 🚀</h3>
        <p style='color: #ffffff; margin-bottom: 1.5rem; font-size: 1.1rem;'>Select an analysis type from the sidebar to get started with AI-powered feedback!</p>
        <div style='display: inline-block; padding: 0.5rem 1.5rem; background: linear-gradient(135deg, rgba(42, 0, 64, 0.3) 0%, rgba(74, 0, 100, 0.3) 100%); border-radius: 0.75rem; border: 1px solid rgba(74, 0, 100, 0.6);'>
            <span style='color: #ffffff; font-weight: 600;'>✨ Free • Fast • AI-Powered ✨</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Close main-content wrapper
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()

