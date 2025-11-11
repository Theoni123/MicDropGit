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
            <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z" fill="currentColor"/>
        </svg>
        AI Coach
    </h1>
    """, unsafe_allow_html=True)
    st.markdown("**Your complete speaking coach** - Get comprehensive analysis of voice, language, and body language with personalized recommendations from a single upload.")
    
    # Tips for best results
    with st.expander("Tips for Best Results", expanded=False):
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
    
    st.markdown("""
    <h2 style='color: #ffffff; margin-top: 2rem; margin-bottom: 1.5rem;'>
        📊 Comprehensive Analysis Results
    </h2>
    """, unsafe_allow_html=True)
    
    # Overall Score Section
    overall_score = overall_scores['overall_score']
    
    # Score interpretation
    if overall_score >= 80:
        score_label = "Excellent"
        score_color = "#10b981"
        score_emoji = "🌟"
        gradient = "linear-gradient(135deg, rgba(16, 185, 129, 0.2), rgba(5, 150, 105, 0.3))"
    elif overall_score >= 65:
        score_label = "Good"
        score_color = "#3b82f6"
        score_emoji = "👍"
        gradient = "linear-gradient(135deg, rgba(59, 130, 246, 0.2), rgba(37, 99, 235, 0.3))"
    elif overall_score >= 50:
        score_label = "Fair"
        score_color = "#f59e0b"
        score_emoji = "📊"
        gradient = "linear-gradient(135deg, rgba(245, 158, 11, 0.2), rgba(217, 119, 6, 0.3))"
    else:
        score_label = "Needs Improvement"
        score_color = "#ef4444"
        score_emoji = "📈"
        gradient = "linear-gradient(135deg, rgba(239, 68, 68, 0.2), rgba(220, 38, 38, 0.3))"
    
    # Overall score card
    st.markdown(f"""
    <div style='
        background: {gradient};
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 2rem;
        margin: 1.5rem 0;
        text-align: center;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    '>
        <div style='font-size: 4rem; margin-bottom: 0.5rem;'>{score_emoji}</div>
        <div style='font-size: 3rem; font-weight: bold; color: {score_color}; margin-bottom: 0.5rem;'>
            {overall_score:.1f}
        </div>
        <div style='font-size: 1.5rem; color: white; margin-bottom: 0.5rem;'>Overall Score</div>
        <div style='font-size: 1.2rem; color: rgba(255, 255, 255, 0.8);'>{score_label}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Component Scores with modern cards
    st.markdown("""
    <h3 style='color: #ffffff; margin-top: 2rem; margin-bottom: 1rem;'>
        📈 Component Scores
    </h3>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    def get_score_color(score):
        if score >= 80:
            return "#10b981", "rgba(16, 185, 129, 0.15)"
        elif score >= 65:
            return "#3b82f6", "rgba(59, 130, 246, 0.15)"
        elif score >= 50:
            return "#f59e0b", "rgba(245, 158, 11, 0.15)"
        else:
            return "#ef4444", "rgba(239, 68, 68, 0.15)"
    
    with col1:
        voice_color, voice_bg = get_score_color(overall_scores['voice_score'])
        st.markdown(f"""
        <div style='
            background: linear-gradient(135deg, {voice_bg}, rgba(42, 0, 64, 0.3));
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-left: 4px solid {voice_color};
            border-radius: 15px;
            padding: 1.5rem;
            text-align: center;
            box-shadow: 0 4px 16px 0 rgba(0, 0, 0, 0.25);
        '>
            <div style='font-size: 2rem; margin-bottom: 0.5rem;'>🎙️</div>
            <div style='font-size: 1.8rem; font-weight: bold; color: {voice_color};'>
                {overall_scores['voice_score']:.1f}
            </div>
            <div style='color: white; font-size: 0.9rem; margin-top: 0.3rem;'>Voice Score</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        lang_color, lang_bg = get_score_color(overall_scores['language_score'])
        st.markdown(f"""
        <div style='
            background: linear-gradient(135deg, {lang_bg}, rgba(42, 0, 64, 0.3));
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-left: 4px solid {lang_color};
            border-radius: 15px;
            padding: 1.5rem;
            text-align: center;
            box-shadow: 0 4px 16px 0 rgba(0, 0, 0, 0.25);
        '>
            <div style='font-size: 2rem; margin-bottom: 0.5rem;'>📝</div>
            <div style='font-size: 1.8rem; font-weight: bold; color: {lang_color};'>
                {overall_scores['language_score']:.1f}
            </div>
            <div style='color: white; font-size: 0.9rem; margin-top: 0.3rem;'>Language Score</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        if body_metrics:
            body_color, body_bg = get_score_color(overall_scores['body_score'])
            st.markdown(f"""
            <div style='
                background: linear-gradient(135deg, {body_bg}, rgba(42, 0, 64, 0.3));
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-left: 4px solid {body_color};
                border-radius: 15px;
                padding: 1.5rem;
                text-align: center;
                box-shadow: 0 4px 16px 0 rgba(0, 0, 0, 0.25);
            '>
                <div style='font-size: 2rem; margin-bottom: 0.5rem;'>👤</div>
                <div style='font-size: 1.8rem; font-weight: bold; color: {body_color};'>
                    {overall_scores['body_score']:.1f}
                </div>
                <div style='color: white; font-size: 0.9rem; margin-top: 0.3rem;'>Body Language Score</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style='
                background: linear-gradient(135deg, rgba(107, 114, 128, 0.15), rgba(42, 0, 64, 0.3));
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-left: 4px solid #6b7280;
                border-radius: 15px;
                padding: 1.5rem;
                text-align: center;
                box-shadow: 0 4px 16px 0 rgba(0, 0, 0, 0.25);
            '>
                <div style='font-size: 2rem; margin-bottom: 0.5rem;'>👤</div>
                <div style='font-size: 1.5rem; font-weight: bold; color: #6b7280;'>
                    N/A
                </div>
                <div style='color: white; font-size: 0.9rem; margin-top: 0.3rem;'>Body Language Score</div>
                <div style='color: rgba(255, 255, 255, 0.6); font-size: 0.8rem; margin-top: 0.3rem;'>Video required</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Detailed Analysis Sections
    st.markdown("""
    <h2 style='color: #ffffff; margin-top: 3rem; margin-bottom: 1.5rem;'>
        🔍 Detailed Analysis
    </h2>
    """, unsafe_allow_html=True)
    
    # Voice Analysis Section
    st.markdown("""
    <h3 style='color: #ffffff; margin-top: 2rem; margin-bottom: 1rem;'>
        🎙️ Voice Analysis
    </h3>
    """, unsafe_allow_html=True)
    
    voice_feedback = generate_voice_feedback(voice_metrics)
    
    # Voice metrics cards
    col1, col2, col3, col4 = st.columns(4)
    
    wpm = voice_metrics['pace']['wpm']
    if 120 <= wpm <= 160:
        pace_color = "#10b981"
        pace_status = "✓ Good"
    elif 100 <= wpm < 120 or 160 < wpm <= 180:
        pace_color = "#f59e0b"
        pace_status = "⚠ Adjust"
    else:
        pace_color = "#ef4444"
        pace_status = "✗ Review"
    
    with col1:
        st.markdown(f"""
        <div style='
            background: linear-gradient(135deg, rgba(42, 0, 64, 0.4), rgba(75, 0, 130, 0.3));
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-left: 4px solid {pace_color};
            border-radius: 15px;
            padding: 1.5rem;
            text-align: center;
            box-shadow: 0 4px 16px 0 rgba(0, 0, 0, 0.25);
        '>
            <div style='color: rgba(255, 255, 255, 0.7); font-size: 0.9rem; margin-bottom: 0.5rem;'>Pace</div>
            <div style='font-size: 2rem; font-weight: bold; color: {pace_color};'>{wpm:.0f}</div>
            <div style='color: white; font-size: 0.85rem; margin-top: 0.3rem;'>WPM</div>
            <div style='color: {pace_color}; font-size: 0.75rem; margin-top: 0.5rem;'>{pace_status}</div>
        </div>
        """, unsafe_allow_html=True)
    
    pause_count = voice_metrics['pauses']['count']
    avg_pause = voice_metrics['pauses']['avg_duration']
    if 5 <= pause_count <= 15 and avg_pause < 2.0:
        pause_color = "#10b981"
        pause_status = "✓ Good"
    elif pause_count < 5 or (pause_count <= 20 and avg_pause < 3.0):
        pause_color = "#f59e0b"
        pause_status = "⚠ Adjust"
    else:
        pause_color = "#ef4444"
        pause_status = "✗ Review"
    
    with col2:
        st.markdown(f"""
        <div style='
            background: linear-gradient(135deg, rgba(42, 0, 64, 0.4), rgba(75, 0, 130, 0.3));
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-left: 4px solid {pause_color};
            border-radius: 15px;
            padding: 1.5rem;
            text-align: center;
            box-shadow: 0 4px 16px 0 rgba(0, 0, 0, 0.25);
        '>
            <div style='color: rgba(255, 255, 255, 0.7); font-size: 0.9rem; margin-bottom: 0.5rem;'>Pauses</div>
            <div style='font-size: 2rem; font-weight: bold; color: {pause_color};'>{pause_count}</div>
            <div style='color: white; font-size: 0.85rem; margin-top: 0.3rem;'>{avg_pause:.1f}s avg</div>
            <div style='color: {pause_color}; font-size: 0.75rem; margin-top: 0.5rem;'>{pause_status}</div>
        </div>
        """, unsafe_allow_html=True)
    
    monotony = voice_metrics['pitch']['monotony_score']
    if monotony < 0.3:
        pitch_color = "#10b981"
        pitch_status = "✓ Varied"
    elif monotony < 0.5:
        pitch_color = "#f59e0b"
        pitch_status = "⚠ Somewhat"
    else:
        pitch_color = "#ef4444"
        pitch_status = "✗ Monotone"
    
    with col3:
        st.markdown(f"""
        <div style='
            background: linear-gradient(135deg, rgba(42, 0, 64, 0.4), rgba(75, 0, 130, 0.3));
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-left: 4px solid {pitch_color};
            border-radius: 15px;
            padding: 1.5rem;
            text-align: center;
            box-shadow: 0 4px 16px 0 rgba(0, 0, 0, 0.25);
        '>
            <div style='color: rgba(255, 255, 255, 0.7); font-size: 0.9rem; margin-bottom: 0.5rem;'>Pitch</div>
            <div style='font-size: 2rem; font-weight: bold; color: {pitch_color};'>{(1-monotony)*100:.0f}</div>
            <div style='color: white; font-size: 0.85rem; margin-top: 0.3rem;'>Variation %</div>
            <div style='color: {pitch_color}; font-size: 0.75rem; margin-top: 0.5rem;'>{pitch_status}</div>
        </div>
        """, unsafe_allow_html=True)
    
    consistency = voice_metrics['volume']['volume_consistency']
    if consistency > 0.5:
        volume_color = "#10b981"
        volume_status = "✓ Consistent"
    elif consistency > 0.3:
        volume_color = "#f59e0b"
        volume_status = "⚠ Variable"
    else:
        volume_color = "#ef4444"
        volume_status = "✗ Inconsistent"
    
    with col4:
        st.markdown(f"""
        <div style='
            background: linear-gradient(135deg, rgba(42, 0, 64, 0.4), rgba(75, 0, 130, 0.3));
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-left: 4px solid {volume_color};
            border-radius: 15px;
            padding: 1.5rem;
            text-align: center;
            box-shadow: 0 4px 16px 0 rgba(0, 0, 0, 0.25);
        '>
            <div style='color: rgba(255, 255, 255, 0.7); font-size: 0.9rem; margin-bottom: 0.5rem;'>Volume</div>
            <div style='font-size: 2rem; font-weight: bold; color: {volume_color};'>{consistency*100:.0f}</div>
            <div style='color: white; font-size: 0.85rem; margin-top: 0.3rem;'>Consistency %</div>
            <div style='color: {volume_color}; font-size: 0.75rem; margin-top: 0.5rem;'>{volume_status}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Voice visualizations
    st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)
    
    # Pace gauge
    fig_pace = go.Figure()
    fig_pace.add_trace(go.Indicator(
        mode="gauge+number",
        value=wpm,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Speaking Pace (WPM)", 'font': {'color': 'white', 'size': 16}},
        number={'font': {'color': 'white', 'size': 32}},
        gauge={
            'axis': {
                'range': [None, 200], 
                'tickcolor': 'white',
                'tickfont': {'color': 'white'}
            },
            'bar': {'color': pace_color},
            'bgcolor': 'rgba(42, 0, 64, 0.3)',
            'bordercolor': 'rgba(255, 255, 255, 0.1)',
            'steps': [
                {'range': [0, 100], 'color': 'rgba(239, 68, 68, 0.3)'},
                {'range': [100, 120], 'color': 'rgba(245, 158, 11, 0.3)'},
                {'range': [120, 160], 'color': 'rgba(16, 185, 129, 0.3)'},
                {'range': [160, 180], 'color': 'rgba(245, 158, 11, 0.3)'},
                {'range': [180, 200], 'color': 'rgba(239, 68, 68, 0.3)'}
            ],
        }
    ))
    fig_pace.update_layout(
        height=250,
        paper_bgcolor='rgba(0,0,0,0)',
        font={'color': 'white', 'size': 12}
    )
    st.plotly_chart(fig_pace, use_container_width=True)
    
    # Pauses over time
    if voice_metrics['pauses']['pauses']:
        pauses = voice_metrics['pauses']['pauses']
        fig_pauses = go.Figure()
        fig_pauses.add_trace(go.Scatter(
            x=[p[0] for p in pauses],
            y=[p[1] - p[0] for p in pauses],
            mode='markers',
            marker=dict(size=10, color=pause_color, line=dict(width=1, color='white')),
            name='Pauses'
        ))
        fig_pauses.update_layout(
            title={'text': "Pauses Over Time", 'font': {'color': 'white', 'size': 16}},
            xaxis_title="Time (seconds)",
            yaxis_title="Pause Duration (seconds)",
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
        st.plotly_chart(fig_pauses, use_container_width=True)
    
    # Pitch analysis
    pitch_data = voice_metrics['pitch']
    col1, col2 = st.columns(2)
    
    with col1:
        pitch_values = pitch_data.get('pitch_values', [])
        if len(pitch_values) > 0:
            times = np.linspace(0, len(y) / sr, len(pitch_values))
            fig_pitch = go.Figure()
            fig_pitch.add_trace(go.Scatter(
                x=times,
                y=pitch_values,
                mode='lines',
                line=dict(color=pitch_color, width=2),
                fill='tozeroy',
                fillcolor=f'rgba{tuple(list(int(pitch_color[i:i+2], 16) for i in (1, 3, 5)) + [0.3])}',
                name='Pitch'
            ))
        else:
            # Fallback if no pitch data
            fig_pitch = go.Figure()
            fig_pitch.add_annotation(
                text="Pitch data not available",
                xref="paper", yref="paper",
                x=0.5, y=0.5,
                showarrow=False,
                font=dict(color='white', size=14)
            )
        fig_pitch.update_layout(
            title={'text': "Pitch Variation", 'font': {'color': 'white', 'size': 16}},
            xaxis_title="Time",
            yaxis_title="Pitch (Hz)",
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
        st.plotly_chart(fig_pitch, use_container_width=True)
    
    with col2:
        # Volume analysis
        volume_data = voice_metrics['volume']
        rms_db = volume_data.get('rms_db', [])
        if len(rms_db) > 0:
            times = np.linspace(0, len(y) / sr, len(rms_db))
            fig_volume = go.Figure()
            fig_volume.add_trace(go.Scatter(
                x=times,
                y=rms_db,
                mode='lines',
                line=dict(color=volume_color, width=2),
                fill='tozeroy',
                fillcolor=f'rgba{tuple(list(int(volume_color[i:i+2], 16) for i in (1, 3, 5)) + [0.3])}',
                name='Volume'
            ))
        else:
            # Fallback if no volume data
            fig_volume = go.Figure()
            fig_volume.add_annotation(
                text="Volume data not available",
                xref="paper", yref="paper",
                x=0.5, y=0.5,
                showarrow=False,
                font=dict(color='white', size=14)
            )
        fig_volume.update_layout(
            title={'text': "Volume Levels", 'font': {'color': 'white', 'size': 16}},
            xaxis_title="Time",
            yaxis_title="Volume (dB)",
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
        st.plotly_chart(fig_volume, use_container_width=True)
    
    # Voice feedback
    st.markdown("""
    <h4 style='color: #ffffff; margin-top: 1.5rem; margin-bottom: 1rem;'>
        💡 Voice Recommendations
    </h4>
    """, unsafe_allow_html=True)
    
    for i, rec in enumerate(voice_feedback['recommendations'], 1):
        st.markdown(f"""
        <div style='
            background: linear-gradient(135deg, rgba(59, 130, 246, 0.1), rgba(42, 0, 64, 0.3));
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-left: 3px solid #3b82f6;
            border-radius: 10px;
            padding: 1rem;
            margin-bottom: 0.75rem;
            color: white;
        '>
            <strong>{i}.</strong> {rec}
        </div>
        """, unsafe_allow_html=True)
    
    # Language Analysis Section
    if text:
        st.markdown("""
        <h3 style='color: #ffffff; margin-top: 2.5rem; margin-bottom: 1rem;'>
            📝 Language Analysis
        </h3>
        """, unsafe_allow_html=True)
        
        language_feedback = generate_language_feedback(language_metrics)
        
        # Language metrics cards
        col1, col2, col3, col4 = st.columns(4)
        
        filler_rate = language_metrics.get('filler_words', {}).get('filler_rate', 0.0)
        if filler_rate < 2:
            filler_color = "#10b981"
            filler_status = "✓ Excellent"
        elif filler_rate < 5:
            filler_color = "#f59e0b"
            filler_status = "⚠ Moderate"
        else:
            filler_color = "#ef4444"
            filler_status = "✗ High"
        
        with col1:
            st.markdown(f"""
            <div style='
                background: linear-gradient(135deg, rgba(42, 0, 64, 0.4), rgba(75, 0, 130, 0.3));
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-left: 4px solid {filler_color};
                border-radius: 15px;
                padding: 1.5rem;
                text-align: center;
                box-shadow: 0 4px 16px 0 rgba(0, 0, 0, 0.25);
            '>
                <div style='color: rgba(255, 255, 255, 0.7); font-size: 0.9rem; margin-bottom: 0.5rem;'>Filler Words</div>
                <div style='font-size: 2rem; font-weight: bold; color: {filler_color};'>{filler_rate:.1f}</div>
                <div style='color: white; font-size: 0.85rem; margin-top: 0.3rem;'>per 100 words</div>
                <div style='color: {filler_color}; font-size: 0.75rem; margin-top: 0.5rem;'>{filler_status}</div>
            </div>
            """, unsafe_allow_html=True)
        
        diversity = language_metrics.get('vocabulary', {}).get('diversity_ratio', 0.0)
        if diversity >= 0.7:
            vocab_color = "#10b981"
            vocab_status = "✓ Excellent"
        elif diversity >= 0.5:
            vocab_color = "#f59e0b"
            vocab_status = "⚠ Good"
        else:
            vocab_color = "#ef4444"
            vocab_status = "✗ Limited"
        
        with col2:
            st.markdown(f"""
            <div style='
                background: linear-gradient(135deg, rgba(42, 0, 64, 0.4), rgba(75, 0, 130, 0.3));
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-left: 4px solid {vocab_color};
                border-radius: 15px;
                padding: 1.5rem;
                text-align: center;
                box-shadow: 0 4px 16px 0 rgba(0, 0, 0, 0.25);
            '>
                <div style='color: rgba(255, 255, 255, 0.7); font-size: 0.9rem; margin-bottom: 0.5rem;'>Vocabulary</div>
                <div style='font-size: 2rem; font-weight: bold; color: {vocab_color};'>{diversity*100:.0f}</div>
                <div style='color: white; font-size: 0.85rem; margin-top: 0.3rem;'>Diversity %</div>
                <div style='color: {vocab_color}; font-size: 0.75rem; margin-top: 0.5rem;'>{vocab_status}</div>
            </div>
            """, unsafe_allow_html=True)
        
        flesch = language_metrics.get('readability', {}).get('flesch_reading_ease', 0)
        if flesch >= 60:
            read_color = "#10b981"
            read_status = "✓ Easy"
        elif flesch >= 30:
            read_color = "#f59e0b"
            read_status = "⚠ Moderate"
        elif flesch > 0:
            read_color = "#ef4444"
            read_status = "✗ Difficult"
        else:
            read_color = "#6b7280"
            read_status = "N/A"
        
        with col3:
            st.markdown(f"""
            <div style='
                background: linear-gradient(135deg, rgba(42, 0, 64, 0.4), rgba(75, 0, 130, 0.3));
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-left: 4px solid {read_color};
                border-radius: 15px;
                padding: 1.5rem;
                text-align: center;
                box-shadow: 0 4px 16px 0 rgba(0, 0, 0, 0.25);
            '>
                <div style='color: rgba(255, 255, 255, 0.7); font-size: 0.9rem; margin-bottom: 0.5rem;'>Readability</div>
                <div style='font-size: 2rem; font-weight: bold; color: {read_color};'>{flesch if flesch > 0 else "—"}</div>
                <div style='color: white; font-size: 0.85rem; margin-top: 0.3rem;'>Flesch Score</div>
                <div style='color: {read_color}; font-size: 0.75rem; margin-top: 0.5rem;'>{read_status}</div>
            </div>
            """, unsafe_allow_html=True)
        
        avg_sentence = language_metrics.get('sentence_structure', {}).get('avg_words_per_sentence', 0)
        if 15 <= avg_sentence <= 25:
            sent_color = "#10b981"
            sent_status = "✓ Good"
        elif 10 <= avg_sentence < 15 or 25 < avg_sentence <= 35:
            sent_color = "#f59e0b"
            sent_status = "⚠ Adjust"
        else:
            sent_color = "#ef4444"
            sent_status = "✗ Review"
        
        with col4:
            st.markdown(f"""
            <div style='
                background: linear-gradient(135deg, rgba(42, 0, 64, 0.4), rgba(75, 0, 130, 0.3));
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-left: 4px solid {sent_color};
                border-radius: 15px;
                padding: 1.5rem;
                text-align: center;
                box-shadow: 0 4px 16px 0 rgba(0, 0, 0, 0.25);
            '>
                <div style='color: rgba(255, 255, 255, 0.7); font-size: 0.9rem; margin-bottom: 0.5rem;'>Sentence Length</div>
                <div style='font-size: 2rem; font-weight: bold; color: {sent_color};'>{avg_sentence:.0f}</div>
                <div style='color: white; font-size: 0.85rem; margin-top: 0.3rem;'>words avg</div>
                <div style='color: {sent_color}; font-size: 0.75rem; margin-top: 0.5rem;'>{sent_status}</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Language visualizations
        st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)
        
        # Filler words chart
        filler_words = language_metrics.get('filler_words', {}).get('filler_words', {})
        if filler_words:
            fig_fillers = go.Figure()
            fig_fillers.add_trace(go.Bar(
                x=list(filler_words.keys()),
                y=list(filler_words.values()),
                marker_color=filler_color,
                marker_line=dict(color='white', width=1)
            ))
            fig_fillers.update_layout(
                title={'text': "Filler Words Detected", 'font': {'color': 'white', 'size': 16}},
                xaxis_title="Filler Word",
                yaxis_title="Count",
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
            st.plotly_chart(fig_fillers, use_container_width=True)
        
        # Vocabulary diversity gauge
        fig_vocab = go.Figure()
        fig_vocab.add_trace(go.Indicator(
            mode="gauge+number",
            value=diversity * 100,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Vocabulary Diversity (%)", 'font': {'color': 'white', 'size': 16}},
            number={'font': {'color': 'white', 'size': 32}, 'suffix': '%'},
            gauge={
                'axis': {
                    'range': [None, 100], 
                    'tickcolor': 'white',
                    'tickfont': {'color': 'white'}
                },
                'bar': {'color': vocab_color},
                'bgcolor': 'rgba(42, 0, 64, 0.3)',
                'bordercolor': 'rgba(255, 255, 255, 0.1)',
                'steps': [
                    {'range': [0, 30], 'color': 'rgba(239, 68, 68, 0.3)'},
                    {'range': [30, 50], 'color': 'rgba(245, 158, 11, 0.3)'},
                    {'range': [50, 70], 'color': 'rgba(59, 130, 246, 0.3)'},
                    {'range': [70, 100], 'color': 'rgba(16, 185, 129, 0.3)'}
                ],
            }
        ))
        fig_vocab.update_layout(
            height=250,
            paper_bgcolor='rgba(0,0,0,0)',
            font={'color': 'white', 'size': 12}
        )
        st.plotly_chart(fig_vocab, use_container_width=True)
        
        # Readability metrics
        st.markdown("""
        <h4 style='color: #ffffff; margin-top: 1.5rem; margin-bottom: 1rem;'>
            📖 Readability Metrics
        </h4>
        """, unsafe_allow_html=True)
        
        readability = language_metrics.get('readability', {})
        col1, col2, col3 = st.columns(3)
        
        with col1:
            flesch_ease = readability.get('flesch_reading_ease', 0)
            flesch_display = f"{flesch_ease:.1f}" if flesch_ease > 0 else "—"
            st.markdown(f"""
            <div style='
                background: linear-gradient(135deg, rgba(59, 130, 246, 0.15), rgba(42, 0, 64, 0.3));
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 10px;
                padding: 1rem;
                text-align: center;
            '>
                <div style='color: #3b82f6; font-size: 1.5rem; font-weight: bold;'>
                    {flesch_display}
                </div>
                <div style='color: white; font-size: 0.85rem; margin-top: 0.3rem;'>Flesch Reading Ease</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            flesch_grade = readability.get('flesch_kincaid_grade', 0)
            grade_display = f"{flesch_grade:.1f}" if flesch_grade > 0 else "—"
            st.markdown(f"""
            <div style='
                background: linear-gradient(135deg, rgba(59, 130, 246, 0.15), rgba(42, 0, 64, 0.3));
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 10px;
                padding: 1rem;
                text-align: center;
            '>
                <div style='color: #3b82f6; font-size: 1.5rem; font-weight: bold;'>
                    {grade_display}
                </div>
                <div style='color: white; font-size: 0.85rem; margin-top: 0.3rem;'>Grade Level</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            syllables = readability.get('avg_syllables_per_word', 0)
            st.markdown(f"""
            <div style='
                background: linear-gradient(135deg, rgba(59, 130, 246, 0.15), rgba(42, 0, 64, 0.3));
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 10px;
                padding: 1rem;
                text-align: center;
            '>
                <div style='color: #3b82f6; font-size: 1.5rem; font-weight: bold;'>
                    {syllables:.2f}
                </div>
                <div style='color: white; font-size: 0.85rem; margin-top: 0.3rem;'>Avg Syllables/Word</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Language feedback
        st.markdown("""
        <h4 style='color: #ffffff; margin-top: 1.5rem; margin-bottom: 1rem;'>
            💡 Language Recommendations
        </h4>
        """, unsafe_allow_html=True)
        
        for i, rec in enumerate(language_feedback['recommendations'], 1):
            st.markdown(f"""
            <div style='
                background: linear-gradient(135deg, rgba(16, 185, 129, 0.1), rgba(42, 0, 64, 0.3));
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-left: 3px solid #10b981;
                border-radius: 10px;
                padding: 1rem;
                margin-bottom: 0.75rem;
                color: white;
            '>
                <strong>{i}.</strong> {rec}
            </div>
            """, unsafe_allow_html=True)
    
    # Body Language Analysis Section
    if body_metrics:
        st.markdown("""
        <h3 style='color: #ffffff; margin-top: 2.5rem; margin-bottom: 1rem;'>
            👤 Body Language Analysis
        </h3>
        """, unsafe_allow_html=True)
        
        body_feedback = generate_body_language_feedback(body_metrics)
        
        # Body language metrics cards
        col1, col2, col3, col4, col5 = st.columns(5)
        
        posture_score = body_metrics.get('posture', {}).get('posture_score', 0.0)
        if posture_score >= 0.75:
            posture_color = "#10b981"
            posture_status = "✓ Excellent"
        elif posture_score >= 0.5:
            posture_color = "#f59e0b"
            posture_status = "⚠ Fair"
        else:
            posture_color = "#ef4444"
            posture_status = "✗ Poor"
        
        with col1:
            st.markdown(f"""
            <div style='
                background: linear-gradient(135deg, rgba(42, 0, 64, 0.4), rgba(75, 0, 130, 0.3));
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-left: 4px solid {posture_color};
                border-radius: 15px;
                padding: 1.5rem;
                text-align: center;
                box-shadow: 0 4px 16px 0 rgba(0, 0, 0, 0.25);
            '>
                <div style='color: rgba(255, 255, 255, 0.7); font-size: 0.9rem; margin-bottom: 0.5rem;'>Posture</div>
                <div style='font-size: 2rem; font-weight: bold; color: {posture_color};'>{posture_score*100:.0f}</div>
                <div style='color: white; font-size: 0.85rem; margin-top: 0.3rem;'>Score %</div>
                <div style='color: {posture_color}; font-size: 0.75rem; margin-top: 0.5rem;'>{posture_status}</div>
            </div>
            """, unsafe_allow_html=True)
        
        gesture_freq = body_metrics.get('gestures', {}).get('gesture_frequency', 0.0)
        if 2 <= gesture_freq <= 8:
            gesture_color = "#10b981"
            gesture_status = "✓ Good"
        elif 1 <= gesture_freq < 2 or 8 < gesture_freq <= 12:
            gesture_color = "#f59e0b"
            gesture_status = "⚠ Adjust"
        else:
            gesture_color = "#ef4444"
            gesture_status = "✗ Review"
        
        with col2:
            st.markdown(f"""
            <div style='
                background: linear-gradient(135deg, rgba(42, 0, 64, 0.4), rgba(75, 0, 130, 0.3));
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-left: 4px solid {gesture_color};
                border-radius: 15px;
                padding: 1.5rem;
                text-align: center;
                box-shadow: 0 4px 16px 0 rgba(0, 0, 0, 0.25);
            '>
                <div style='color: rgba(255, 255, 255, 0.7); font-size: 0.9rem; margin-bottom: 0.5rem;'>Gestures</div>
                <div style='font-size: 2rem; font-weight: bold; color: {gesture_color};'>{gesture_freq:.1f}</div>
                <div style='color: white; font-size: 0.85rem; margin-top: 0.3rem;'>per second</div>
                <div style='color: {gesture_color}; font-size: 0.75rem; margin-top: 0.5rem;'>{gesture_status}</div>
            </div>
            """, unsafe_allow_html=True)
        
        eye_contact = body_metrics.get('eye_contact', {}).get('eye_contact_percentage', 0.0)
        if eye_contact >= 0.7:
            eye_color = "#10b981"
            eye_status = "✓ Excellent"
        elif eye_contact >= 0.5:
            eye_color = "#f59e0b"
            eye_status = "⚠ Fair"
        else:
            eye_color = "#ef4444"
            eye_status = "✗ Low"
        
        with col3:
            st.markdown(f"""
            <div style='
                background: linear-gradient(135deg, rgba(42, 0, 64, 0.4), rgba(75, 0, 130, 0.3));
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-left: 4px solid {eye_color};
                border-radius: 15px;
                padding: 1.5rem;
                text-align: center;
                box-shadow: 0 4px 16px 0 rgba(0, 0, 0, 0.25);
            '>
                <div style='color: rgba(255, 255, 255, 0.7); font-size: 0.9rem; margin-bottom: 0.5rem;'>Eye Contact</div>
                <div style='font-size: 2rem; font-weight: bold; color: {eye_color};'>{eye_contact*100:.0f}</div>
                <div style='color: white; font-size: 0.85rem; margin-top: 0.3rem;'>Percentage %</div>
                <div style='color: {eye_color}; font-size: 0.75rem; margin-top: 0.5rem;'>{eye_status}</div>
            </div>
            """, unsafe_allow_html=True)
        
        engagement = body_metrics.get('facial_expressions', {}).get('engagement_score', 0.0)
        if engagement >= 0.7:
            engage_color = "#10b981"
            engage_status = "✓ Engaged"
        elif engagement >= 0.5:
            engage_color = "#f59e0b"
            engage_status = "⚠ Moderate"
        else:
            engage_color = "#ef4444"
            engage_status = "✗ Low"
        
        with col4:
            st.markdown(f"""
            <div style='
                background: linear-gradient(135deg, rgba(42, 0, 64, 0.4), rgba(75, 0, 130, 0.3));
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-left: 4px solid {engage_color};
                border-radius: 15px;
                padding: 1.5rem;
                text-align: center;
                box-shadow: 0 4px 16px 0 rgba(0, 0, 0, 0.25);
            '>
                <div style='color: rgba(255, 255, 255, 0.7); font-size: 0.9rem; margin-bottom: 0.5rem;'>Engagement</div>
                <div style='font-size: 2rem; font-weight: bold; color: {engage_color};'>{engagement*100:.0f}</div>
                <div style='color: white; font-size: 0.85rem; margin-top: 0.3rem;'>Score %</div>
                <div style='color: {engage_color}; font-size: 0.75rem; margin-top: 0.5rem;'>{engage_status}</div>
            </div>
            """, unsafe_allow_html=True)
        
        presence = body_metrics.get('presence_score', 0.0)
        if presence >= 0.75:
            presence_color = "#10b981"
            presence_status = "✓ Strong"
        elif presence >= 0.55:
            presence_color = "#f59e0b"
            presence_status = "⚠ Moderate"
        else:
            presence_color = "#ef4444"
            presence_status = "✗ Weak"
        
        with col5:
            st.markdown(f"""
            <div style='
                background: linear-gradient(135deg, rgba(42, 0, 64, 0.4), rgba(75, 0, 130, 0.3));
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-left: 4px solid {presence_color};
                border-radius: 15px;
                padding: 1.5rem;
                text-align: center;
                box-shadow: 0 4px 16px 0 rgba(0, 0, 0, 0.25);
            '>
                <div style='color: rgba(255, 255, 255, 0.7); font-size: 0.9rem; margin-bottom: 0.5rem;'>Presence</div>
                <div style='font-size: 2rem; font-weight: bold; color: {presence_color};'>{presence*100:.0f}</div>
                <div style='color: white; font-size: 0.85rem; margin-top: 0.3rem;'>Overall %</div>
                <div style='color: {presence_color}; font-size: 0.75rem; margin-top: 0.5rem;'>{presence_status}</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Body language visualizations
        st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        # Posture gauge
        with col1:
            fig_posture = go.Figure()
            fig_posture.add_trace(go.Indicator(
                mode="gauge+number",
                value=posture_score * 100,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Posture Quality (%)", 'font': {'color': 'white', 'size': 16}},
                number={'font': {'color': 'white', 'size': 32}, 'suffix': '%'},
                gauge={
                    'axis': {
                        'range': [None, 100], 
                        'tickcolor': 'white',
                        'tickfont': {'color': 'white'}
                    },
                    'bar': {'color': posture_color},
                    'bgcolor': 'rgba(42, 0, 64, 0.3)',
                    'bordercolor': 'rgba(255, 255, 255, 0.1)',
                    'steps': [
                        {'range': [0, 50], 'color': 'rgba(239, 68, 68, 0.3)'},
                        {'range': [50, 75], 'color': 'rgba(245, 158, 11, 0.3)'},
                        {'range': [75, 100], 'color': 'rgba(16, 185, 129, 0.3)'}
                    ],
                }
            ))
            fig_posture.update_layout(
                height=250,
                paper_bgcolor='rgba(0,0,0,0)',
                font={'color': 'white', 'size': 12}
            )
            st.plotly_chart(fig_posture, use_container_width=True)
        
        # Eye contact gauge
        with col2:
            fig_eye = go.Figure()
            fig_eye.add_trace(go.Indicator(
                mode="gauge+number",
                value=eye_contact * 100,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Eye Contact (%)", 'font': {'color': 'white', 'size': 16}},
                number={'font': {'color': 'white', 'size': 32}, 'suffix': '%'},
                gauge={
                    'axis': {
                        'range': [None, 100],
                        'tickcolor': 'white',
                        'tickfont': {'color': 'white'}
                    },
                    'bar': {'color': eye_color},
                    'bgcolor': 'rgba(42, 0, 64, 0.3)',
                    'bordercolor': 'rgba(255, 255, 255, 0.1)',
                    'steps': [
                        {'range': [0, 50], 'color': 'rgba(239, 68, 68, 0.3)'},
                        {'range': [50, 70], 'color': 'rgba(245, 158, 11, 0.3)'},
                        {'range': [70, 100], 'color': 'rgba(16, 185, 129, 0.3)'}
                    ],
                }
            ))
            fig_eye.update_layout(
                height=250,
                paper_bgcolor='rgba(0,0,0,0)',
                font={'color': 'white', 'size': 12}
            )
            st.plotly_chart(fig_eye, use_container_width=True)
        
        # Gesture analysis
        gesture_count = body_metrics.get('gestures', {}).get('gesture_count', 0)
        gesture_variety = body_metrics.get('gestures', {}).get('gesture_variety', 0.0)
        
        fig_gestures = go.Figure()
        fig_gestures.add_trace(go.Bar(
            x=['Total Gestures', 'Variety Score', 'Frequency'],
            y=[gesture_count, gesture_variety * 100, gesture_freq],
            marker_color=[gesture_color, gesture_color, gesture_color],
            marker_line=dict(color='white', width=1)
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
        
        # Movement gauge
        movement_score = body_metrics.get('movement_score', 0.0)
        if movement_score >= 0.7:
            move_color = "#10b981"
        elif movement_score >= 0.4:
            move_color = "#f59e0b"
        else:
            move_color = "#ef4444"
        
        fig_movement = go.Figure()
        fig_movement.add_trace(go.Indicator(
            mode="gauge+number",
            value=movement_score * 100,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Movement & Energy (%)", 'font': {'color': 'white', 'size': 16}},
            number={'font': {'color': 'white', 'size': 32}, 'suffix': '%'},
            gauge={
                'axis': {
                    'range': [None, 100],
                    'tickcolor': 'white',
                    'tickfont': {'color': 'white'}
                },
                'bar': {'color': move_color},
                'bgcolor': 'rgba(42, 0, 64, 0.3)',
                'bordercolor': 'rgba(255, 255, 255, 0.1)',
                'steps': [
                    {'range': [0, 40], 'color': 'rgba(239, 68, 68, 0.3)'},
                    {'range': [40, 70], 'color': 'rgba(245, 158, 11, 0.3)'},
                    {'range': [70, 100], 'color': 'rgba(16, 185, 129, 0.3)'}
                ],
            }
        ))
        fig_movement.update_layout(
            height=250,
            paper_bgcolor='rgba(0,0,0,0)',
            font={'color': 'white', 'size': 12}
        )
        st.plotly_chart(fig_movement, use_container_width=True)
        
        # Body language feedback
        st.markdown("""
        <h4 style='color: #ffffff; margin-top: 1.5rem; margin-bottom: 1rem;'>
            💡 Body Language Recommendations
        </h4>
        """, unsafe_allow_html=True)
        
        for i, rec in enumerate(body_feedback['recommendations'], 1):
            st.markdown(f"""
            <div style='
                background: linear-gradient(135deg, rgba(139, 92, 246, 0.1), rgba(42, 0, 64, 0.3));
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-left: 3px solid #8b5cf6;
                border-radius: 10px;
                padding: 1rem;
                margin-bottom: 0.75rem;
                color: white;
            '>
                <strong>{i}.</strong> {rec}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <h3 style='color: #ffffff; margin-top: 2.5rem; margin-bottom: 1rem;'>
            👤 Body Language Analysis
        </h3>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style='
            background: linear-gradient(135deg, rgba(107, 114, 128, 0.15), rgba(42, 0, 64, 0.3));
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 2rem;
            text-align: center;
        '>
            <div style='font-size: 3rem; margin-bottom: 1rem;'>📹</div>
            <div style='color: white; font-size: 1.2rem; margin-bottom: 0.5rem;'>Video Analysis Not Available</div>
            <div style='color: rgba(255, 255, 255, 0.7); font-size: 0.95rem;'>
                Body language analysis requires a video file with MediaPipe dependencies installed.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Summary Section
    st.markdown("""
    <h2 style='color: #ffffff; margin-top: 3rem; margin-bottom: 1.5rem;'>
        📊 Performance Summary
    </h2>
    """, unsafe_allow_html=True)
    
    # Summary cards
    col1, col2 = st.columns(2)
    
    with col1:
        voice_status = "✓ Good" if overall_scores['voice_score'] >= 70 else "⚠ Needs Work"
        voice_status_color = "#10b981" if overall_scores['voice_score'] >= 70 else "#f59e0b"
        
        st.markdown(f"""
        <div style='
            background: linear-gradient(135deg, rgba(42, 0, 64, 0.4), rgba(75, 0, 130, 0.3));
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 1.5rem;
            margin-bottom: 1rem;
        '>
            <div style='font-size: 1.5rem; margin-bottom: 0.5rem;'>🎙️</div>
            <div style='color: white; font-size: 1.2rem; font-weight: bold; margin-bottom: 0.5rem;'>Voice Analysis</div>
            <div style='color: #3b82f6; font-size: 2rem; font-weight: bold; margin-bottom: 0.5rem;'>
                {overall_scores['voice_score']:.1f}
            </div>
            <div style='color: {voice_status_color}; font-size: 0.9rem;'>{voice_status}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        lang_status = "✓ Good" if overall_scores['language_score'] >= 70 else "⚠ Needs Work"
        lang_status_color = "#10b981" if overall_scores['language_score'] >= 70 else "#f59e0b"
        
        st.markdown(f"""
        <div style='
            background: linear-gradient(135deg, rgba(42, 0, 64, 0.4), rgba(75, 0, 130, 0.3));
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 1.5rem;
            margin-bottom: 1rem;
        '>
            <div style='font-size: 1.5rem; margin-bottom: 0.5rem;'>📝</div>
            <div style='color: white; font-size: 1.2rem; font-weight: bold; margin-bottom: 0.5rem;'>Language Analysis</div>
            <div style='color: #10b981; font-size: 2rem; font-weight: bold; margin-bottom: 0.5rem;'>
                {overall_scores['language_score']:.1f}
            </div>
            <div style='color: {lang_status_color}; font-size: 0.9rem;'>{lang_status}</div>
        </div>
        """, unsafe_allow_html=True)
    
    if body_metrics:
        body_status = "✓ Good" if overall_scores['body_score'] >= 70 else "⚠ Needs Work"
        body_status_color = "#10b981" if overall_scores['body_score'] >= 70 else "#f59e0b"
        
        st.markdown(f"""
        <div style='
            background: linear-gradient(135deg, rgba(42, 0, 64, 0.4), rgba(75, 0, 130, 0.3));
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 1.5rem;
            margin-bottom: 1rem;
        '>
            <div style='font-size: 1.5rem; margin-bottom: 0.5rem;'>👤</div>
            <div style='color: white; font-size: 1.2rem; font-weight: bold; margin-bottom: 0.5rem;'>Body Language Analysis</div>
            <div style='color: #8b5cf6; font-size: 2rem; font-weight: bold; margin-bottom: 0.5rem;'>
                {overall_scores['body_score']:.1f}
            </div>
            <div style='color: {body_status_color}; font-size: 0.9rem;'>{body_status}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Final encouragement message
    st.markdown(f"""
    <div style='
        background: linear-gradient(135deg, {gradient});
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 2rem;
        margin-top: 2rem;
        text-align: center;
    '>
        <div style='font-size: 2rem; margin-bottom: 1rem;'>{score_emoji}</div>
        <div style='color: white; font-size: 1.3rem; font-weight: bold; margin-bottom: 0.5rem;'>
            Overall Performance: {score_label}
        </div>
        <div style='color: rgba(255, 255, 255, 0.8); font-size: 1rem; line-height: 1.6;'>
            Your speaking score is <strong style='color: {score_color};'>{overall_score:.1f}/100</strong>. 
            {"Keep up the excellent work! 🌟" if overall_score >= 80 else
             "You're on the right track! Focus on the recommendations above to improve further. 💪" if overall_score >= 65 else
             "Great effort! Work on the priority actions to see significant improvement. 📈" if overall_score >= 50 else
             "There's room for growth! Follow the recommendations carefully and practice regularly. 🎯"}
        </div>
    </div>
    """, unsafe_allow_html=True)
