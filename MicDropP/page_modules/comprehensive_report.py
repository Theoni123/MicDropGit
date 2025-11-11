"""
Comprehensive Report Page
Combines all analyses into a single comprehensive report
"""

import streamlit as st
import plotly.graph_objects as go
import numpy as np
from utils.audio_processor import (
    load_audio, transcribe_audio, calculate_pace,
    detect_pauses, analyze_pitch, analyze_volume
)
from utils.language_analyzer import analyze_language
from utils.feedback_generator import (
    generate_voice_feedback, generate_language_feedback, generate_body_language_feedback
)

# Check for video processing dependencies
try:
    import cv2
    import mediapipe as mp
    HAS_VIDEO_DEPS = True
except ImportError:
    HAS_VIDEO_DEPS = False

if HAS_VIDEO_DEPS:
    from utils.video_processor import process_video


def extract_audio_from_video(video_file):
    """
    Extract audio from video file for voice/language analysis
    
    Args:
        video_file: Uploaded video file
    
    Returns:
        AudioSegment object that can be used like an audio file
    """
    from pydub import AudioSegment
    import tempfile
    import os
    
    tmp_path = None
    try:
        # Save video to temp file
        if hasattr(video_file, 'read'):
            video_bytes = video_file.read()
            video_file.seek(0)  # Reset for video processing
            
            file_ext = os.path.splitext(video_file.name)[1] if hasattr(video_file, 'name') else '.mp4'
            if not file_ext:
                file_ext = '.mp4'
            
            with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as tmp_file:
                tmp_file.write(video_bytes)
                tmp_path = tmp_file.name
        else:
            tmp_path = video_file
        
        # Extract audio using pydub
        audio = AudioSegment.from_file(tmp_path)
        
        return audio
        
    except Exception as e:
        raise Exception(f"Error extracting audio from video: {str(e)}")
    finally:
        # Clean up temp file
        if tmp_path and hasattr(video_file, 'read') and os.path.exists(tmp_path):
            try:
                os.unlink(tmp_path)
            except:
                pass


def calculate_overall_score(voice_metrics, language_metrics, body_metrics):
    """
    Calculate overall speaking score from all three analyses
    
    Args:
        voice_metrics: Voice analysis metrics
        language_metrics: Language analysis metrics
        body_metrics: Body language metrics
    
    Returns:
        Dictionary with overall scores
    """
    scores = {
        'voice_score': 0.0,
        'language_score': 0.0,
        'body_score': 0.0,
        'overall_score': 0.0
    }
    
    # Voice score (0-100)
    voice_feedback = generate_voice_feedback(voice_metrics)
    voice_scores = voice_feedback['scores']
    
    pace_score = 1.0 if voice_scores.get('pace') == 'good' else 0.5
    pause_score = 1.0 if voice_scores.get('pauses') == 'good' else 0.5
    pitch_score = 1.0 if voice_scores.get('pitch') in ['good', 'varied'] else 0.3
    volume_score = 1.0 if voice_scores.get('volume') == 'consistent' else 0.5
    
    scores['voice_score'] = (pace_score * 0.3 + pause_score * 0.2 + 
                            pitch_score * 0.3 + volume_score * 0.2) * 100
    
    # Language score (0-100)
    language_feedback = generate_language_feedback(language_metrics)
    lang_scores = language_feedback['scores']
    
    filler_score = 1.0 if lang_scores.get('filler_words') == 'low' else (0.5 if lang_scores.get('filler_words') == 'moderate' else 0.2)
    vocab_score = 1.0 if lang_scores.get('vocabulary') in ['good', 'high'] else 0.5
    readability_score = 1.0 if lang_scores.get('readability') in ['easy', 'moderate'] else 0.5
    structure_score = 1.0 if lang_scores.get('sentence_structure') == 'good' else 0.5
    tone_score = 1.0 if lang_scores.get('tone') == 'engaging' else 0.5
    
    scores['language_score'] = (filler_score * 0.3 + vocab_score * 0.2 + 
                                readability_score * 0.2 + structure_score * 0.15 + 
                                tone_score * 0.15) * 100
    
    # Body language score (0-100)
    if body_metrics:
        body_feedback = generate_body_language_feedback(body_metrics)
        body_scores = body_feedback['scores']
        
        posture_score = 1.0 if body_scores.get('posture') == 'good' else (0.5 if body_scores.get('posture') == 'fair' else 0.2)
        gesture_score = 1.0 if body_scores.get('gestures') == 'good' else (0.5 if body_scores.get('gestures') == 'low' else 0.3)
        eye_score = 1.0 if body_scores.get('eye_contact') == 'good' else (0.5 if body_scores.get('eye_contact') == 'fair' else 0.2)
        expression_score = 1.0 if body_scores.get('facial_expressions') == 'good' else (0.5 if body_scores.get('facial_expressions') == 'moderate' else 0.2)
        movement_score = 1.0 if body_scores.get('movement') == 'appropriate' else 0.5
        
        scores['body_score'] = (posture_score * 0.25 + gesture_score * 0.2 + 
                              eye_score * 0.25 + expression_score * 0.15 + 
                              movement_score * 0.15) * 100
    else:
        scores['body_score'] = 0.0
    
    # Overall score (weighted average)
    if scores['body_score'] > 0:
        # All three analyses available
        scores['overall_score'] = (scores['voice_score'] * 0.35 + 
                                  scores['language_score'] * 0.35 + 
                                  scores['body_score'] * 0.30)
    else:
        # Only voice and language (audio-only)
        scores['overall_score'] = (scores['voice_score'] * 0.5 + 
                                  scores['language_score'] * 0.5)
    
    return scores


def show():
    """Display comprehensive report page"""
    
    st.markdown("""
    <h1 style='display: flex; align-items: center; gap: 0.75rem; color: #ffffff;'>
        <svg style="width: 2rem; height: 2rem; fill: currentColor;" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zM9 17H7v-7h2v7zm4 0h-2V7h2v10zm4 0h-2v-4h2v4z" fill="currentColor"/>
        </svg>
        Comprehensive Report
    </h1>
    """, unsafe_allow_html=True)
    st.markdown("Get a complete analysis combining voice, language, and body language from a single upload")
    
    # Tips for best results
    with st.expander("💡 Tips for Best Results", expanded=False):
        st.markdown("""
        **For Video Uploads (Full Analysis):**
        - **Video Quality**: Ensure good lighting so your face and body are clearly visible
        - **Full Body View**: Keep your full body visible in the frame for best analysis
        - **Lighting**: Use natural or bright lighting - avoid backlighting or shadows
        - **Audio Quality**: Use a quiet environment with minimal background noise
        - **Format**: MP4, WebM, MOV, or AVI formats are supported
        
        **For Audio Uploads (Voice & Language Only):**
        - **Audio Quality**: Use a quiet environment with minimal background noise
        - **Speak Clearly**: Enunciate your words and speak at a natural pace
        - **Format**: MP3, WAV, M4A, OGG, or FLAC formats are supported
        
        **General:**
        - **Duration**: 30 seconds to 5 minutes works best for analysis
        """)
    
    # Check if video dependencies are available
    if not HAS_VIDEO_DEPS:
        st.warning("⚠️ **Video processing dependencies not available.** Body language analysis will be skipped. Install with: `pip install opencv-python mediapipe`")
    
    # File upload section
    st.header("Upload Video or Audio")
    
    uploaded_file = st.file_uploader(
        "Choose a video or audio file",
        type=['mp4', 'webm', 'mov', 'avi', 'mp3', 'wav', 'm4a', 'ogg', 'flac'],
        help="For comprehensive analysis, upload a video file. Audio files will provide voice and language analysis only."
    )
    
    if uploaded_file is not None:
        # Determine file type
        file_ext = uploaded_file.name.split('.')[-1].lower() if hasattr(uploaded_file, 'name') else ''
        is_video = file_ext in ['mp4', 'webm', 'mov', 'avi']
        is_audio = file_ext in ['mp3', 'wav', 'm4a', 'ogg', 'flac']
        
        if not is_video and not is_audio:
            st.error("❌ Unsupported file format. Please upload a video (MP4, WebM, MOV, AVI) or audio (MP3, WAV, M4A, OGG, FLAC) file.")
            return
        
        # Processing options
        with st.sidebar:
            st.header("Processing Options")
            if is_video and HAS_VIDEO_DEPS:
                max_frames = st.slider(
                    "Max frames to process",
                    min_value=10,
                    max_value=200,
                    value=100,
                    help="Lower values = faster processing, less detailed analysis"
                )
            else:
                max_frames = None
        
        # Process file
        with st.spinner("🔄 Processing comprehensive analysis... This may take a moment."):
            try:
                # Initialize results
                voice_metrics = None
                language_metrics = None
                body_metrics = None
                text = None
                
                # Progress tracking
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # Step 1: Extract audio and process voice/language
                status_text.text("📢 Step 1/3: Analyzing voice and language...")
                progress_bar.progress(20)
                
                try:
                    # Reset file pointer before processing
                    uploaded_file.seek(0)
                    
                    # Load audio (works for both audio and video files)
                    y, sr = load_audio(uploaded_file)
                    duration = len(y) / sr
                    
                    # Reset file pointer before transcription
                    uploaded_file.seek(0)
                    
                    # Transcribe
                    status_text.text("📝 Transcribing speech...")
                    progress_bar.progress(30)
                    text = transcribe_audio(uploaded_file)
                    
                    if text and text != "Could not understand audio" and not text.startswith("Error"):
                        st.success(f"✅ Audio loaded successfully! Duration: {duration:.2f} seconds")
                        with st.expander("📄 View Transcribed Text"):
                            st.text_area("Transcription", text, height=100, label_visibility="collapsed")
                    else:
                        st.warning("⚠️ Could not transcribe audio. Analysis will continue with audio-only metrics.")
                        text = None
                    
                    # Calculate voice metrics
                    status_text.text("🎙️ Analyzing voice characteristics...")
                    progress_bar.progress(50)
                    
                    wpm, duration, _ = calculate_pace(uploaded_file, text if text else None)
                    pauses = detect_pauses(y, sr)
                    pause_count = len(pauses)
                    pause_durations = [end - start for start, end in pauses]
                    avg_pause_duration = np.mean(pause_durations) if pause_durations else 0
                    pitch_stats = analyze_pitch(y, sr)
                    volume_stats = analyze_volume(y, sr)
                    
                    voice_metrics = {
                        'pace': {'wpm': wpm, 'duration': duration},
                        'pauses': {
                            'count': pause_count,
                            'avg_duration': avg_pause_duration,
                            'pauses': pauses
                        },
                        'pitch': pitch_stats,
                        'volume': volume_stats
                    }
                    
                    # Analyze language
                    if text:
                        status_text.text("📝 Analyzing language...")
                        progress_bar.progress(70)
                        language_metrics = analyze_language(text)
                    else:
                        language_metrics = {
                            'filler_words': {},
                            'vocabulary': {},
                            'readability': {},
                            'sentence_structure': {},
                            'repetition': {},
                            'tone': {},
                            'grammar': {}
                        }
                    
                except Exception as e:
                    st.error(f"❌ Error processing audio: {str(e)}")
                    st.exception(e)
                    return
                
                # Step 2: Process video for body language (if video file)
                if is_video and HAS_VIDEO_DEPS:
                    status_text.text("👤 Step 2/3: Analyzing body language...")
                    progress_bar.progress(80)
                    
                    try:
                        # Reset file pointer before video processing
                        uploaded_file.seek(0)
                        body_metrics = process_video(uploaded_file, max_frames=max_frames)
                        st.success(f"✅ Video processed! Frames analyzed: {body_metrics.get('frames_processed', 0)}")
                    except Exception as e:
                        st.warning(f"⚠️ Could not process video for body language analysis: {str(e)}")
                        body_metrics = None
                else:
                    body_metrics = None
                    if is_video:
                        st.info("ℹ️ Body language analysis skipped (dependencies not available or audio-only file)")
                
                # Step 3: Generate comprehensive report
                status_text.text("📊 Step 3/3: Generating comprehensive report...")
                progress_bar.progress(95)
                
                # Calculate overall scores
                overall_scores = calculate_overall_score(voice_metrics, language_metrics, body_metrics)
                
                progress_bar.progress(100)
                status_text.text("✅ Analysis complete!")
                
                # Display comprehensive results
                display_comprehensive_results(
                    voice_metrics, language_metrics, body_metrics, 
                    overall_scores, text, y, sr
                )
                
            except Exception as e:
                st.error(f"❌ Error processing file: {str(e)}")
                st.exception(e)


def display_comprehensive_results(voice_metrics, language_metrics, body_metrics, 
                                 overall_scores, text, y, sr):
    """Display comprehensive analysis results"""
    
    st.header("📊 Comprehensive Analysis Results")
    
    # Overall Score Section
    st.subheader("🎯 Overall Speaking Score")
    
    overall_score = overall_scores['overall_score']
    
    # Score interpretation
    if overall_score >= 80:
        score_label = "Excellent"
        score_color = "green"
        score_emoji = "🌟"
    elif overall_score >= 65:
        score_label = "Good"
        score_color = "blue"
        score_emoji = "👍"
    elif overall_score >= 50:
        score_label = "Fair"
        score_color = "orange"
        score_emoji = "📊"
    else:
        score_label = "Needs Improvement"
        score_color = "red"
        score_emoji = "📈"
    
    # Overall score gauge
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        fig_overall = go.Figure()
        fig_overall.add_trace(go.Indicator(
            mode="gauge+number+delta",
            value=overall_score,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': f"{score_emoji} Overall Score"},
            delta={'reference': 70},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': score_color},
                'steps': [
                    {'range': [0, 50], 'color': "lightgray"},
                    {'range': [50, 65], 'color': "gray"},
                    {'range': [65, 80], 'color': "lightblue"},
                    {'range': [80, 100], 'color': "lightgreen"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 70
                }
            }
        ))
        fig_overall.update_layout(height=300)
        st.plotly_chart(fig_overall, use_container_width=True)
        
        st.markdown(f"### {score_label} ({overall_score:.1f}/100)")
    
    # Component Scores
    st.subheader("📈 Component Scores")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("🎙️ Voice Score", f"{overall_scores['voice_score']:.1f}/100",
                 delta=f"{overall_scores['voice_score'] - 70:.1f}" if overall_scores['voice_score'] != 70 else None)
    
    with col2:
        st.metric("📝 Language Score", f"{overall_scores['language_score']:.1f}/100",
                 delta=f"{overall_scores['language_score'] - 70:.1f}" if overall_scores['language_score'] != 70 else None)
    
    with col3:
        if body_metrics:
            st.metric("👤 Body Language Score", f"{overall_scores['body_score']:.1f}/100",
                     delta=f"{overall_scores['body_score'] - 70:.1f}" if overall_scores['body_score'] != 70 else None)
        else:
            st.metric("👤 Body Language Score", "N/A", 
                     delta="Video required", delta_color="off")
    
    # Detailed Analysis Sections
    st.header("🔍 Detailed Analysis")
    
    # Voice Analysis Section
    with st.expander("🎙️ Voice Analysis Details", expanded=True):
        voice_feedback = generate_voice_feedback(voice_metrics)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Pace", f"{voice_metrics['pace']['wpm']:.0f} WPM")
        with col2:
            st.metric("Pauses", f"{voice_metrics['pauses']['count']}")
        with col3:
            monotony = voice_metrics['pitch']['monotony_score']
            st.metric("Pitch Variation", "Varied" if monotony < 0.3 else "Monotone")
        with col4:
            consistency = voice_metrics['volume']['volume_consistency']
            st.metric("Volume", "Consistent" if consistency > 0.5 else "Variable")
        
        st.markdown("**Key Recommendations:**")
        for i, rec in enumerate(voice_feedback['recommendations'][:3], 1):
            st.markdown(f"{i}. {rec}")
    
    # Language Analysis Section
    if text:
        with st.expander("📝 Language Analysis Details", expanded=True):
            language_feedback = generate_language_feedback(language_metrics)
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                filler_rate = language_metrics.get('filler_words', {}).get('filler_rate', 0.0)
                st.metric("Filler Words", f"{filler_rate:.1f}/100 words")
            with col2:
                diversity = language_metrics.get('vocabulary', {}).get('diversity_ratio', 0.0)
                st.metric("Vocab Diversity", f"{diversity*100:.1f}%")
            with col3:
                flesch = language_metrics.get('readability', {}).get('flesch_reading_ease', 0)
                if flesch > 0:
                    st.metric("Readability", f"{flesch:.0f}")
                else:
                    st.metric("Readability", "N/A")
            with col4:
                avg_sentence = language_metrics.get('sentence_structure', {}).get('avg_words_per_sentence', 0)
                st.metric("Avg Sentence", f"{avg_sentence:.1f} words")
            
            st.markdown("**Key Recommendations:**")
            for i, rec in enumerate(language_feedback['recommendations'][:3], 1):
                st.markdown(f"{i}. {rec}")
    
    # Body Language Analysis Section
    if body_metrics:
        with st.expander("👤 Body Language Analysis Details", expanded=True):
            body_feedback = generate_body_language_feedback(body_metrics)
            
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                posture_score = body_metrics.get('posture', {}).get('posture_score', 0.0)
                st.metric("Posture", f"{posture_score*100:.0f}%")
            with col2:
                gesture_freq = body_metrics.get('gestures', {}).get('gesture_frequency', 0.0)
                st.metric("Gestures", f"{gesture_freq:.1f}/sec")
            with col3:
                eye_contact = body_metrics.get('eye_contact', {}).get('eye_contact_percentage', 0.0)
                st.metric("Eye Contact", f"{eye_contact*100:.0f}%")
            with col4:
                engagement = body_metrics.get('facial_expressions', {}).get('engagement_score', 0.0)
                st.metric("Engagement", f"{engagement*100:.0f}%")
            with col5:
                presence = body_metrics.get('presence_score', 0.0)
                st.metric("Presence", f"{presence*100:.0f}%")
            
            st.markdown("**Key Recommendations:**")
            for i, rec in enumerate(body_feedback['recommendations'][:3], 1):
                st.markdown(f"{i}. {rec}")
    else:
        with st.expander("👤 Body Language Analysis Details"):
            st.info("Body language analysis requires a video file with MediaPipe dependencies installed.")
    
    # Combined Recommendations
    st.header("💡 Comprehensive Recommendations")
    
    all_recommendations = []
    
    # Collect all recommendations
    voice_feedback = generate_voice_feedback(voice_metrics)
    all_recommendations.extend([("🎙️ Voice", rec) for rec in voice_feedback['recommendations']])
    
    if text:
        language_feedback = generate_language_feedback(language_metrics)
        all_recommendations.extend([("📝 Language", rec) for rec in language_feedback['recommendations']])
    
    if body_metrics:
        body_feedback = generate_body_language_feedback(body_metrics)
        all_recommendations.extend([("👤 Body Language", rec) for rec in body_feedback['recommendations']])
    
    # Display top recommendations
    st.markdown("### Top Priority Actions")
    for i, (category, rec) in enumerate(all_recommendations[:5], 1):
        st.info(f"**{category}:** {rec}")
    
    if len(all_recommendations) > 5:
        with st.expander(f"View all {len(all_recommendations)} recommendations"):
            for i, (category, rec) in enumerate(all_recommendations[5:], 6):
                st.markdown(f"{i}. **{category}:** {rec}")
    
    # Summary Table
    st.header("📋 Summary")
    
    summary_data = {
        'Category': ['Overall Score', 'Voice', 'Language', 'Body Language'],
        'Score': [
            f"{overall_scores['overall_score']:.1f}/100",
            f"{overall_scores['voice_score']:.1f}/100",
            f"{overall_scores['language_score']:.1f}/100",
            f"{overall_scores['body_score']:.1f}/100" if body_metrics else "N/A"
        ],
        'Status': [
            score_label,
            "Good" if overall_scores['voice_score'] >= 70 else "Needs Work",
            "Good" if overall_scores['language_score'] >= 70 else "Needs Work",
            "Good" if body_metrics and overall_scores['body_score'] >= 70 else ("N/A" if not body_metrics else "Needs Work")
        ]
    }
    
    import pandas as pd
    df = pd.DataFrame(summary_data)
    st.dataframe(df, use_container_width=True, hide_index=True)
