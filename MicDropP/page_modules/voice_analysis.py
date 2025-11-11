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
    
    st.markdown("""
    <h1 style='display: flex; align-items: center; gap: 0.75rem; color: #ffffff;'>
        <svg style="width: 2rem; height: 2rem; fill: currentColor;" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3z" fill="currentColor"/>
            <path d="M17 11c0 2.76-2.24 5-5 5s-5-2.24-5-5H5c0 3.53 2.61 6.43 6 6.92V21h2v-3.08c3.39-.49 6-3.39 6-6.92h-2z" fill="currentColor"/>
        </svg>
        Voice Analysis
    </h1>
    """, unsafe_allow_html=True)
    st.markdown("Analyze your speaking pace, pitch, pauses, and volume.")
    
    # Tips for best results
    with st.expander("Tips for Best Results", expanded=False):
        st.markdown("""
        - **Audio Quality**: Use a quiet environment with minimal background noise
        - **Speak Clearly**: Enunciate your words and speak at a natural pace
        - **Duration**: 30 seconds to 5 minutes works best for analysis
        - **Format**: MP3, WAV, M4A, OGG, or FLAC formats are supported
        - **Microphone**: Use a good quality microphone if possible for clearer audio
        """)
    
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
        record_audio = st.button("Record Audio", use_container_width=True)
    
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
    
    st.markdown("---")
    st.markdown("## 📊 Analysis Results")
    st.markdown("")
    
    # Key Metrics with modern cards
    st.markdown("### 🎯 Key Metrics")
    st.markdown("")
    
    col1, col2, col3, col4 = st.columns(4)
    
    wpm = voice_metrics['pace']['wpm']
    pause_count = voice_metrics['pauses']['count']
    monotony = voice_metrics['pitch']['monotony_score']
    consistency = voice_metrics['volume']['volume_consistency']
    
    # Determine status colors
    pace_color = "#10b981" if 120 <= wpm <= 180 else "#f59e0b"
    pause_color = "#10b981" if 3 <= pause_count <= 15 else "#f59e0b"
    pitch_color = "#10b981" if monotony < 0.7 else ("#f59e0b" if monotony < 0.85 else "#ef4444")
    volume_color = "#10b981" if consistency > 0.5 else "#f59e0b"
    
    with col1:
        st.markdown(f"""
        <div class='metric-card' style='text-align: center; padding: 1.5rem; border-left: 4px solid {pace_color};'>
            <div style='font-size: 0.875rem; color: rgba(255, 255, 255, 0.7); font-weight: 500; margin-bottom: 0.5rem;'>SPEAKING PACE</div>
            <div style='font-size: 2.5rem; font-weight: 800; color: {pace_color}; margin-bottom: 0.25rem;'>{wpm:.0f}</div>
            <div style='font-size: 0.875rem; color: rgba(255, 255, 255, 0.6);'>words per minute</div>
            <div style='font-size: 0.75rem; color: rgba(255, 255, 255, 0.5); margin-top: 0.5rem;'>Ideal: 140-160 WPM</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class='metric-card' style='text-align: center; padding: 1.5rem; border-left: 4px solid {pause_color};'>
            <div style='font-size: 0.875rem; color: rgba(255, 255, 255, 0.7); font-weight: 500; margin-bottom: 0.5rem;'>PAUSES</div>
            <div style='font-size: 2.5rem; font-weight: 800; color: {pause_color}; margin-bottom: 0.25rem;'>{pause_count}</div>
            <div style='font-size: 0.875rem; color: rgba(255, 255, 255, 0.6);'>detected</div>
            <div style='font-size: 0.75rem; color: rgba(255, 255, 255, 0.5); margin-top: 0.5rem;'>Ideal: 3-15 pauses</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        pitch_label = "Varied" if monotony < 0.3 else ("Monotone" if monotony > 0.7 else "Good")
        st.markdown(f"""
        <div class='metric-card' style='text-align: center; padding: 1.5rem; border-left: 4px solid {pitch_color};'>
            <div style='font-size: 0.875rem; color: rgba(255, 255, 255, 0.7); font-weight: 500; margin-bottom: 0.5rem;'>PITCH VARIATION</div>
            <div style='font-size: 2.5rem; font-weight: 800; color: {pitch_color}; margin-bottom: 0.25rem;'>{pitch_label}</div>
            <div style='font-size: 0.875rem; color: rgba(255, 255, 255, 0.6);'>{(1-monotony)*100:.0f}% varied</div>
            <div style='font-size: 0.75rem; color: rgba(255, 255, 255, 0.5); margin-top: 0.5rem;'>Lower is more varied</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        vol_label = "Consistent" if consistency > 0.5 else "Variable"
        st.markdown(f"""
        <div class='metric-card' style='text-align: center; padding: 1.5rem; border-left: 4px solid {volume_color};'>
            <div style='font-size: 0.875rem; color: rgba(255, 255, 255, 0.7); font-weight: 500; margin-bottom: 0.5rem;'>VOLUME</div>
            <div style='font-size: 2.5rem; font-weight: 800; color: {volume_color}; margin-bottom: 0.25rem;'>{vol_label}</div>
            <div style='font-size: 0.875rem; color: rgba(255, 255, 255, 0.6);'>{consistency*100:.0f}% consistent</div>
            <div style='font-size: 0.75rem; color: rgba(255, 255, 255, 0.5); margin-top: 0.5rem;'>Higher is better</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("")
    st.markdown("")
    
    # Visualizations
    st.markdown("### 📈 Detailed Visualizations")
    st.markdown("")
    
    # Pace visualization
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🎤 Speaking Pace")
        fig_pace = go.Figure()
        fig_pace.add_trace(go.Indicator(
            mode="gauge+number",
            value=voice_metrics['pace']['wpm'],
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Words Per Minute", 'font': {'size': 16, 'color': 'white'}},
            gauge={
                'axis': {
                    'range': [None, 200], 
                    'tickcolor': 'white',
                    'tickfont': {'color': 'white'}
                },
                'bar': {'color': pace_color},
                'bgcolor': 'rgba(42, 0, 64, 0.3)',
                'steps': [
                    {'range': [0, 120], 'color': "rgba(239, 68, 68, 0.2)"},
                    {'range': [120, 180], 'color': "rgba(16, 185, 129, 0.2)"},
                    {'range': [180, 200], 'color': "rgba(239, 68, 68, 0.2)"}
                ],
                'threshold': {
                    'line': {'color': "white", 'width': 2},
                    'thickness': 0.75,
                    'value': 150
                }
            },
            number={'font': {'size': 32, 'color': pace_color}}
        ))
        fig_pace.update_layout(
            height=300,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font={'color': 'white'}
        )
        st.plotly_chart(fig_pace, use_container_width=True)
    
    with col2:
        st.markdown("#### ⏸️ Pause Analysis")
        if voice_metrics['pauses']['count'] > 0:
            pause_times = [start for start, _ in voice_metrics['pauses']['pauses']]
            pause_durations = [end - start for start, end in voice_metrics['pauses']['pauses']]
            
            fig_pauses = go.Figure()
            fig_pauses.add_trace(go.Bar(
                x=pause_times,
                y=pause_durations,
                marker_color=pause_color,
                marker_line_color='rgba(255,255,255,0.2)',
                marker_line_width=1,
                name='Pause Duration',
                hovertemplate='<b>Time:</b> %{x:.1f}s<br><b>Duration:</b> %{y:.2f}s<extra></extra>'
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
        else:
            st.info("✅ No significant pauses detected.")
    
    st.markdown("")
    
    # Pitch and Volume visualization
    col1, col2 = st.columns(2)
    
    with col1:
        if 'pitch_values' in voice_metrics['pitch'] and len(voice_metrics['pitch']['pitch_values']) > 0:
            st.markdown("#### 🎵 Pitch Variation")
            pitch_values = voice_metrics['pitch']['pitch_values']
            times = np.linspace(0, len(y) / sr, len(pitch_values))
            
            fig_pitch = go.Figure()
            fig_pitch.add_trace(go.Scatter(
                x=times,
                y=pitch_values,
                mode='lines',
                name='Pitch',
                line=dict(color=pitch_color, width=2),
                fill='tozeroy',
                fillcolor=f'rgba({int(pitch_color[1:3], 16)}, {int(pitch_color[3:5], 16)}, {int(pitch_color[5:7], 16)}, 0.2)',
                hovertemplate='<b>Time:</b> %{x:.1f}s<br><b>Pitch:</b> %{y:.0f} Hz<extra></extra>'
            ))
            fig_pitch.update_layout(
                title={'text': "Pitch Over Time", 'font': {'color': 'white', 'size': 16}},
                xaxis_title="Time (seconds)",
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
        st.markdown("#### 🔊 Volume Over Time")
        rms_db = voice_metrics['volume']['rms_db']
        times = np.linspace(0, len(y) / sr, len(rms_db))
        
        fig_volume = go.Figure()
        fig_volume.add_trace(go.Scatter(
            x=times,
            y=rms_db,
            mode='lines',
            name='Volume (dB)',
            fill='tozeroy',
            line=dict(color=volume_color, width=2),
            fillcolor=f'rgba({int(volume_color[1:3], 16)}, {int(volume_color[3:5], 16)}, {int(volume_color[5:7], 16)}, 0.2)',
            hovertemplate='<b>Time:</b> %{x:.1f}s<br><b>Volume:</b> %{y:.1f} dB<extra></extra>'
        ))
        fig_volume.update_layout(
            title={'text': "Volume Over Time", 'font': {'color': 'white', 'size': 16}},
            xaxis_title="Time (seconds)",
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
    
    st.markdown("")
    st.markdown("")
    
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
        'good': {'emoji': '🟢', 'label': 'Good', 'color': '#10b981'},
        'slow': {'emoji': '🟡', 'label': 'Slow', 'color': '#f59e0b'},
        'fast': {'emoji': '🟡', 'label': 'Fast', 'color': '#f59e0b'},
        'few': {'emoji': '🟡', 'label': 'Few', 'color': '#f59e0b'},
        'many': {'emoji': '🟡', 'label': 'Many', 'color': '#f59e0b'},
        'monotone': {'emoji': '🔴', 'label': 'Monotone', 'color': '#ef4444'},
        'varied': {'emoji': '🟢', 'label': 'Varied', 'color': '#10b981'},
        'consistent': {'emoji': '🟢', 'label': 'Consistent', 'color': '#10b981'},
        'inconsistent': {'emoji': '🟡', 'label': 'Variable', 'color': '#f59e0b'}
    }
    
    col1, col2, col3, col4 = st.columns(4)
    
    score_items = [
        ('Pace', scores.get('pace', 'good')),
        ('Pauses', scores.get('pauses', 'good')),
        ('Pitch', scores.get('pitch', 'good')),
        ('Volume', scores.get('volume', 'good'))
    ]
    
    for col, (metric_name, score_key) in zip([col1, col2, col3, col4], score_items):
        score_data = score_info.get(score_key, {'emoji': '⚪', 'label': 'N/A', 'color': '#6b7280'})
        with col:
            st.markdown(f"""
            <div style='text-align: center; padding: 1rem; background: rgba(42, 0, 64, 0.4); border-radius: 0.75rem; border: 1px solid rgba(74, 0, 100, 0.4);'>
                <div style='font-size: 0.875rem; color: rgba(255, 255, 255, 0.6); margin-bottom: 0.5rem;'>{metric_name}</div>
                <div style='font-size: 2rem; margin-bottom: 0.25rem;'>{score_data['emoji']}</div>
                <div style='font-size: 1rem; color: {score_data["color"]}; font-weight: 600;'>{score_data['label']}</div>
            </div>
            """, unsafe_allow_html=True)

