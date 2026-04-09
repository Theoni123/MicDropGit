"""
MicDrop - AI Public Speaking Coach
Main Streamlit application entry point
"""

import streamlit as st
import os
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="MicDrop - AI Public Speaking Coach",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Page background — cool off-white (pairs with coral + powder blue surfaces)
background_css = """
        background-color: #f5f8fc;
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
    
    /* Standardize all body text to same size */
    body, p, span, div, li, td, th, label, input, textarea, select, button, a {{
        font-size: 1.125rem !important;
    }}
    
    /* Keep titles at their sizes */
    h1 {{
        font-size: 2.5rem !important;
    }}
    
    h2 {{
        font-size: 2rem !important;
    }}
    
    h3 {{
        font-size: 1.5rem !important;
    }}
    
    h4 {{
        font-size: 1.25rem !important;
    }}
    
    h5, h6 {{
        font-size: 1.125rem !important;
    }}
    
    /* Override Streamlit default text sizes */
    .stMarkdown p, .stMarkdown span, .stMarkdown div, .stMarkdown li {{
        font-size: 1.125rem !important;
    }}
    
    /* Override metric labels but keep values */
    [data-testid="stMetricLabel"] {{
        font-size: 1.125rem !important;
    }}
    
    /* Caption text slightly smaller */
    .stCaption, caption {{
        font-size: 0.875rem !important;
    }}
    
    /* Override Streamlit component text sizes */
    .stText, .stTextInput > div > div > input, .stTextArea > div > div > textarea {{
        font-size: 1.125rem !important;
    }}
    
    /* Info, success, warning, error messages */
    .stAlert, .stSuccess, .stInfo, .stWarning, .stError {{
        font-size: 1.125rem !important;
    }}
    
    .stAlert p, .stSuccess p, .stInfo p, .stWarning p, .stError p {{
        font-size: 1.125rem !important;
    }}
    
    /* Expander headers */
    [data-testid="stExpander"] summary {{
        font-size: 1.125rem !important;
    }}
    
    /* Sidebar text */
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] div {{
        font-size: 1.125rem !important;
    }}
    
    /* Table text */
    table, table td, table th {{
        font-size: 1.125rem !important;
    }}
    
    /* Main column: dark text on light background */
    .main .stMarkdown, .main .stMarkdown p, .main .stMarkdown span, .main .stMarkdown div, .main .stMarkdown li,
    .main p, .main span, .main li, .main label, .main .stText, .main [data-testid="stMarkdownContainer"] p,
    .main [data-testid="stMarkdownContainer"] span, .main [data-testid="stMarkdownContainer"] div,
    .main [data-testid="stMarkdownContainer"] li {{
        color: rgba(0, 0, 0, 0.9) !important;
    }}
    
    .main h1, .main h3, .main h4, .main h5, .main h6 {{
        color: rgba(0, 0, 0, 0.92) !important;
    }}
    
    .main .stCaption, .main caption {{
        color: rgba(0, 0, 0, 0.65) !important;
    }}
    
    .main [data-testid="stExpander"] p,
    .main [data-testid="stExpander"] span,
    .main [data-testid="stExpander"] div,
    .main [data-testid="stExpander"] li {{
        color: rgba(0, 0, 0, 0.9) !important;
    }}
    
    .main [data-testid="stMetricLabel"] {{
        color: rgba(0, 0, 0, 0.85) !important;
    }}
    
    .main [data-testid="stMetricDelta"] {{
        color: rgba(0, 0, 0, 0.85) !important;
    }}
    
    .main .stInfo, .main .stSuccess, .main .stWarning, .main .stError,
    .main .stInfo p, .main .stSuccess p, .main .stWarning p, .main .stError p {{
        color: rgba(0, 0, 0, 0.9) !important;
    }}
    
    /* Sidebar: dark text on white background */
    [data-testid="stSidebar"] .stMarkdown, [data-testid="stSidebar"] p, [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] div, [data-testid="stSidebar"] li {{
        color: rgba(0, 0, 0, 0.88) !important;
    }}
    
    /* Home stat — marker sweep (matches header diffusion orange) */
    @keyframes homeStatHighlighterSweep {{
        from {{
            background-size: 0% 1.12em;
        }}
        to {{
            background-size: 100% 1.12em;
        }}
    }}

    .home-stat-highlighter,
    .stMarkdown .home-stat-highlighter,
    [data-testid="stMarkdownContainer"] .home-stat-highlighter {{
        font-weight: 600 !important;
        color: rgba(0, 0, 0, 0.9) !important;
        background-image: linear-gradient(
            120deg,
            rgba(255, 145, 70, 0.55) 0%,
            rgba(255, 130, 65, 0.5) 45%,
            rgba(250, 145, 85, 0.48) 100%
        );
        background-repeat: no-repeat;
        /* Tall marker band behind full line height */
        background-position: 0 58%;
        background-size: 0% 1.12em;
        padding: 0.08em 0.1em 0.06em 0.1em;
        margin: 0 -0.06em;
        box-decoration-break: clone;
        -webkit-box-decoration-break: clone;
        animation: homeStatHighlighterSweep 1.05s cubic-bezier(0.25, 0.8, 0.25, 1) 1.85s forwards;
    }}

    @media (prefers-reduced-motion: reduce) {{
        .home-stat-highlighter,
        .stMarkdown .home-stat-highlighter,
        [data-testid="stMarkdownContainer"] .home-stat-highlighter {{
            animation: none;
            background-size: 100% 1.12em;
        }}
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
        overflow-x: hidden;
    }}
    
    /* Apply background to Streamlit app container */
    .stApp {{
{background_css}
        position: relative;
        min-height: 100vh;
        width: 100%;
        overflow-x: hidden;
    }}
    
    /* Ensure root is transparent */
    #root {{
        background: transparent !important;
    }}
    
    /* App view container - make transparent */
    [data-testid="stAppViewContainer"] {{
        background: transparent !important;
    }}
    
    /* Main content area — Streamlit uses .stMain / stMainBlockContainer (not .main) */
    .main,
    .stMain,
    [data-testid="stMain"] {{
        background: transparent !important;
        position: relative;
    }}
    
    .main .block-container,
    .stMain .block-container,
    [data-testid="stMainBlockContainer"] {{
        position: relative;
        z-index: 1;
        background: transparent !important;
    }}
    
    /* Make all containers transparent to show background */
    .block-container, .element-container, [data-testid="column"], [data-testid="stColumn"] {{
        background: transparent !important;
    }}
    
    /* Main header — black to coral wordmark, coral diffusion */
    .main-header {{
        font-size: 4.5rem;
        font-weight: 900;
        text-align: center;
        /* Solid logo color (match subtitle) */
        color: rgba(0, 0, 0, 0.55) !important;
        background: none !important;
        -webkit-background-clip: unset !important;
        -webkit-text-fill-color: rgba(0, 0, 0, 0.55) !important;
        background-clip: unset !important;
        margin-top: 3rem;
        margin-bottom: 0.5rem;
        letter-spacing: -0.03em;
        animation: none !important;
        text-shadow: none !important;
        position: relative;
    }}

    /* Keep the mic icon solid (don’t inherit animated wordmark styling) */
    .main-header svg {{
        color: rgba(0, 0, 0, 0.55) !important;
    }}
    .main-header svg path {{
        fill: currentColor !important;
    }}
    
    .main-header::after {{
        content: '';
        position: absolute;
        top: 78%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 160px;
        height: 160px;
        /* Warm the diffusion glow: coral -> orange */
        background: radial-gradient(circle, rgba(255, 145, 70, 0.95) 0%, rgba(255, 130, 65, 0.72) 28%, rgba(250, 145, 85, 0.45) 52%, rgba(255, 185, 140, 0.18) 72%, transparent 100%);
        border-radius: 50%;
        filter: blur(28px);
        z-index: -1;
        opacity: 0;
        animation: gradientGlow 2s ease-out forwards;
        animation-delay: 1s;
    }}
    
    @keyframes gradientGlow {{
        0% {{
            width: 160px;
            height: 160px;
            opacity: 0;
            transform: translate(-50%, -50%) scale(0.5);
        }}
        50% {{
            opacity: 1;
        }}
        100% {{
            width: 420px;
            height: 420px;
            opacity: 1;
            transform: translate(-50%, -50%) scale(1);
        }}
    }}
    
    .sub-header {{
        text-align: center;
        color: rgba(0, 0, 0, 0.55) !important;
        background: none !important;
        -webkit-background-clip: unset !important;
        -webkit-text-fill-color: rgba(0, 0, 0, 0.55) !important;
        background-clip: unset !important;
        margin-bottom: 5.5rem;
        font-size: 1.125rem !important;
        font-weight: 500;
        letter-spacing: 0.01em;
    }}
    
    /* Sidebar — same cool off-white as page */
    [data-testid="stSidebar"] {{
        background: #f5f8fc;
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-right: 1px solid rgba(0, 0, 0, 0.08);
        box-shadow: 4px 0 24px rgba(0, 0, 0, 0.08);
        z-index: 9999 !important;
        /* Lock sidebar - always visible */
        display: block !important;
        visibility: visible !important;
        transform: translateX(0) !important;
        opacity: 1 !important;
    }}
    
    /* Hide sidebar toggle button completely */
    button[data-testid="baseButton-header"] {{
        display: none !important;
        visibility: hidden !important;
    }}
    
    /* Hide any sidebar toggle controls */
    [data-testid="stSidebar"] button[aria-label*="close"],
    [data-testid="stSidebar"] button[aria-label*="toggle"],
    [data-testid="stSidebar"] button[aria-label*="menu"],
    button[kind="header"] {{
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
        pointer-events: none !important;
    }}
    
    /* Force sidebar to always be expanded - override Streamlit's collapsed state */
    .stApp[data-sidebar-state="collapsed"] [data-testid="stSidebar"],
    .stApp [data-testid="stSidebar"][aria-expanded="false"] {{
        display: block !important;
        visibility: visible !important;
        transform: translateX(0) !important;
        opacity: 1 !important;
        width: auto !important;
        min-width: 21rem !important;
    }}
    
    /* Prevent sidebar from being hidden */
    [data-testid="stSidebar"] {{
        position: relative !important;
        left: 0 !important;
        margin-left: 0 !important;
    }}
    
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {{
        color: rgba(0, 0, 0, 0.88);
    }}
    
    [data-testid="stSidebar"] .stRadio label {{
        color: rgba(0, 0, 0, 0.82);
        font-weight: 500;
        padding: 0.875rem 1rem;
        border-radius: 0.75rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        margin: 0.25rem 0;
        border: 1px solid transparent;
    }}
    
    [data-testid="stSidebar"] .stRadio label:hover {{
        background: rgba(0, 0, 0, 0.04);
        border-color: rgba(0, 0, 0, 0.08);
        transform: translateX(4px);
    }}
    
    [data-testid="stSidebar"] .stRadio input:checked + label {{
        background: linear-gradient(135deg, rgba(143, 184, 237, 0.95) 0%, rgba(111, 156, 221, 0.95) 100%);
        color: white;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.45);
        border-color: rgba(143, 184, 237, 0.9);
    }}
    
    /* Metric Cards — powder blue surface */
    .metric-card {{
        background: rgba(232, 242, 251, 0.95);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        padding: 1.5rem;
        border-radius: 1.25rem;
        margin: 0.5rem 0;
        border: 1px solid rgba(91, 143, 199, 0.35);
        box-shadow: 0 8px 28px rgba(91, 143, 199, 0.12);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }}
    
    .metric-card:hover {{
        transform: translateY(-6px) scale(1.02);
        box-shadow: 0 16px 40px rgba(91, 143, 199, 0.2);
        border-color: rgba(143, 184, 237, 0.5);
        background: #e0ecf8;
    }}
    
    /* Feature Cards — powder blue surface */
    .feature-card {{
        background: rgba(232, 242, 251, 0.98);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        padding: 2.5rem;
        border-radius: 1.5rem;
        border: 1px solid rgba(91, 143, 199, 0.38);
        box-shadow: 0 8px 32px rgba(91, 143, 199, 0.14), 
                    0 0 0 1px rgba(255, 255, 255, 0.6) inset;
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
        background: linear-gradient(90deg, transparent, rgba(143, 184, 237, 0.25), transparent);
        transition: left 0.5s;
    }}
    
    .feature-card:hover::before {{
        left: 100%;
    }}
    
    .feature-card:hover {{
        box-shadow: 0 20px 48px rgba(91, 143, 199, 0.22),
                    0 0 0 1px rgba(143, 184, 237, 0.22) inset;
        transform: translateY(-8px) scale(1.01);
        border-color: rgba(143, 184, 237, 0.55);
        background: #dceaf6;
    }}
    
    .feature-card h3 {{
        color: #8fb8ed !important;
        -webkit-text-fill-color: #8fb8ed !important;
        margin-bottom: 1rem;
        font-weight: 700;
        font-size: 1.5rem !important;
    }}
    
    /* Ensure all text in feature cards is consistent */
    .feature-card p, .feature-card li, .feature-card span, .feature-card ul {{
        font-size: 1.125rem !important;
        color: rgba(0, 0, 0, 0.88) !important;
    }}
    
    /* Buttons — pastel emphasis */
    .stButton > button {{
        background: linear-gradient(135deg, #7faee8 0%, #8fb8ed 100%);
        color: white;
        border: none;
        border-radius: 0.75rem;
        padding: 0.75rem 2.5rem;
        font-weight: 600;
        font-size: 1.125rem !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 14px rgba(143, 184, 237, 0.35);
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
        box-shadow: 0 8px 24px rgba(143, 184, 237, 0.45);
    }}
    
    .stButton > button:active {{
        transform: translateY(-1px) scale(1.02);
    }}
    
    /* File Uploader */
    [data-testid="stFileUploader"] {{
        border: 2px dashed rgba(91, 143, 199, 0.45);
        border-radius: 1.25rem;
        padding: 3rem 2rem;
        background: rgba(232, 242, 251, 0.9);
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
        background: linear-gradient(45deg, transparent, rgba(143, 184, 237, 0.22), transparent);
        transform: rotate(45deg);
        transition: all 0.6s;
    }}
    
    [data-testid="stFileUploader"]:hover {{
        border-color: rgba(143, 184, 237, 0.65);
        background: #dceaf6;
        box-shadow: 0 8px 32px rgba(91, 143, 199, 0.15);
    }}
    
    [data-testid="stFileUploader"]:hover::before {{
        top: 50%;
        left: 50%;
    }}
    
    /* Main column headings — .main is legacy; Streamlit uses .stMain / stMain */
    .main h1, .main h2, .main h3,
    .stMain h1, .stMain h2, .stMain h3,
    [data-testid="stMain"] h1, [data-testid="stMain"] h2, [data-testid="stMain"] h3 {{
        color: #111111;
        font-weight: 700;
        letter-spacing: -0.02em;
    }}
    
    .main h2,
    .stMain h2,
    [data-testid="stMain"] h2 {{
        margin-top: 2.5rem;
        margin-bottom: 1.5rem;
        font-size: 2rem !important;
        color: #8fb8ed !important;
        -webkit-text-fill-color: #8fb8ed !important;
    }}

    /* Black section title on home (override blue h2 above; wrap + selectors for Streamlit DOM) */
    .main .home-section-title-black-wrap h2,
    .stMain .home-section-title-black-wrap h2,
    [data-testid="stMain"] .home-section-title-black-wrap h2,
    [data-testid="stMarkdownContainer"] .home-section-title-black-wrap h2,
    .main h2.home-section-title-black,
    .stMain h2.home-section-title-black,
    [data-testid="stMain"] h2.home-section-title-black,
    [data-testid="stMarkdownContainer"] h2.home-section-title-black {{
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
    }}
    
    .main h3,
    .stMain h3,
    [data-testid="stMain"] h3 {{
        font-size: 1.5rem !important;
        font-weight: 600;
    }}
    
    /* Alerts — pastel / black accents only */
    .stSuccess {{
        border-left: 4px solid #8fb8ed;
        border-radius: 0.75rem;
        background: rgba(143, 184, 237, 0.08);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    }}
    
    .stInfo {{
        border-left: 4px solid #5b8fc7;
        border-radius: 0.75rem;
        background: rgba(232, 242, 251, 0.9);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        box-shadow: 0 4px 12px rgba(91, 143, 199, 0.12);
    }}
    
    .stWarning {{
        border-left: 4px solid #8fb8ed;
        border-radius: 0.75rem;
        background: rgba(143, 184, 237, 0.06);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    }}
    
    /* Metrics */
    [data-testid="stMetricValue"] {{
        font-size: 2.25rem !important;
        font-weight: 800;
        background: linear-gradient(135deg, #0a0a0a 0%, #8fb8ed 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }}
    
    [data-testid="stMetricLabel"] {{
        font-weight: 600;
        color: #111111;
        font-size: 1.125rem !important;
    }}
    
    /* Expanders */
    [data-testid="stExpander"] {{
        border: 1px solid rgba(91, 143, 199, 0.35);
        border-radius: 1rem;
        margin-bottom: 1.5rem;
        background: rgba(232, 242, 251, 0.92);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        box-shadow: 0 4px 16px rgba(91, 143, 199, 0.12);
        transition: all 0.3s ease;
    }}
    
    [data-testid="stExpander"]:hover {{
        box-shadow: 0 8px 24px rgba(91, 143, 199, 0.18);
        border-color: rgba(143, 184, 237, 0.5);
        background: #e8f2fb;
    }}
    
    /* Hide Streamlit branding */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden; display: none !important;}}
    header {{visibility: hidden;}}
    
    /* Hide Streamlit footer completely */
    footer[data-testid="stFooter"],
    .stApp footer,
    footer.stApp footer,
    [data-testid="stFooter"] {{
        display: none !important;
        visibility: hidden !important;
        height: 0 !important;
        padding: 0 !important;
        margin: 0 !important;
        border: none !important;
    }}
    
    /* Hide any bottom border or line */
    .stApp > footer,
    .main footer,
    footer {{
        display: none !important;
        visibility: hidden !important;
        height: 0 !important;
        max-height: 0 !important;
        overflow: hidden !important;
    }}
    
    /* Scrollbar */
    ::-webkit-scrollbar {{
        width: 12px;
    }}
    
    ::-webkit-scrollbar-track {{
        background: rgba(91, 143, 199, 0.12);
        border-radius: 10px;
    }}
    
    ::-webkit-scrollbar-thumb {{
        background: linear-gradient(135deg, #8fb8ed 0%, #5b8fc7 100%);
        border-radius: 10px;
        border: 2px solid rgba(91, 143, 199, 0.2);
    }}
    
    ::-webkit-scrollbar-thumb:hover {{
        background: linear-gradient(135deg, #5b8fc7 0%, #8fb8ed 100%);
    }}
    
    /* Main container padding — extra top room so header diffusion glow isn’t tight to viewport */
    .main .block-container,
    .stMain .block-container,
    [data-testid="stMainBlockContainer"] {{
        padding-top: clamp(10.5rem, 20vh, 17rem) !important;
        padding-bottom: 4rem !important;
        /* Responsive gutters (used by full-bleed sections) */
        padding-left: clamp(1rem, 5vw, 5rem) !important;
        padding-right: clamp(1rem, 5vw, 5rem) !important;
        max-width: 1400px;
    }}
    
    /* Gradient text utility */
    .gradient-text {{
        background: linear-gradient(135deg, #0a0a0a 0%, #8fb8ed 100%);
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
            rgba(143, 184, 237, 0.1) 0%, 
            rgba(91, 143, 199, 0.1) 50%, 
            rgba(143, 184, 237, 0.1) 100%);
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
    
    .main .block-container > div,
    .stMain .block-container > div,
    [data-testid="stMainBlockContainer"] > div {{
        animation: fadeIn 0.6s ease-out;
    }}
    
    /* Modern input styling */
    input, textarea, select {{
        border-radius: 0.75rem !important;
        border: 1px solid rgba(226, 232, 240, 0.8) !important;
        transition: all 0.3s ease !important;
    }}
    
    input:focus, textarea:focus, select:focus {{
        border-color: #8fb8ed !important;
        box-shadow: 0 0 0 3px rgba(143, 184, 237, 0.25) !important;
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
            #0a0a0a 0%, 
            #1a1a1a 8%, 
            #0a0a0a 16%, 
            #1a1a1a 24%,
            #0a0a0a 32%,
            #1a1a1a 40%,
            #0a0a0a 48%,
            #1a1a1a 56%,
            #0a0a0a 64%,
            #1a1a1a 72%,
            #0a0a0a 80%,
            #1a1a1a 88%,
            #0a0a0a 96%,
            #1a1a1a 100%);
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
            #0a0a0a 0px,
            #1a1a1a 2px,
            #0a0a0a 4px,
            #1a1a1a 6px,
            #0a0a0a 8px
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
    
    /* Stage/platform at bottom - Hidden from the start */
    .stage-platform {{
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        height: 80px;
        background: linear-gradient(to top, 
            rgba(0, 0, 0, 0.85) 0%,
            rgba(0, 0, 0, 0.5) 50%,
            rgba(0, 0, 0, 0.25) 100%);
        z-index: 1;
        box-shadow: 0 -10px 30px rgba(0, 0, 0, 0.5);
        pointer-events: none;
        /* Hide stage platform completely - never show it */
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
        height: 0 !important;
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
    
    /* Hide stage platform after animation */
    .curtain-container.hidden .stage-platform {{
        display: none !important;
    }}
    
    @keyframes hideStage {{
        to {{
            opacity: 0;
            visibility: hidden;
            display: none;
            height: 0;
        }}
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

    /* Home hero — minimal, spacing only */
    .home-hero {{
        background: transparent;
        border: none;
        padding: clamp(3.5rem, 9vh, 7rem) 0 1rem 0;
        margin: clamp(5.5rem, 13vh, 9rem) 0 2rem 0;
        max-width: none;
        width: 100%;
        min-height: 0;
        box-shadow: none;
    }}

    .main .home-hero h2 {{
        margin-top: 0 !important;
        margin-bottom: 1rem !important;
        color: #000000 !important;
    }}
    </style>
""", unsafe_allow_html=True)

def main():
    """Main application function"""
    
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
                
                // Hide stage platform immediately (it should never be visible)
                (function() {{
                    var container = document.getElementById('curtainContainer');
                    if (container) {{
                        var stagePlatform = container.querySelector('.stage-platform');
                        if (stagePlatform) {{
                            // Hide immediately
                            stagePlatform.style.display = 'none';
                            stagePlatform.style.visibility = 'hidden';
                            stagePlatform.style.opacity = '0';
                            stagePlatform.style.height = '0';
                            stagePlatform.style.width = '0';
                            stagePlatform.style.pointerEvents = 'none';
                            // Remove from DOM completely
                            stagePlatform.remove();
                        }}
                    }}
                }})();
                
                // Also hide after a short delay to catch any late rendering
                setTimeout(function() {{
                    var container = document.getElementById('curtainContainer');
                    if (container) {{
                        var stagePlatform = container.querySelector('.stage-platform');
                        if (stagePlatform) {{
                            stagePlatform.style.display = 'none';
                            stagePlatform.style.visibility = 'hidden';
                            stagePlatform.remove();
                        }}
                    }}
                }}, 100);
                
                // Hide curtains after animation completes (3.5s animation + 0.5s delay + 0.5s buffer)
                setTimeout(function() {{
                    var container = document.getElementById('curtainContainer');
                    if (container) {{
                        container.style.display = 'none';
                        // Also explicitly hide stage platform (redundant but safe)
                        var stagePlatform = container.querySelector('.stage-platform');
                        if (stagePlatform) {{
                            stagePlatform.style.display = 'none';
                        }}
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
    
    # Lock sidebar - prevent toggling
    st.markdown("""
    <script>
    (function() {{
        // Function to lock sidebar and prevent toggling
        function lockSidebar() {{
            var sidebar = document.querySelector('[data-testid="stSidebar"]');
            if (sidebar) {{
                // Force sidebar to be visible
                sidebar.style.display = 'block';
                sidebar.style.visibility = 'visible';
                sidebar.style.transform = 'translateX(0)';
                sidebar.style.opacity = '1';
                sidebar.setAttribute('aria-expanded', 'true');
                
                // Remove any collapsed classes
                sidebar.classList.remove('collapsed');
                document.body.classList.remove('sidebar-collapsed');
                
                // Hide toggle buttons
                var toggleButtons = document.querySelectorAll(
                    'button[data-testid*="header"], ' +
                    'button[aria-label*="close"], ' +
                    'button[aria-label*="toggle"], ' +
                    'button[aria-label*="menu"], ' +
                    'button[kind="header"]'
                );
                toggleButtons.forEach(function(btn) {{
                    btn.style.display = 'none';
                    btn.style.visibility = 'hidden';
                    btn.style.opacity = '0';
                    btn.style.pointerEvents = 'none';
                }});
            }}
        }}
        
        // Lock sidebar immediately
        lockSidebar();
        
        // Lock sidebar on DOM ready
        if (document.readyState === 'loading') {{
            document.addEventListener('DOMContentLoaded', lockSidebar);
        }}
        
        // Lock sidebar after a short delay to catch late-rendered elements
        setTimeout(lockSidebar, 100);
        setTimeout(lockSidebar, 500);
        setTimeout(lockSidebar, 1000);
        
        // Continuously monitor and lock sidebar
        var lockInterval = setInterval(function() {{
            lockSidebar();
        }}, 500);
        
        // Stop monitoring after 5 seconds (sidebar should be locked by then)
        setTimeout(function() {{
            clearInterval(lockInterval);
        }}, 5000);
        
        // Prevent keyboard shortcuts from toggling sidebar
        document.addEventListener('keydown', function(e) {{
            // Block bracket keys that toggle sidebar in Streamlit
            if (e.key === '[' || e.key === ']') {{
                e.preventDefault();
                e.stopPropagation();
                lockSidebar();
                return false;
            }}
        }}, true);
        
        // Watch for sidebar state changes and force it back to expanded
        var observer = new MutationObserver(function(mutations) {{
            mutations.forEach(function(mutation) {{
                if (mutation.type === 'attributes' || mutation.type === 'childList') {{
                    lockSidebar();
                }}
            }});
        }});
        
        // Observe sidebar and app container for changes
        setTimeout(function() {{
            var sidebar = document.querySelector('[data-testid="stSidebar"]');
            var app = document.querySelector('.stApp');
            if (sidebar) {{
                observer.observe(sidebar, {{
                    attributes: true,
                    attributeFilter: ['class', 'style', 'aria-expanded'],
                    childList: true,
                    subtree: true
                }});
            }}
            if (app) {{
                observer.observe(app, {{
                    attributes: true,
                    attributeFilter: ['data-sidebar-state'],
                    childList: false
                }});
            }}
        }}, 500);
    }})();
    </script>
    """, unsafe_allow_html=True)
    
    # Header with curtain reveal effect
    st.markdown('''
    <div class="main-content">
        <h1 class="main-header">
            <svg class="icon icon-xl" style="display: inline-block; vertical-align: middle; margin-right: 0.25rem; width: 3rem; height: 3rem; color: rgba(0, 0, 0, 0.55);" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3z" fill="currentColor"/>
                <path d="M17 11c0 2.76-2.24 5-5 5s-5-2.24-5-5H5c0 3.53 2.61 6.43 6 6.92V21h2v-3.08c3.39-.49 6-3.39 6-6.92h-2z" fill="currentColor"/>
            </svg>
            MicDrop
        </h1>
    </div>
    ''', unsafe_allow_html=True)
    st.markdown('<div class="main-content"><p class="sub-header">AI Public Speaking Coach</p></div>', unsafe_allow_html=True)
    
    # Sidebar navigation with modern header
    st.sidebar.markdown("""
    <div style='text-align: center; padding: 1.5rem 0 2rem 0; border-bottom: 1px solid rgba(0, 0, 0, 0.08); margin-bottom: 1.5rem;'>
        <h2 style='color: rgba(0, 0, 0, 0.82) !important; font-size: 1.5rem !important; font-weight: 700; margin: 0; letter-spacing: -0.02em; display: flex; align-items: center; justify-content: center; gap: 0.5rem;'>
            <svg style="width: 1.5rem; height: 1.5rem; fill: #8fb8ed;" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3z" fill="#8fb8ed"/>
                <path d="M17 11c0 2.76-2.24 5-5 5s-5-2.24-5-5H5c0 3.53 2.61 6.43 6 6.92V21h2v-3.08c3.39-.49 6-3.39 6-6.92h-2z" fill="#8fb8ed"/>
            </svg>
            MicDrop
        </h2>
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
        color: rgba(0, 0, 0, 0.78) !important;
        border-radius: 0.5rem !important;
        transition: all 0.3s ease !important;
        margin-bottom: 0.5rem !important;
        box-shadow: none !important;
        font-weight: 500 !important;
        position: relative !important;
    }
    [data-testid="stSidebar"] .stButton > button:hover {
        background: rgba(0, 0, 0, 0.04) !important;
        border-color: rgba(0, 0, 0, 0.08) !important;
        transform: translateX(4px) !important;
    }
    [data-testid="stSidebar"] .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, rgba(143, 184, 237, 0.98) 0%, rgba(111, 156, 221, 0.95) 100%) !important;
        border-color: rgba(255, 255, 255, 0.25) !important;
        color: white !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25) !important;
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
        background-image: url('data:image/svg+xml;utf8,<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z" fill="rgba(0,0,0,0.78)"/></svg>');
    }
    
    /* Voice Analysis icon */
    [data-testid="stSidebar"] button[data-testid*="nav_Voice"]::before {
        background-image: url('data:image/svg+xml;utf8,<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3z" fill="rgba(0,0,0,0.78)"/><path d="M17 11c0 2.76-2.24 5-5 5s-5-2.24-5-5H5c0 3.53 2.61 6.43 6 6.92V21h2v-3.08c3.39-.49 6-3.39 6-6.92h-2z" fill="rgba(0,0,0,0.78)"/></svg>');
    }
    
    /* Language Analysis icon */
    [data-testid="stSidebar"] button[data-testid*="nav_Language"]::before {
        background-image: url('data:image/svg+xml;utf8,<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25zM20.71 7.04c.39-.39.39-1.02 0-1.41l-2.34-2.34c-.39-.39-1.02-.39-1.41 0l-1.83 1.83 3.75 3.75 1.83-1.83z" fill="rgba(0,0,0,0.78)"/></svg>');
    }
    
    /* Body Language Analysis icon */
    [data-testid="stSidebar"] button[data-testid*="nav_Body"]::before {
        background-image: url('data:image/svg+xml;utf8,<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z" fill="rgba(0,0,0,0.78)"/></svg>');
    }
    
    /* AI Coach icon */
    [data-testid="stSidebar"] button[data-testid*="Coach"]::before {
        background-image: url('data:image/svg+xml;utf8,<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z" fill="rgba(0,0,0,0.78)"/></svg>');
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
        "AI Coach": "AI Coach",
        "Voice Analysis": "Voice Analysis",
        "Language Analysis": "Language Analysis",
        "Body Language Analysis": "Body Language Analysis"
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
    elif page == "AI Coach":
        from page_modules import comprehensive_report
        comprehensive_report.show()

def show_home():
    """Display home page with instructions"""
    
    # Wrap content in main-content div for fade-in effect
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    
    # Introduction
    st.markdown("""
    <div class="home-hero">
        <div style='text-align: center; padding: 0; margin: 0;'>
            <p style='font-size: 1.125rem !important; color: rgba(0, 0, 0, 0.9); font-weight: 400; max-width: 700px; margin: 0 auto;'>
                <span class='home-stat-highlighter'>75% of people</span> are afraid of public speaking.
                <a href='https://www.healthcentral.com/condition/anxiety/glossophobia-fear-of-public-' target='_blank' rel='noopener noreferrer' style='color: rgba(0, 0, 0, 0.65); text-decoration: none; margin-left: 0.5rem; display: inline-block; vertical-align: middle;' title='Source'>
                    <svg style='width: 1em; height: 1em; fill: currentColor;' viewBox='0 0 24 24' xmlns='http://www.w3.org/2000/svg'>
                        <path d='M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z'/>
                    </svg>
                </a>
            </p>
            <p style='font-size: 1.125rem !important; color: rgba(0, 0, 0, 0.9); font-weight: 400; max-width: 700px; margin: 1.25rem auto 0 auto;'>
                Let's change that! With your personal AI coach, master the art of confident communication.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature Cards
    st.markdown("""
    <div class='home-section-title-black-wrap'>
    <h2 class='home-section-title-black' style='margin-bottom: 1rem; font-size: 2rem !important; font-weight: 700;'>Analysis Features</h2>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class='feature-card'>
            <h3 style='color: #8fb8ed; margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem;'>
                <svg style="width: 1.5rem; height: 1.5rem; fill: currentColor;" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3z" fill="currentColor"/>
                    <path d="M17 11c0 2.76-2.24 5-5 5s-5-2.24-5-5H5c0 3.53 2.61 6.43 6 6.92V21h2v-3.08c3.39-.49 6-3.39 6-6.92h-2z" fill="currentColor"/>
                </svg>
                Voice Analysis
            </h3>
            <ul style='color: rgba(0, 0, 0, 0.88); line-height: 1.8;'>
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
            <h3 style='color: #8fb8ed; margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem;'>
                <svg style="width: 1.5rem; height: 1.5rem; fill: currentColor;" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25zM20.71 7.04c.39-.39.39-1.02 0-1.41l-2.34-2.34c-.39-.39-1.02-.39-1.41 0l-1.83 1.83 3.75 3.75 1.83-1.83z" fill="currentColor"/>
                </svg>
                Language Analysis
            </h3>
            <ul style='color: rgba(0, 0, 0, 0.88); line-height: 1.8;'>
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
            <h3 style='color: #8fb8ed; margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem;'>
                <svg style="width: 1.5rem; height: 1.5rem; fill: currentColor;" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z" fill="currentColor"/>
                </svg>
                Body Language Analysis
            </h3>
            <ul style='color: rgba(0, 0, 0, 0.88); line-height: 1.8;'>
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
    st.markdown("""
    <div style='color: rgba(0, 0, 0, 0.88); line-height: 1.8;'>
        <h2 style='margin-bottom: 1rem; font-size: 2rem !important; font-weight: 700; color: #8fb8ed !important;'>Getting Started</h2>
        <ol style='color: rgba(0, 0, 0, 0.88); line-height: 1.8; padding-left: 1.5rem;'>
            <li><strong>Choose an analysis type</strong> from the sidebar</li>
            <li><strong>Upload</strong> audio/video</li>
            <li><strong>Review</strong> your feedback and recommendations</li>
            <li><strong>Practice and improve!</strong></li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Call to Action - Clickable Card
    st.markdown("""
    <div style='margin-top: 3rem;'>
    """, unsafe_allow_html=True)
    
    # Create clickable button styled as card
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        if st.button("Start Your AI Coaching Session", key="cta_ai_coach", use_container_width=True, type="primary"):
            st.session_state.current_page = "AI Coach"
            st.rerun()
    
    # Style the button with modern glassmorphism
    st.markdown("""
    <style>
    @keyframes pulse-glow {
        0%, 100% {
            box-shadow: 
                0 12px 48px 0 rgba(143, 184, 237, 0.28),
                inset 0 2px 0 0 rgba(255, 255, 255, 0.3),
                0 0 0 1px rgba(255, 255, 255, 0.1),
                0 0 40px rgba(143, 184, 237, 0.18);
        }
        50% {
            box-shadow: 
                0 12px 48px 0 rgba(143, 184, 237, 0.45),
                inset 0 2px 0 0 rgba(255, 255, 255, 0.4),
                0 0 0 1px rgba(255, 255, 255, 0.2),
                0 0 60px rgba(143, 184, 237, 0.35);
        }
    }
    
    button[data-testid*="cta_ai_coach"] {
        background: rgba(143, 184, 237, 0.18) !important;
        backdrop-filter: blur(30px) saturate(200%) !important;
        -webkit-backdrop-filter: blur(30px) saturate(200%) !important;
        border: 2px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 25px !important;
        padding: 4rem 3rem !important;
        text-align: center !important;
        cursor: pointer !important;
        transition: all 0.5s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
        box-shadow: 
            0 12px 48px 0 rgba(143, 184, 237, 0.28),
            inset 0 2px 0 0 rgba(255, 255, 255, 0.3),
            0 0 0 1px rgba(255, 255, 255, 0.1),
            0 0 40px rgba(143, 184, 237, 0.18) !important;
        height: auto !important;
        min-height: 240px !important;
        position: relative !important;
        overflow: hidden !important;
        animation: pulse-glow 3s ease-in-out infinite !important;
    }
    
    button[data-testid*="cta_ai_coach"]::before {
        content: '' !important;
        position: absolute !important;
        top: -50% !important;
        left: -50% !important;
        width: 200% !important;
        height: 200% !important;
        background: radial-gradient(circle, rgba(255, 255, 255, 0.15) 0%, transparent 70%) !important;
        opacity: 0 !important;
        transition: opacity 0.5s ease !important;
    }
    
    button[data-testid*="cta_ai_coach"]::after {
        content: '' !important;
        position: absolute !important;
        top: 0 !important;
        left: -100% !important;
        width: 100% !important;
        height: 100% !important;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent) !important;
        transition: left 0.6s ease !important;
    }
    
    button[data-testid*="cta_ai_coach"]:hover {
        transform: translateY(-8px) scale(1.03) !important;
        box-shadow: 
            0 24px 80px 0 rgba(143, 184, 237, 0.45),
            inset 0 3px 0 0 rgba(255, 255, 255, 0.5),
            0 0 0 2px rgba(143, 184, 237, 0.4),
            0 0 80px rgba(143, 184, 237, 0.35) !important;
        border-color: rgba(255, 255, 255, 0.5) !important;
        background: rgba(143, 184, 237, 0.28) !important;
        animation: none !important;
    }
    
    button[data-testid*="cta_ai_coach"]:hover::before {
        opacity: 1 !important;
    }
    
    button[data-testid*="cta_ai_coach"]:hover::after {
        left: 100% !important;
    }
    
    button[data-testid*="cta_ai_coach"]:active {
        transform: translateY(-4px) scale(0.98) !important;
        box-shadow: 
            0 12px 40px 0 rgba(143, 184, 237, 0.5),
            inset 0 4px 0 0 rgba(255, 255, 255, 0.6),
            0 0 0 3px rgba(143, 184, 237, 0.45),
            0 0 60px rgba(143, 184, 237, 0.45) !important;
    }
    
    button[data-testid*="cta_ai_coach"]:focus {
        box-shadow: 
            0 20px 64px 0 rgba(143, 184, 237, 0.45),
            inset 0 2px 0 0 rgba(255, 255, 255, 0.4),
            0 0 0 3px rgba(143, 184, 237, 0.4),
            0 0 80px rgba(143, 184, 237, 0.38) !important;
        outline: none !important;
    }
    
    button[data-testid*="cta_ai_coach"] p {
        color: white !important;
        font-size: 1.75rem !important;
        font-weight: 700 !important;
        margin: 0 !important;
        text-shadow: 
            0 2px 10px rgba(0, 0, 0, 0.4), 
            0 0 30px rgba(143, 184, 237, 0.45),
            0 0 10px rgba(255, 255, 255, 0.3) !important;
        letter-spacing: 0.8px !important;
        text-transform: uppercase !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Close main-content wrapper
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()

