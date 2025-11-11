"""
Body Language Analysis Page
Analyzes body language: posture, gestures, eye contact, facial expressions
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

# Check for required dependencies
try:
    import cv2
    import mediapipe as mp
    HAS_VIDEO_DEPS = True
except ImportError:
    HAS_VIDEO_DEPS = False

if HAS_VIDEO_DEPS:
    from utils.video_processor import process_video
    from utils.feedback_generator import generate_body_language_feedback


def show():
    """Display body language analysis page"""
    
    st.markdown("""
    <h1 style='display: flex; align-items: center; gap: 0.75rem; color: #ffffff;'>
        <svg style="width: 2rem; height: 2rem; fill: currentColor;" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z" fill="currentColor"/>
        </svg>
        Body Language Analysis
    </h1>
    """, unsafe_allow_html=True)
    st.markdown("Analyze your posture, gestures, eye contact, facial expressions, and movement")
    
    # Check if dependencies are installed
    if not HAS_VIDEO_DEPS:
        st.error("⚠️ **Missing Dependencies**")
        st.markdown("""
        The body language analysis requires additional packages that are not currently installed.
        
        **To install the required dependencies, run:**
        ```bash
        pip install opencv-python mediapipe
        ```
        
        Or install all dependencies:
        ```bash
        pip install -r requirements.txt
        ```
        
        **Note:** If you're using Python 3.13, MediaPipe may not be available yet. 
        Consider using Python 3.11 or 3.12 for full functionality.
        """)
        return
    
    # File upload section
    st.header("Upload Video")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        video_file = st.file_uploader(
            "Choose a video file",
            type=['mp4', 'webm', 'mov', 'avi'],
            help="Supported formats: MP4, WebM, MOV, AVI"
        )
    
    with col2:
        st.markdown("### Or")
        record_video = st.button("📹 Record Video", use_container_width=True)
    
    if record_video:
        st.info("Video recording feature coming soon! Please upload a video file for now.")
    
    # Processing options
    if video_file is not None:
        st.sidebar.header("Processing Options")
        max_frames = st.sidebar.slider(
            "Max frames to process",
            min_value=10,
            max_value=200,
            value=100,
            help="Lower values = faster processing, less detailed analysis"
        )
        
        # Process video
        with st.spinner("Processing video... This may take a moment."):
            try:
                # Process video
                body_metrics = process_video(video_file, max_frames=max_frames)
                
                # Show basic info
                duration = body_metrics.get('duration', 0)
                frames_processed = body_metrics.get('frames_processed', 0)
                st.success(
                    f"✅ Video processed successfully! "
                    f"Duration: {duration:.2f}s, Frames analyzed: {frames_processed}"
                )
                
                # Generate feedback
                feedback = generate_body_language_feedback(body_metrics)
                
                # Display results
                display_results(body_metrics, feedback)
                
            except Exception as e:
                st.error(f"❌ Error processing video: {str(e)}")
                st.exception(e)
                st.info(
                    "💡 **Tips for better results:**\n"
                    "- Ensure good lighting\n"
                    "- Keep your full body visible\n"
                    "- Use MP4 format for best compatibility\n"
                    "- Keep video under 5 minutes for faster processing"
                )


def display_results(body_metrics, feedback):
    """Display body language analysis results"""
    
    st.header("📊 Analysis Results")
    
    # Key Metrics
    st.subheader("Key Metrics")
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        posture_score = body_metrics.get('posture', {}).get('posture_score', 0.0)
        posture_label = "Good" if posture_score > 0.7 else ("Fair" if posture_score > 0.5 else "Needs Work")
        st.metric("Posture", posture_label, f"{posture_score*100:.0f}%")
    
    with col2:
        gesture_freq = body_metrics.get('gestures', {}).get('gesture_frequency', 0.0)
        gesture_label = "Good" if 0.5 <= gesture_freq <= 3.0 else ("Low" if gesture_freq < 0.5 else "Excessive")
        st.metric("Gestures", f"{gesture_freq:.1f}/sec", gesture_label)
    
    with col3:
        eye_contact_pct = body_metrics.get('eye_contact', {}).get('eye_contact_percentage', 0.0)
        eye_label = "Good" if eye_contact_pct > 0.6 else ("Fair" if eye_contact_pct > 0.3 else "Low")
        st.metric("Eye Contact", f"{eye_contact_pct*100:.0f}%", eye_label)
    
    with col4:
        engagement = body_metrics.get('facial_expressions', {}).get('engagement_score', 0.0)
        engagement_label = "Good" if engagement > 0.6 else ("Moderate" if engagement > 0.4 else "Low")
        st.metric("Engagement", f"{engagement*100:.0f}%", engagement_label)
    
    with col5:
        presence = body_metrics.get('presence_score', 0.0)
        presence_label = "Excellent" if presence > 0.7 else ("Good" if presence > 0.5 else "Needs Work")
        st.metric("Overall Presence", f"{presence*100:.0f}%", presence_label)
    
    # Detailed Visualizations
    st.subheader("📈 Detailed Analysis")
    
    # Posture and Movement
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Posture Analysis**")
        posture = body_metrics.get('posture', {})
        posture_score = posture.get('posture_score', 0.0)
        upright_pct = posture.get('upright_percentage', 0.0)
        
        fig_posture = go.Figure()
        fig_posture.add_trace(go.Indicator(
            mode="gauge+number",
            value=posture_score * 100,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Posture Score"},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': "darkgreen"},
                'steps': [
                    {'range': [0, 50], 'color': "lightgray"},
                    {'range': [50, 70], 'color': "gray"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 70
                }
            }
        ))
        fig_posture.update_layout(height=300)
        st.plotly_chart(fig_posture, use_container_width=True)
        
        st.caption(f"Upright: {upright_pct*100:.0f}% | Spine angle: {posture.get('spine_alignment', 0):.1f}°")
    
    with col2:
        st.markdown("**Movement Analysis**")
        movement = body_metrics.get('movement', {})
        movement_type = movement.get('movement_type', 'unknown')
        movement_score = movement.get('movement_score', 0.0)
        
        # Movement type indicator
        movement_colors = {
            'stationary': 'orange',
            'appropriate': 'green',
            'excessive': 'red',
            'unknown': 'gray'
        }
        
        fig_movement = go.Figure()
        fig_movement.add_trace(go.Indicator(
            mode="gauge+number",
            value=movement_score * 100,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Movement Score"},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': movement_colors.get(movement_type, 'gray')},
                'steps': [
                    {'range': [0, 30], 'color': "lightgray"},
                    {'range': [30, 70], 'color': "gray"}
                ]
            }
        ))
        fig_movement.update_layout(height=300)
        st.plotly_chart(fig_movement, use_container_width=True)
        
        st.caption(f"Type: {movement_type.title()} | Avg movement: {movement.get('average_movement', 0):.4f}")
    
    # Gestures and Eye Contact
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Gesture Analysis**")
        gestures = body_metrics.get('gestures', {})
        gesture_count = gestures.get('gesture_count', 0)
        hands_visible = gestures.get('hands_visible_percentage', 0.0)
        
        fig_gestures = go.Figure()
        fig_gestures.add_trace(go.Bar(
            x=['Gestures Detected', 'Hands Visible'],
            y=[gesture_count, hands_visible * 100],
            marker_color=['coral', 'lightblue'],
            name='Metrics'
        ))
        fig_gestures.update_layout(
            title="Gesture Metrics",
            yaxis_title="Count / Percentage",
            height=300
        )
        st.plotly_chart(fig_gestures, use_container_width=True)
        
        st.caption(f"Gesture frequency: {gestures.get('gesture_frequency', 0):.2f} per second")
    
    with col2:
        st.markdown("**Eye Contact Analysis**")
        eye_contact = body_metrics.get('eye_contact', {})
        eye_contact_pct = eye_contact.get('eye_contact_percentage', 0.0)
        face_visible = eye_contact.get('face_visible_percentage', 0.0)
        gaze_direction = eye_contact.get('gaze_direction', 'unknown')
        
        fig_eye = go.Figure()
        fig_eye.add_trace(go.Indicator(
            mode="gauge+number",
            value=eye_contact_pct * 100,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Eye Contact %"},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 30], 'color': "lightgray"},
                    {'range': [30, 60], 'color': "gray"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 60
                }
            }
        ))
        fig_eye.update_layout(height=300)
        st.plotly_chart(fig_eye, use_container_width=True)
        
        st.caption(f"Face visible: {face_visible*100:.0f}% | Gaze: {gaze_direction.title()}")
    
    # Facial Expressions
    st.markdown("**Facial Expression Analysis**")
    expressions = body_metrics.get('facial_expressions', {})
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Engagement Score", f"{expressions.get('engagement_score', 0)*100:.0f}%")
    with col2:
        st.metric("Confidence Score", f"{expressions.get('confidence_score', 0)*100:.0f}%")
    with col3:
        st.metric("Smile Percentage", f"{expressions.get('smile_percentage', 0)*100:.0f}%")
    
    # Feedback and Recommendations
    st.header("💡 Feedback & Recommendations")
    
    for i, recommendation in enumerate(feedback['recommendations'], 1):
        st.info(f"{i}. {recommendation}")
    
    # Summary scores
    st.subheader("Summary Scores")
    scores = feedback['scores']
    
    score_colors = {
        'poor': '🔴',
        'fair': '🟡',
        'good': '🟢',
        'excellent': '🟢',
        'low': '🟡',
        'moderate': '🟡',
        'excessive': '🔴',
        'stationary': '🟡',
        'appropriate': '🟢',
        'needs_improvement': '🔴'
    }
    
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        score_key = scores.get('posture', 'N/A')
        st.markdown(f"**Posture:** {score_colors.get(score_key, '⚪')} {score_key.title() if score_key != 'N/A' else 'N/A'}")
    with col2:
        score_key = scores.get('gestures', 'N/A')
        st.markdown(f"**Gestures:** {score_colors.get(score_key, '⚪')} {score_key.title() if score_key != 'N/A' else 'N/A'}")
    with col3:
        score_key = scores.get('eye_contact', 'N/A')
        st.markdown(f"**Eye Contact:** {score_colors.get(score_key, '⚪')} {score_key.title() if score_key != 'N/A' else 'N/A'}")
    with col4:
        score_key = scores.get('facial_expressions', 'N/A')
        st.markdown(f"**Expressions:** {score_colors.get(score_key, '⚪')} {score_key.title() if score_key != 'N/A' else 'N/A'}")
    with col5:
        score_key = scores.get('movement', 'N/A')
        st.markdown(f"**Movement:** {score_colors.get(score_key, '⚪')} {score_key.title() if score_key != 'N/A' else 'N/A'}")
    
    st.markdown(f"**Overall Presence:** {score_colors.get(scores.get('overall', 'N/A'), '⚪')} {scores.get('overall', 'N/A').title().replace('_', ' ') if scores.get('overall', 'N/A') != 'N/A' else 'N/A'}")
