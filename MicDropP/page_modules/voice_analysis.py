"""
Voice Analysis Page
Analyzes voice characteristics: pace, pitch, pauses, volume
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from utils.audio_processor import (
    load_audio, transcribe_audio, calculate_pace,
    detect_pauses, analyze_pitch, analyze_volume
)
from utils.feedback_generator import generate_voice_feedback


def show():
    """Display voice analysis page"""
    
    st.title("🎙️ Voice Analysis")
    st.markdown("Analyze your speaking pace, pitch, pauses, and volume")
    
    # File upload section
    st.header("Upload Audio")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        audio_file = st.file_uploader(
            "Choose an audio file",
            type=['mp3', 'wav', 'm4a', 'ogg', 'flac'],
            help="Supported formats: MP3, WAV, M4A, OGG, FLAC"
        )
    
    with col2:
        st.markdown("### Or")
        record_audio = st.button("🎤 Record Audio", use_container_width=True)
    
    if record_audio:
        st.info("Audio recording feature coming soon! Please upload an audio file for now.")
    
    if audio_file is not None:
        # Process audio
        with st.spinner("Processing audio... This may take a moment."):
            try:
                # Load audio
                y, sr = load_audio(audio_file)
                duration = len(y) / sr
                
                # Show basic info
                st.success(f"✅ Audio loaded successfully! Duration: {duration:.2f} seconds")
                
                # Transcribe
                with st.spinner("Transcribing audio..."):
                    text = transcribe_audio(audio_file)
                
                if text and text != "Could not understand audio":
                    st.text_area("Transcribed Text", text, height=100)
                else:
                    st.warning("⚠️ Could not transcribe audio. Analysis will continue with audio-only metrics.")
                
                # Calculate metrics
                with st.spinner("Analyzing voice characteristics..."):
                    # Pace
                    wpm, duration, _ = calculate_pace(audio_file, text if text else None)
                    
                    # Pauses
                    pauses = detect_pauses(y, sr)
                    pause_count = len(pauses)
                    pause_durations = [end - start for start, end in pauses]
                    avg_pause_duration = np.mean(pause_durations) if pause_durations else 0
                    
                    # Pitch
                    pitch_stats = analyze_pitch(y, sr)
                    
                    # Volume
                    volume_stats = analyze_volume(y, sr)
                
                # Organize metrics
                voice_metrics = {
                    'pace': {
                        'wpm': wpm,
                        'duration': duration
                    },
                    'pauses': {
                        'count': pause_count,
                        'avg_duration': avg_pause_duration,
                        'pauses': pauses
                    },
                    'pitch': pitch_stats,
                    'volume': volume_stats
                }
                
                # Generate feedback
                feedback = generate_voice_feedback(voice_metrics)
                
                # Display results
                display_results(voice_metrics, feedback, y, sr)
                
            except Exception as e:
                st.error(f"❌ Error processing audio: {str(e)}")
                st.exception(e)


def display_results(voice_metrics, feedback, y, sr):
    """Display analysis results"""
    
    st.header("📊 Analysis Results")
    
    # Key Metrics
    st.subheader("Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        wpm = voice_metrics['pace']['wpm']
        st.metric("Speaking Pace", f"{wpm:.0f} WPM", 
                 delta="Ideal: 140-160" if wpm < 120 or wpm > 180 else "Good range")
    
    with col2:
        pause_count = voice_metrics['pauses']['count']
        st.metric("Pauses", f"{pause_count}", 
                 delta="Good" if 3 <= pause_count <= 15 else "Review")
    
    with col3:
        monotony = voice_metrics['pitch']['monotony_score']
        pitch_score = "Varied" if monotony < 0.3 else ("Monotone" if monotony > 0.7 else "Good")
        st.metric("Pitch Variation", pitch_score)
    
    with col4:
        consistency = voice_metrics['volume']['volume_consistency']
        vol_score = "Consistent" if consistency > 0.5 else "Variable"
        st.metric("Volume", vol_score)
    
    # Visualizations
    st.subheader("📈 Detailed Visualizations")
    
    # Pace visualization
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Speaking Pace**")
        fig_pace = go.Figure()
        fig_pace.add_trace(go.Indicator(
            mode="gauge+number",
            value=voice_metrics['pace']['wpm'],
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Words Per Minute"},
            gauge={
                'axis': {'range': [None, 200]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 120], 'color': "lightgray"},
                    {'range': [120, 180], 'color': "gray"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 160
                }
            }
        ))
        fig_pace.update_layout(height=300)
        st.plotly_chart(fig_pace, use_container_width=True)
    
    with col2:
        st.markdown("**Pause Analysis**")
        if voice_metrics['pauses']['count'] > 0:
            pause_times = [start for start, _ in voice_metrics['pauses']['pauses']]
            pause_durations = [end - start for start, end in voice_metrics['pauses']['pauses']]
            
            fig_pauses = go.Figure()
            fig_pauses.add_trace(go.Bar(
                x=pause_times,
                y=pause_durations,
                marker_color='orange',
                name='Pause Duration'
            ))
            fig_pauses.update_layout(
                title="Pauses Over Time",
                xaxis_title="Time (seconds)",
                yaxis_title="Pause Duration (seconds)",
                height=300
            )
            st.plotly_chart(fig_pauses, use_container_width=True)
        else:
            st.info("No significant pauses detected.")
    
    # Pitch visualization
    if 'pitch_values' in voice_metrics['pitch'] and len(voice_metrics['pitch']['pitch_values']) > 0:
        st.markdown("**Pitch Variation**")
        pitch_values = voice_metrics['pitch']['pitch_values']
        times = np.linspace(0, len(y) / sr, len(pitch_values))
        
        fig_pitch = go.Figure()
        fig_pitch.add_trace(go.Scatter(
            x=times,
            y=pitch_values,
            mode='lines',
            name='Pitch',
            line=dict(color='green', width=2)
        ))
        fig_pitch.update_layout(
            title="Pitch Over Time",
            xaxis_title="Time (seconds)",
            yaxis_title="Pitch (Hz)",
            height=300
        )
        st.plotly_chart(fig_pitch, use_container_width=True)
    
    # Volume visualization
    st.markdown("**Volume Over Time**")
    rms_db = voice_metrics['volume']['rms_db']
    times = np.linspace(0, len(y) / sr, len(rms_db))
    
    fig_volume = go.Figure()
    fig_volume.add_trace(go.Scatter(
        x=times,
        y=rms_db,
        mode='lines',
        name='Volume (dB)',
        fill='tozeroy',
        line=dict(color='purple', width=2)
    ))
    fig_volume.update_layout(
        title="Volume Over Time",
        xaxis_title="Time (seconds)",
        yaxis_title="Volume (dB)",
        height=300
    )
    st.plotly_chart(fig_volume, use_container_width=True)
    
    # Feedback and Recommendations
    st.header("💡 Feedback & Recommendations")
    
    for i, recommendation in enumerate(feedback['recommendations'], 1):
        st.info(f"{i}. {recommendation}")
    
    # Summary scores
    st.subheader("Summary Scores")
    scores = feedback['scores']
    
    score_colors = {
        'good': '🟢',
        'slow': '🟡',
        'fast': '🟡',
        'few': '🟡',
        'many': '🟡',
        'monotone': '🔴',
        'varied': '🟢',
        'consistent': '🟢',
        'inconsistent': '🟡'
    }
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"**Pace:** {score_colors.get(scores.get('pace', 'good'), '⚪')} {scores.get('pace', 'N/A').title()}")
    with col2:
        st.markdown(f"**Pauses:** {score_colors.get(scores.get('pauses', 'good'), '⚪')} {scores.get('pauses', 'N/A').title()}")
    with col3:
        st.markdown(f"**Pitch:** {score_colors.get(scores.get('pitch', 'good'), '⚪')} {scores.get('pitch', 'N/A').title()}")
    with col4:
        st.markdown(f"**Volume:** {score_colors.get(scores.get('volume', 'good'), '⚪')} {scores.get('volume', 'N/A').title()}")

