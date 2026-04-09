"""
Language Analysis Page
Analyzes language: clarity, word choice, filler words, structure
"""

import streamlit as st
import plotly.graph_objects as go
import numpy as np
from utils.audio_processor import transcribe_audio
from utils.language_analyzer import analyze_language
from utils.feedback_generator import generate_language_feedback


def show():
    """Display language analysis page"""
    
    st.markdown("""
    <h1 style='display: flex; align-items: center; gap: 0.75rem; color: #111111;'>
        <svg style="width: 2rem; height: 2rem; fill: currentColor;" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25zM20.71 7.04c.39-.39.39-1.02 0-1.41l-2.34-2.34c-.39-.39-1.02-.39-1.41 0l-1.83 1.83 3.75 3.75 1.83-1.83z" fill="currentColor"/>
        </svg>
        Language Analysis
    </h1>
    """, unsafe_allow_html=True)
    st.markdown("Analyze your speech for clarity, word choice, filler words, structure, and tone.")
    
    # Tips for best results
    with st.expander("Tips for Best Results", expanded=False):
        st.markdown("""
        - **Audio Quality**: Use a quiet environment with minimal background noise for better transcription
        - **Text Input**: If transcription fails, you can paste your speech text directly
        - **Duration**: 30 seconds to 5 minutes of speech works best
        - **Format**: MP3, WAV, M4A, OGG, or FLAC formats are supported
        - **Clarity**: Speak clearly and at a natural pace for accurate transcription
        - **Content**: Natural speech works best - avoid reading from scripts if possible
        """)
    
    # File upload section
    st.header("Upload Audio or Enter Text")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        audio_file = st.file_uploader(
            "Choose an audio file",
            type=['mp3', 'wav', 'm4a', 'ogg', 'flac'],
            help="Supported formats: MP3, WAV, M4A, OGG, FLAC"
        )
    
    with col2:
        st.markdown("### Or")
        use_text_input = st.checkbox("Enter text directly", value=False)
    
    # Text input option
    text_input = None
    if use_text_input:
        text_input = st.text_area(
            "Enter your speech text",
            height=150,
            help="Paste or type the text you want to analyze"
        )
    
    # Process if audio file uploaded
    if audio_file is not None:
        # Transcribe audio
        with st.spinner("Transcribing audio..."):
            try:
                text = transcribe_audio(audio_file)
                
                if text and text != "Could not understand audio" and not text.startswith("Error"):
                    st.success("✅ Audio transcribed successfully!")
                    st.text_area("Transcribed Text", text, height=100, key="transcribed")
                    process_language_analysis(text)
                else:
                    st.error(f"❌ Could not transcribe audio: {text}")
                    st.info("Try uploading a clearer audio file or use the text input option instead.")
            except Exception as e:
                st.error(f"❌ Error transcribing audio: {str(e)}")
                st.exception(e)
    
    # Process if text input provided
    elif text_input and text_input.strip():
        process_language_analysis(text_input)


def process_language_analysis(text):
    """Process and display language analysis results"""
    
    if not text or not text.strip():
        st.warning("⚠️ Please provide text to analyze.")
        return
    
    # Analyze language
    with st.spinner("Analyzing language characteristics..."):
        try:
            language_metrics = analyze_language(text)
            feedback = generate_language_feedback(language_metrics)
            
            # Display results
            display_results(language_metrics, feedback, text)
            
        except Exception as e:
            st.error(f"❌ Error analyzing language: {str(e)}")
            st.exception(e)


def display_results(language_metrics, feedback, text):
    """Display language analysis results"""
    
    st.markdown("---")
    st.markdown("## 📊 Analysis Results")
    st.markdown("")
    
    # Key Metrics with modern cards
    st.markdown("### 🎯 Key Metrics")
    st.markdown("")
    
    col1, col2, col3, col4 = st.columns(4)
    
    filler_rate = language_metrics.get('filler_words', {}).get('filler_rate', 0.0)
    diversity = language_metrics.get('vocabulary', {}).get('diversity_ratio', 0.0)
    flesch = language_metrics.get('readability', {}).get('flesch_reading_ease', 0)
    avg_sentence = language_metrics.get('sentence_structure', {}).get('avg_words_per_sentence', 0)
    
    # Determine status colors
    filler_color = "#111111" if filler_rate < 1.5 else ("#d96c6c" if filler_rate < 3.0 else "#000000")
    vocab_color = "#000000" if diversity < 0.4 else ("#111111" if diversity > 0.7 else "#d96c6c")
    readability_color = "#111111" if flesch > 70 else ("#000000" if flesch < 30 else "#d96c6c") if flesch > 0 else "#000000"
    sentence_color = "#111111" if 10 <= avg_sentence <= 20 else "#d96c6c"
    
    with col1:
        filler_label = "Low" if filler_rate < 1.5 else ("Moderate" if filler_rate < 3.0 else "High")
        st.markdown(f"""
        <div class='metric-card' style='text-align: center; padding: 1.5rem; border-left: 4px solid {filler_color};'>
            <div style='font-size: 0.875rem; color: rgba(255, 255, 255, 0.7); font-weight: 500; margin-bottom: 0.5rem;'>FILLER WORDS</div>
            <div style='font-size: 2.5rem; font-weight: 800; color: {filler_color}; margin-bottom: 0.25rem;'>{filler_rate:.1f}</div>
            <div style='font-size: 0.875rem; color: rgba(255, 255, 255, 0.6);'>per 100 words</div>
            <div style='font-size: 0.75rem; color: rgba(255, 255, 255, 0.5); margin-top: 0.5rem;'>{filler_label} usage</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        vocab_label = "Low" if diversity < 0.4 else ("High" if diversity > 0.7 else "Good")
        st.markdown(f"""
        <div class='metric-card' style='text-align: center; padding: 1.5rem; border-left: 4px solid {vocab_color};'>
            <div style='font-size: 0.875rem; color: rgba(255, 255, 255, 0.7); font-weight: 500; margin-bottom: 0.5rem;'>VOCABULARY</div>
            <div style='font-size: 2.5rem; font-weight: 800; color: {vocab_color}; margin-bottom: 0.25rem;'>{diversity*100:.0f}%</div>
            <div style='font-size: 0.875rem; color: rgba(255, 255, 255, 0.6);'>diversity</div>
            <div style='font-size: 0.75rem; color: rgba(255, 255, 255, 0.5); margin-top: 0.5rem;'>{vocab_label} variety</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        if flesch > 0:
            readability_label = "Easy" if flesch > 70 else ("Difficult" if flesch < 30 else "Moderate")
            st.markdown(f"""
            <div class='metric-card' style='text-align: center; padding: 1.5rem; border-left: 4px solid {readability_color};'>
                <div style='font-size: 0.875rem; color: rgba(255, 255, 255, 0.7); font-weight: 500; margin-bottom: 0.5rem;'>READABILITY</div>
                <div style='font-size: 2.5rem; font-weight: 800; color: {readability_color}; margin-bottom: 0.25rem;'>{flesch:.0f}</div>
                <div style='font-size: 0.875rem; color: rgba(255, 255, 255, 0.6);'>Flesch score</div>
                <div style='font-size: 0.75rem; color: rgba(255, 255, 255, 0.5); margin-top: 0.5rem;'>{readability_label} to read</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class='metric-card' style='text-align: center; padding: 1.5rem; border-left: 4px solid {readability_color};'>
                <div style='font-size: 0.875rem; color: rgba(255, 255, 255, 0.7); font-weight: 500; margin-bottom: 0.5rem;'>READABILITY</div>
                <div style='font-size: 2.5rem; font-weight: 800; color: {readability_color}; margin-bottom: 0.25rem;'>N/A</div>
                <div style='font-size: 0.875rem; color: rgba(255, 255, 255, 0.6);'>score</div>
                <div style='font-size: 0.75rem; color: rgba(255, 255, 255, 0.5); margin-top: 0.5rem;'>Not available</div>
            </div>
            """, unsafe_allow_html=True)
    
    with col4:
        sentence_label = "Good" if 10 <= avg_sentence <= 20 else ("Complex" if avg_sentence > 20 else "Simple")
        st.markdown(f"""
        <div class='metric-card' style='text-align: center; padding: 1.5rem; border-left: 4px solid {sentence_color};'>
            <div style='font-size: 0.875rem; color: rgba(255, 255, 255, 0.7); font-weight: 500; margin-bottom: 0.5rem;'>SENTENCE LENGTH</div>
            <div style='font-size: 2.5rem; font-weight: 800; color: {sentence_color}; margin-bottom: 0.25rem;'>{avg_sentence:.1f}</div>
            <div style='font-size: 0.875rem; color: rgba(255, 255, 255, 0.6);'>words average</div>
            <div style='font-size: 0.75rem; color: rgba(255, 255, 255, 0.5); margin-top: 0.5rem;'>{sentence_label} length</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("")
    st.markdown("")
    
    # Detailed Visualizations
    st.markdown("### 📈 Detailed Analysis")
    st.markdown("")
    
    # Filler words visualization
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🗣️ Filler Words Breakdown")
        filler_words_dict = language_metrics.get('filler_words', {}).get('filler_words', {})
        if filler_words_dict:
            fillers = list(filler_words_dict.keys())
            counts = list(filler_words_dict.values())
            
            fig_fillers = go.Figure()
            fig_fillers.add_trace(go.Bar(
                x=fillers,
                y=counts,
                marker_color=filler_color,
                marker_line_color='rgba(255,255,255,0.2)',
                marker_line_width=1,
                name='Filler Count',
                hovertemplate='<b>%{x}</b><br>Count: %{y}<extra></extra>'
            ))
            fig_fillers.update_layout(
                title={'text': "Filler Words Detected", 'font': {'color': '#111111', 'size': 16}},
                xaxis_title="Filler Word",
                yaxis_title="Count",
                height=300,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(91, 143, 199, 0.14)',
                font={'color': '#111111', 'size': 12},
                xaxis={
                    'gridcolor': 'rgba(255,255,255,0.1)',
                    'color': '#111111',
                    'title': {'font': {'color': '#111111'}},
                    'tickfont': {'color': '#111111'}
                },
                yaxis={
                    'gridcolor': 'rgba(255,255,255,0.1)',
                    'color': '#111111',
                    'title': {'font': {'color': '#111111'}},
                    'tickfont': {'color': '#111111'}
                }
            )
            st.plotly_chart(fig_fillers, use_container_width=True)
        else:
            st.markdown("""
            <div style='padding: 2rem; text-align: center; background: rgba(217, 108, 108, 0.1); border-radius: 0.75rem; border: 1px solid rgba(217, 108, 108, 0.3);'>
                <div style='font-size: 2rem; margin-bottom: 0.5rem;'>✅</div>
                <div style='font-size: 1rem; color: #111111; font-weight: 600;'>No filler words detected!</div>
                <div style='font-size: 0.875rem; color: rgba(255, 255, 255, 0.6); margin-top: 0.5rem;'>Great job keeping your speech clean</div>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("#### 📚 Vocabulary Diversity")
        vocab_stats = language_metrics.get('vocabulary', {})
        unique_words = vocab_stats.get('unique_words', 0)
        total_words = vocab_stats.get('total_words', 0)
        
        fig_vocab = go.Figure()
        fig_vocab.add_trace(go.Indicator(
            mode="gauge+number",
            value=vocab_stats.get('diversity_ratio', 0) * 100,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Diversity %", 'font': {'size': 16, 'color': '#111111'}},
            gauge={
                'axis': {
                    'range': [None, 100], 
                    'tickcolor': '#94a3b8',
                    'tickfont': {'color': '#111111'}
                },
                'bar': {'color': vocab_color},
                'bgcolor': 'rgba(91, 143, 199, 0.25)',
                'steps': [
                    {'range': [0, 40], 'color': "rgba(91, 143, 199, 0.14)"},
                    {'range': [40, 70], 'color': "rgba(217, 108, 108, 0.2)"},
                    {'range': [70, 100], 'color': "rgba(217, 108, 108, 0.2)"}
                ],
                'threshold': {
                    'line': {'color': '#111111', 'width': 2},
                    'thickness': 0.75,
                    'value': 70
                }
            },
            number={'font': {'size': 32, 'color': vocab_color}}
        ))
        fig_vocab.update_layout(
            height=300,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font={'color': '#111111', 'size': 12}
        )
        st.plotly_chart(fig_vocab, use_container_width=True)
        
        st.markdown(f"""
        <div style='text-align: center; font-size: 0.875rem; color: rgba(255, 255, 255, 0.6);'>
            {unique_words} unique words / {total_words} total words
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("")
    
    # Readability metrics
    st.markdown("#### 📖 Readability Metrics")
    readability = language_metrics.get('readability', {})
    if readability.get('flesch_reading_ease', 0) > 0:
        col1, col2, col3, col4 = st.columns(4)
        
        metrics_data = [
            ("Flesch Reading Ease", readability.get('flesch_reading_ease', 0), "0f", "Higher = easier"),
            ("Flesch-Kincaid Grade", readability.get('flesch_kincaid_grade', 0), "1f", "Grade level"),
            ("SMOG Index", readability.get('smog_index', 0), "1f", "Years of education"),
            ("ARI", readability.get('automated_readability_index', 0), "1f", "Grade level")
        ]
        
        for col, (label, value, fmt, desc) in zip([col1, col2, col3, col4], metrics_data):
            with col:
                st.markdown(f"""
                <div style='text-align: center; padding: 1rem; background: rgba(91, 143, 199, 0.22); border-radius: 0.75rem; border: 1px solid rgba(217, 108, 108, 0.4);'>
                    <div style='font-size: 0.75rem; color: rgba(255, 255, 255, 0.6); margin-bottom: 0.5rem; text-transform: uppercase;'>{label}</div>
                    <div style='font-size: 2rem; font-weight: 700; color: #d96c6c; margin-bottom: 0.25rem;'>{value:.{fmt}}</div>
                    <div style='font-size: 0.75rem; color: rgba(255, 255, 255, 0.5);'>{desc}</div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style='padding: 1.5rem; text-align: center; background: rgba(99, 102, 241, 0.1); border-radius: 0.75rem; border: 1px solid rgba(99, 102, 241, 0.3);'>
            <div style='font-size: 1rem; color: #6366f1; font-weight: 600;'>ℹ️ Readability metrics require textstat library</div>
            <div style='font-size: 0.875rem; color: rgba(255, 255, 255, 0.6); margin-top: 0.5rem;'>Install with: pip install textstat</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("")
    
    # Sentence structure
    st.markdown("#### 📝 Sentence Structure")
    sentence_stats = language_metrics.get('sentence_structure', {})
    col1, col2, col3 = st.columns(3)
    
    structure_data = [
        ("Total Sentences", sentence_stats.get('sentence_count', 0), "Count"),
        ("Long Sentences", sentence_stats.get('long_sentences_count', 0), ">25 words"),
        ("Short Sentences", sentence_stats.get('short_sentences_count', 0), "<10 words")
    ]
    
    for col, (label, value, desc) in zip([col1, col2, col3], structure_data):
        with col:
            st.markdown(f"""
            <div style='text-align: center; padding: 1rem; background: rgba(91, 143, 199, 0.22); border-radius: 0.75rem; border: 1px solid rgba(217, 108, 108, 0.4);'>
                <div style='font-size: 0.75rem; color: rgba(255, 255, 255, 0.6); margin-bottom: 0.5rem; text-transform: uppercase;'>{label}</div>
                <div style='font-size: 2.5rem; font-weight: 700; color: #d96c6c; margin-bottom: 0.25rem;'>{value}</div>
                <div style='font-size: 0.75rem; color: rgba(255, 255, 255, 0.5);'>{desc}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("")
    
    # Repetition analysis
    repetition_stats = language_metrics.get('repetition', {})
    most_repeated = repetition_stats.get('most_repeated', [])
    
    if most_repeated:
        st.markdown("#### 🔁 Word Repetition")
        col1, col2 = st.columns([1, 2])
        
        with col1:
            repetition_score = repetition_stats.get('repetition_score', 0.0)
            rep_color = "#111111" if repetition_score < 8 else ("#d96c6c" if repetition_score < 15 else "#000000")
            st.markdown(f"""
            <div style='text-align: center; padding: 1.5rem; background: rgba(91, 143, 199, 0.22); border-radius: 0.75rem; border: 1px solid rgba(217, 108, 108, 0.4);'>
                <div style='font-size: 0.75rem; color: rgba(255, 255, 255, 0.6); margin-bottom: 0.5rem; text-transform: uppercase;'>Repetition Score</div>
                <div style='font-size: 2.5rem; font-weight: 700; color: {rep_color}; margin-bottom: 0.25rem;'>{repetition_score:.1f}%</div>
                <div style='font-size: 0.75rem; color: rgba(255, 255, 255, 0.5);'>Lower is better</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            repeated_words_html = " ".join([f"<span style='display: inline-block; padding: 0.5rem 0.75rem; margin: 0.25rem; background: rgba(217, 108, 108, 0.2); border-radius: 0.5rem; border: 1px solid rgba(217, 108, 108, 0.3);'><strong>{word}</strong> <span style='color: #d96c6c;'>({count}x)</span></span>" for word, count in most_repeated[:10]])
            st.markdown(f"""
            <div style='padding: 1rem; background: rgba(91, 143, 199, 0.22); border-radius: 0.75rem; border: 1px solid rgba(217, 108, 108, 0.4);'>
                <div style='font-size: 0.875rem; color: rgba(255, 255, 255, 0.7); margin-bottom: 0.75rem; font-weight: 600;'>Most Repeated Words:</div>
                <div style='display: flex; flex-wrap: wrap; gap: 0.5rem;'>
                    {repeated_words_html}
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("")
    
    # Tone analysis
    st.markdown("#### 🎭 Tone & Engagement")
    tone_stats = language_metrics.get('tone', {})
    col1, col2, col3, col4 = st.columns(4)
    
    tone_data = [
        ("Engagement Score", tone_stats.get('engagement_score', 0), "%", "1f"),
        ("Confidence Indicators", tone_stats.get('confidence_indicators', 0), "", "0f"),
        ("Questions", tone_stats.get('question_count', 0), "", "0f"),
        ("Exclamations", tone_stats.get('exclamation_count', 0), "", "0f")
    ]
    
    for col, (label, value, unit, fmt) in zip([col1, col2, col3, col4], tone_data):
        with col:
            st.markdown(f"""
            <div style='text-align: center; padding: 1rem; background: rgba(91, 143, 199, 0.22); border-radius: 0.75rem; border: 1px solid rgba(217, 108, 108, 0.4);'>
                <div style='font-size: 0.75rem; color: rgba(255, 255, 255, 0.6); margin-bottom: 0.5rem; text-transform: uppercase;'>{label}</div>
                <div style='font-size: 2.25rem; font-weight: 700; color: #d96c6c; margin-bottom: 0.25rem;'>{value:.{fmt}}{unit}</div>
            </div>
            """, unsafe_allow_html=True)
    
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
            rec_color = "#111111"
            rec_icon = "✅"
        elif any(word in recommendation.lower() for word in ['try', 'consider', 'could']):
            rec_color = "#d96c6c"
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
        'high': {'emoji': '🔴', 'label': 'High', 'color': '#000000'},
        'moderate': {'emoji': '🟡', 'label': 'Moderate', 'color': '#d96c6c'},
        'low': {'emoji': '🟢', 'label': 'Low', 'color': '#111111'},
        'low_engagement': {'emoji': '🟡', 'label': 'Low', 'color': '#d96c6c'},
        'engaging': {'emoji': '🟢', 'label': 'Engaging', 'color': '#111111'},
        'good': {'emoji': '🟢', 'label': 'Good', 'color': '#111111'},
        'difficult': {'emoji': '🔴', 'label': 'Difficult', 'color': '#000000'},
        'easy': {'emoji': '🟢', 'label': 'Easy', 'color': '#111111'},
        'complex': {'emoji': '🟡', 'label': 'Complex', 'color': '#d96c6c'},
        'simple': {'emoji': '🟡', 'label': 'Simple', 'color': '#d96c6c'},
        'issues': {'emoji': '🟡', 'label': 'Issues', 'color': '#d96c6c'}
    }
    
    # First row - main metrics
    col1, col2, col3, col4 = st.columns(4)
    
    metrics_row1 = [
        ('Filler Words', scores.get('filler_words', 'good')),
        ('Vocabulary', scores.get('vocabulary', 'good')),
        ('Readability', scores.get('readability', 'good')),
        ('Structure', scores.get('sentence_structure', 'good'))
    ]
    
    for col, (metric_name, score_key) in zip([col1, col2, col3, col4], metrics_row1):
        score_data = score_info.get(score_key, {'emoji': '⚪', 'label': 'N/A', 'color': '#000000'})
        with col:
            st.markdown(f"""
            <div style='text-align: center; padding: 1rem; background: rgba(91, 143, 199, 0.22); border-radius: 0.75rem; border: 1px solid rgba(217, 108, 108, 0.4);'>
                <div style='font-size: 0.875rem; color: rgba(255, 255, 255, 0.6); margin-bottom: 0.5rem;'>{metric_name}</div>
                <div style='font-size: 2rem; margin-bottom: 0.25rem;'>{score_data['emoji']}</div>
                <div style='font-size: 1rem; color: {score_data["color"]}; font-weight: 600;'>{score_data['label']}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("")
    
    # Second row - additional metrics
    col1, col2, col3 = st.columns(3)
    
    metrics_row2 = [
        ('Repetition', scores.get('repetition', 'low')),
        ('Tone', scores.get('tone', 'engaging')),
        ('Grammar', scores.get('grammar', 'good'))
    ]
    
    for col, (metric_name, score_key) in zip([col1, col2, col3], metrics_row2):
        score_data = score_info.get(score_key, {'emoji': '⚪', 'label': 'N/A', 'color': '#000000'})
        with col:
            st.markdown(f"""
            <div style='text-align: center; padding: 1rem; background: rgba(91, 143, 199, 0.22); border-radius: 0.75rem; border: 1px solid rgba(217, 108, 108, 0.4);'>
                <div style='font-size: 0.875rem; color: rgba(255, 255, 255, 0.6); margin-bottom: 0.5rem;'>{metric_name}</div>
                <div style='font-size: 2rem; margin-bottom: 0.25rem;'>{score_data['emoji']}</div>
                <div style='font-size: 1rem; color: {score_data["color"]}; font-weight: 600;'>{score_data['label'].replace('_', ' ').title()}</div>
            </div>
            """, unsafe_allow_html=True)
