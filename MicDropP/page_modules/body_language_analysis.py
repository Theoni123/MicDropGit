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
    st.markdown("Analyze your posture, gestures, eye contact, facial expressions, and movement.")
    
    # Tips for best results
    with st.expander("Tips for Best Results", expanded=False):
        st.markdown("""
        - **Video Quality**: Ensure good lighting so your face and body are clearly visible
        - **Full Body View**: Keep your full body visible in the frame for best analysis
        - **Lighting**: Use natural or bright lighting - avoid backlighting or shadows
        - **Duration**: 30 seconds to 5 minutes works best
        - **Format**: MP4, WebM, MOV, or AVI formats are supported
        - **Positioning**: Stand or sit straight, facing the camera for optimal analysis
        - **Stability**: Keep the camera stable or use a tripod for clearer video
        """)
    
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
        record_video = st.button("Record Video", use_container_width=True)
    
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
                    "**Tips for better results:**\n"
                    "- Ensure good lighting\n"
                    "- Keep your full body visible\n"
                    "- Use MP4 format for best compatibility\n"
                    "- Keep video under 5 minutes for faster processing"
                )


def display_results(body_metrics, feedback):
    """Display body language analysis results"""
    
    st.markdown("---")
    st.markdown("## 📊 Analysis Results")
    st.markdown("")
    
    # Key Metrics with modern cards
    st.markdown("### 🎯 Key Metrics")
    st.markdown("")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    posture_score = body_metrics.get('posture', {}).get('posture_score', 0.0)
    gesture_freq = body_metrics.get('gestures', {}).get('gesture_frequency', 0.0)
    eye_contact_pct = body_metrics.get('eye_contact', {}).get('eye_contact_percentage', 0.0)
    engagement = body_metrics.get('facial_expressions', {}).get('engagement_score', 0.0)
    presence = body_metrics.get('presence_score', 0.0)
    
    # Determine status colors
    posture_color = "#10b981" if posture_score > 0.7 else ("#f59e0b" if posture_score > 0.5 else "#ef4444")
    gesture_color = "#10b981" if 0.5 <= gesture_freq <= 3.0 else ("#f59e0b" if gesture_freq < 0.5 or gesture_freq <= 4.0 else "#ef4444")
    eye_color = "#10b981" if eye_contact_pct > 0.6 else ("#f59e0b" if eye_contact_pct > 0.3 else "#ef4444")
    engagement_color = "#10b981" if engagement > 0.6 else ("#f59e0b" if engagement > 0.4 else "#ef4444")
    presence_color = "#10b981" if presence > 0.7 else ("#f59e0b" if presence > 0.5 else "#ef4444")
    
    with col1:
        posture_label = "Good" if posture_score > 0.7 else ("Fair" if posture_score > 0.5 else "Needs Work")
        st.markdown(f"""
        <div class='metric-card' style='text-align: center; padding: 1.5rem; border-left: 4px solid {posture_color};'>
            <div style='font-size: 0.875rem; color: rgba(255, 255, 255, 0.7); font-weight: 500; margin-bottom: 0.5rem;'>POSTURE</div>
            <div style='font-size: 2.5rem; font-weight: 800; color: {posture_color}; margin-bottom: 0.25rem;'>{posture_score*100:.0f}%</div>
            <div style='font-size: 0.875rem; color: rgba(255, 255, 255, 0.6);'>{posture_label}</div>
            <div style='font-size: 0.75rem; color: rgba(255, 255, 255, 0.5); margin-top: 0.5rem;'>Alignment & stance</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        gesture_label = "Good" if 0.5 <= gesture_freq <= 3.0 else ("Low" if gesture_freq < 0.5 else "Excessive")
        st.markdown(f"""
        <div class='metric-card' style='text-align: center; padding: 1.5rem; border-left: 4px solid {gesture_color};'>
            <div style='font-size: 0.875rem; color: rgba(255, 255, 255, 0.7); font-weight: 500; margin-bottom: 0.5rem;'>GESTURES</div>
            <div style='font-size: 2.5rem; font-weight: 800; color: {gesture_color}; margin-bottom: 0.25rem;'>{gesture_freq:.1f}</div>
            <div style='font-size: 0.875rem; color: rgba(255, 255, 255, 0.6);'>per second</div>
            <div style='font-size: 0.75rem; color: rgba(255, 255, 255, 0.5); margin-top: 0.5rem;'>{gesture_label} frequency</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        eye_label = "Good" if eye_contact_pct > 0.6 else ("Fair" if eye_contact_pct > 0.3 else "Low")
        st.markdown(f"""
        <div class='metric-card' style='text-align: center; padding: 1.5rem; border-left: 4px solid {eye_color};'>
            <div style='font-size: 0.875rem; color: rgba(255, 255, 255, 0.7); font-weight: 500; margin-bottom: 0.5rem;'>EYE CONTACT</div>
            <div style='font-size: 2.5rem; font-weight: 800; color: {eye_color}; margin-bottom: 0.25rem;'>{eye_contact_pct*100:.0f}%</div>
            <div style='font-size: 0.875rem; color: rgba(255, 255, 255, 0.6);'>{eye_label} level</div>
            <div style='font-size: 0.75rem; color: rgba(255, 255, 255, 0.5); margin-top: 0.5rem;'>Camera gaze</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        engagement_label = "Good" if engagement > 0.6 else ("Moderate" if engagement > 0.4 else "Low")
        st.markdown(f"""
        <div class='metric-card' style='text-align: center; padding: 1.5rem; border-left: 4px solid {engagement_color};'>
            <div style='font-size: 0.875rem; color: rgba(255, 255, 255, 0.7); font-weight: 500; margin-bottom: 0.5rem;'>ENGAGEMENT</div>
            <div style='font-size: 2.5rem; font-weight: 800; color: {engagement_color}; margin-bottom: 0.25rem;'>{engagement*100:.0f}%</div>
            <div style='font-size: 0.875rem; color: rgba(255, 255, 255, 0.6);'>{engagement_label} score</div>
            <div style='font-size: 0.75rem; color: rgba(255, 255, 255, 0.5); margin-top: 0.5rem;'>Expressions</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        presence_label = "Excellent" if presence > 0.7 else ("Good" if presence > 0.5 else "Needs Work")
        st.markdown(f"""
        <div class='metric-card' style='text-align: center; padding: 1.5rem; border-left: 4px solid {presence_color};'>
            <div style='font-size: 0.875rem; color: rgba(255, 255, 255, 0.7); font-weight: 500; margin-bottom: 0.5rem;'>PRESENCE</div>
            <div style='font-size: 2.5rem; font-weight: 800; color: {presence_color}; margin-bottom: 0.25rem;'>{presence*100:.0f}%</div>
            <div style='font-size: 0.875rem; color: rgba(255, 255, 255, 0.6);'>{presence_label}</div>
            <div style='font-size: 0.75rem; color: rgba(255, 255, 255, 0.5); margin-top: 0.5rem;'>Overall</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("")
    st.markdown("")
    
    # Detailed Visualizations
    st.markdown("### 📈 Detailed Analysis")
    st.markdown("")
    
    # Posture and Movement
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🧍 Posture Analysis")
        posture = body_metrics.get('posture', {})
        posture_score = posture.get('posture_score', 0.0)
        upright_pct = posture.get('upright_percentage', 0.0)
        
        fig_posture = go.Figure()
        fig_posture.add_trace(go.Indicator(
            mode="gauge+number",
            value=posture_score * 100,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Posture Score", 'font': {'size': 16, 'color': 'white'}},
            gauge={
                'axis': {
                    'range': [None, 100], 
                    'tickcolor': 'white',
                    'tickfont': {'color': 'white'}
                },
                'bar': {'color': posture_color},
                'bgcolor': 'rgba(42, 0, 64, 0.3)',
                'steps': [
                    {'range': [0, 50], 'color': "rgba(239, 68, 68, 0.2)"},
                    {'range': [50, 70], 'color': "rgba(245, 158, 11, 0.2)"},
                    {'range': [70, 100], 'color': "rgba(16, 185, 129, 0.2)"}
                ],
                'threshold': {
                    'line': {'color': "white", 'width': 2},
                    'thickness': 0.75,
                    'value': 70
                }
            },
            number={'font': {'size': 32, 'color': posture_color}}
        ))
        fig_posture.update_layout(
            height=300,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font={'color': 'white'}
        )
        st.plotly_chart(fig_posture, use_container_width=True)
        
        st.markdown(f"""
        <div style='text-align: center; font-size: 0.875rem; color: rgba(255, 255, 255, 0.6);'>
            Upright: {upright_pct*100:.0f}% | Spine angle: {posture.get('spine_alignment', 0):.1f}°
        </div>
        """, unsafe_allow_html=True)
    
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
            title={'text': "Movement Score", 'font': {'size': 16, 'color': 'white'}},
            gauge={
                'axis': {
                    'range': [None, 100],
                    'tickcolor': 'white',
                    'tickfont': {'color': 'white'}
                },
                'bar': {'color': movement_colors.get(movement_type, 'gray')},
                'bgcolor': 'rgba(42, 0, 64, 0.3)',
                'steps': [
                    {'range': [0, 30], 'color': "rgba(239, 68, 68, 0.2)"},
                    {'range': [30, 70], 'color': "rgba(245, 158, 11, 0.2)"},
                    {'range': [70, 100], 'color': "rgba(16, 185, 129, 0.2)"}
                ]
            },
            number={'font': {'size': 32, 'color': movement_colors.get(movement_type, 'gray')}}
        ))
        fig_movement.update_layout(
            height=300,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font={'color': 'white', 'size': 12}
        )
        st.plotly_chart(fig_movement, use_container_width=True)
        
        st.markdown(f"""
        <div style='text-align: center; font-size: 0.875rem; color: rgba(255, 255, 255, 0.6);'>
            Type: {movement_type.title()} | Avg movement: {movement.get('average_movement', 0):.4f}
        </div>
        """, unsafe_allow_html=True)
    
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
            title={'text': "Gesture Metrics", 'font': {'color': 'white', 'size': 16}},
            yaxis_title="Count / Percentage",
            height=300,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(42, 0, 64, 0.2)',
            font={'color': 'white', 'size': 12},
            xaxis={
                'gridcolor': 'rgba(255,255,255,0.1)',
                'color': 'white',
                'title': {'font': {'color': 'white'}},
                'tickfont': {'color': 'white'}
            },
            yaxis={
                'gridcolor': 'rgba(255,255,255,0.1)',
                'color': 'white',
                'title': {'font': {'color': 'white'}},
                'tickfont': {'color': 'white'}
            }
        )
        st.plotly_chart(fig_gestures, use_container_width=True)
        
        st.markdown(f"""
        <div style='text-align: center; font-size: 0.875rem; color: rgba(255, 255, 255, 0.6);'>
            Gesture frequency: {gestures.get('gesture_frequency', 0):.2f} per second
        </div>
        """, unsafe_allow_html=True)
    
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
            title={'text': "Eye Contact %", 'font': {'size': 16, 'color': 'white'}},
            gauge={
                'axis': {
                    'range': [None, 100], 
                    'tickcolor': 'white',
                    'tickfont': {'color': 'white'}
                },
                'bar': {'color': eye_color},
                'bgcolor': 'rgba(42, 0, 64, 0.3)',
                'steps': [
                    {'range': [0, 30], 'color': "rgba(239, 68, 68, 0.2)"},
                    {'range': [30, 60], 'color': "rgba(245, 158, 11, 0.2)"},
                    {'range': [60, 100], 'color': "rgba(16, 185, 129, 0.2)"}
                ],
                'threshold': {
                    'line': {'color': "white", 'width': 2},
                    'thickness': 0.75,
                    'value': 60
                }
            },
            number={'font': {'size': 32, 'color': eye_color}}
        ))
        fig_eye.update_layout(
            height=300,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font={'color': 'white', 'size': 12}
        )
        st.plotly_chart(fig_eye, use_container_width=True)
        
        st.markdown(f"""
        <div style='text-align: center; font-size: 0.875rem; color: rgba(255, 255, 255, 0.6);'>
            Face visible: {face_visible*100:.0f}% | Gaze: {gaze_direction.title()}
        </div>
        """, unsafe_allow_html=True)
    
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
    st.markdown("---")
    st.markdown("## 💡 Feedback & Recommendations")
    st.markdown("")
    
    # Display recommendations in organized cards
    for i, recommendation in enumerate(feedback['recommendations'], 1):
        # Determine recommendation type based on content
        if any(word in recommendation.lower() for word in ['great', 'excellent', 'good']):
            rec_color = "#10b981"
            rec_icon = "✅"
        elif any(word in recommendation.lower() for word in ['try', 'consider', 'could']):
            rec_color = "#f59e0b"
            rec_icon = "💡"
        else:
            rec_color = "#6366f1"
            rec_icon = "📌"
        
        st.markdown(f"""
        <div class='feature-card' style='padding: 1.25rem; margin-bottom: 1rem; border-left: 4px solid {rec_color};'>
            <div style='display: flex; align-items: start; gap: 1rem;'>
                <div style='font-size: 1.5rem; line-height: 1;'>{rec_icon}</div>
                <div style='flex: 1;'>
                    <div style='font-size: 1rem; color: rgba(255, 255, 255, 0.95); line-height: 1.6;'>
                        {recommendation}
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("")
    st.markdown("---")
    
    # Summary scores with improved layout
    st.markdown("### 📋 Quick Summary")
    st.markdown("")
    scores = feedback['scores']
    
    score_info = {
        'poor': {'emoji': '🔴', 'label': 'Poor', 'color': '#ef4444'},
        'fair': {'emoji': '🟡', 'label': 'Fair', 'color': '#f59e0b'},
        'good': {'emoji': '🟢', 'label': 'Good', 'color': '#10b981'},
        'excellent': {'emoji': '🟢', 'label': 'Excellent', 'color': '#10b981'},
        'low': {'emoji': '🟡', 'label': 'Low', 'color': '#f59e0b'},
        'moderate': {'emoji': '🟡', 'label': 'Moderate', 'color': '#f59e0b'},
        'excessive': {'emoji': '🔴', 'label': 'Excessive', 'color': '#ef4444'},
        'stationary': {'emoji': '🟡', 'label': 'Stationary', 'color': '#f59e0b'},
        'appropriate': {'emoji': '🟢', 'label': 'Appropriate', 'color': '#10b981'},
        'needs_improvement': {'emoji': '🔴', 'label': 'Needs Work', 'color': '#ef4444'}
    }
    
    # First row
    col1, col2, col3, col4, col5 = st.columns(5)
    
    metrics_row1 = [
        ('Posture', scores.get('posture', 'good')),
        ('Gestures', scores.get('gestures', 'good')),
        ('Eye Contact', scores.get('eye_contact', 'good')),
        ('Expressions', scores.get('facial_expressions', 'good')),
        ('Movement', scores.get('movement', 'good'))
    ]
    
    for col, (metric_name, score_key) in zip([col1, col2, col3, col4, col5], metrics_row1):
        score_data = score_info.get(score_key, {'emoji': '⚪', 'label': 'N/A', 'color': '#6b7280'})
        with col:
            st.markdown(f"""
            <div style='text-align: center; padding: 1rem; background: rgba(42, 0, 64, 0.4); border-radius: 0.75rem; border: 1px solid rgba(74, 0, 100, 0.4);'>
                <div style='font-size: 0.875rem; color: rgba(255, 255, 255, 0.6); margin-bottom: 0.5rem;'>{metric_name}</div>
                <div style='font-size: 2rem; margin-bottom: 0.25rem;'>{score_data['emoji']}</div>
                <div style='font-size: 1rem; color: {score_data["color"]}; font-weight: 600;'>{score_data['label']}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("")
    
    # Overall presence (centered)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        overall_score = scores.get('overall', 'good')
        overall_data = score_info.get(overall_score, {'emoji': '⚪', 'label': 'N/A', 'color': '#6b7280'})
        st.markdown(f"""
        <div style='text-align: center; padding: 1.5rem; background: rgba(42, 0, 64, 0.5); border-radius: 1rem; border: 2px solid rgba(74, 0, 100, 0.6);'>
            <div style='font-size: 1rem; color: rgba(255, 255, 255, 0.7); margin-bottom: 0.75rem; font-weight: 600;'>OVERALL PRESENCE</div>
            <div style='font-size: 3rem; margin-bottom: 0.5rem;'>{overall_data['emoji']}</div>
            <div style='font-size: 1.25rem; color: {overall_data["color"]}; font-weight: 700;'>{overall_data['label'].replace('_', ' ').title()}</div>
        </div>
        """, unsafe_allow_html=True)
