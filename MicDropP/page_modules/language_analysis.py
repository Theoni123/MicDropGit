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
    <h1 style='display: flex; align-items: center; gap: 0.75rem; color: #ffffff;'>
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
    
    # Show instructions if nothing provided
    elif not audio_file and not text_input:
        st.info("👆 Upload an audio file or enter text above to begin analysis")


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
    
    st.header("📊 Analysis Results")
    
    # Key Metrics
    st.subheader("Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        filler_rate = language_metrics.get('filler_words', {}).get('filler_rate', 0.0)
        filler_score = "Low" if filler_rate < 1.5 else ("Moderate" if filler_rate < 3.0 else "High")
        st.metric("Filler Words", f"{filler_rate:.1f} per 100 words", 
                 delta=filler_score)
    
    with col2:
        diversity = language_metrics.get('vocabulary', {}).get('diversity_ratio', 0.0)
        vocab_score = "Low" if diversity < 0.4 else ("High" if diversity > 0.7 else "Good")
        st.metric("Vocabulary Diversity", f"{diversity*100:.1f}%", 
                 delta=vocab_score)
    
    with col3:
        flesch = language_metrics.get('readability', {}).get('flesch_reading_ease', 0)
        if flesch > 0:
            readability_label = "Easy" if flesch > 70 else ("Difficult" if flesch < 30 else "Moderate")
            st.metric("Readability", f"{flesch:.0f}", 
                     delta=readability_label)
        else:
            st.metric("Readability", "N/A")
    
    with col4:
        avg_sentence = language_metrics.get('sentence_structure', {}).get('avg_words_per_sentence', 0)
        sentence_score = "Good" if 10 <= avg_sentence <= 20 else ("Complex" if avg_sentence > 20 else "Simple")
        st.metric("Avg Sentence Length", f"{avg_sentence:.1f} words", 
                 delta=sentence_score)
    
    # Detailed Visualizations
    st.subheader("📈 Detailed Analysis")
    
    # Filler words visualization
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Filler Words Breakdown**")
        filler_words_dict = language_metrics.get('filler_words', {}).get('filler_words', {})
        if filler_words_dict:
            fillers = list(filler_words_dict.keys())
            counts = list(filler_words_dict.values())
            
            fig_fillers = go.Figure()
            fig_fillers.add_trace(go.Bar(
                x=fillers,
                y=counts,
                marker_color='coral',
                name='Filler Count'
            ))
            fig_fillers.update_layout(
                title="Filler Words Detected",
                xaxis_title="Filler Word",
                yaxis_title="Count",
                height=300
            )
            st.plotly_chart(fig_fillers, use_container_width=True)
        else:
            st.info("✅ No filler words detected!")
    
    with col2:
        st.markdown("**Vocabulary Diversity**")
        vocab_stats = language_metrics.get('vocabulary', {})
        unique_words = vocab_stats.get('unique_words', 0)
        total_words = vocab_stats.get('total_words', 0)
        
        fig_vocab = go.Figure()
        fig_vocab.add_trace(go.Indicator(
            mode="gauge+number",
            value=vocab_stats.get('diversity_ratio', 0) * 100,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Diversity %"},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': "darkgreen"},
                'steps': [
                    {'range': [0, 40], 'color': "lightgray"},
                    {'range': [40, 70], 'color': "gray"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 70
                }
            }
        ))
        fig_vocab.update_layout(height=300)
        st.plotly_chart(fig_vocab, use_container_width=True)
        
        st.caption(f"Unique words: {unique_words} / Total words: {total_words}")
    
    # Readability metrics
    st.markdown("**Readability Metrics**")
    readability = language_metrics.get('readability', {})
    if readability.get('flesch_reading_ease', 0) > 0:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Flesch Reading Ease", f"{readability.get('flesch_reading_ease', 0):.0f}")
        with col2:
            st.metric("Flesch-Kincaid Grade", f"{readability.get('flesch_kincaid_grade', 0):.1f}")
        with col3:
            st.metric("SMOG Index", f"{readability.get('smog_index', 0):.1f}")
        with col4:
            st.metric("ARI", f"{readability.get('automated_readability_index', 0):.1f}")
    else:
        st.info("Readability metrics require textstat library. Install with: pip install textstat")
    
    # Sentence structure
    st.markdown("**Sentence Structure**")
    sentence_stats = language_metrics.get('sentence_structure', {})
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Sentences", sentence_stats.get('sentence_count', 0))
    with col2:
        st.metric("Long Sentences (>25 words)", sentence_stats.get('long_sentences_count', 0))
    with col3:
        st.metric("Short Sentences (<10 words)", sentence_stats.get('short_sentences_count', 0))
    
    # Repetition analysis
    repetition_stats = language_metrics.get('repetition', {})
    most_repeated = repetition_stats.get('most_repeated', [])
    
    if most_repeated:
        st.markdown("**Word Repetition**")
        col1, col2 = st.columns([1, 2])
        
        with col1:
            repetition_score = repetition_stats.get('repetition_score', 0.0)
            st.metric("Repetition Score", f"{repetition_score:.1f}%")
        
        with col2:
            st.markdown("**Most Repeated Words:**")
            repeated_text = ", ".join([f"**{word}** ({count}x)" for word, count in most_repeated[:10]])
            st.markdown(repeated_text)
    
    # Tone analysis
    st.markdown("**Tone & Engagement**")
    tone_stats = language_metrics.get('tone', {})
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Engagement Score", f"{tone_stats.get('engagement_score', 0):.1f}%")
    with col2:
        st.metric("Confidence Indicators", tone_stats.get('confidence_indicators', 0))
    with col3:
        st.metric("Questions", tone_stats.get('question_count', 0))
    with col4:
        st.metric("Exclamations", tone_stats.get('exclamation_count', 0))
    
    # Feedback and Recommendations
    st.header("Feedback & Recommendations")
    
    for i, recommendation in enumerate(feedback['recommendations'], 1):
        st.info(f"{i}. {recommendation}")
    
    # Summary scores
    st.subheader("Summary Scores")
    scores = feedback['scores']
    
    score_colors = {
        'high': '🔴',
        'moderate': '🟡',
        'low': '🟢',
        'low_engagement': '🟡',
        'engaging': '🟢',
        'good': '🟢',
        'difficult': '🔴',
        'easy': '🟢',
        'complex': '🟡',
        'simple': '🟡',
        'issues': '🟡'
    }
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        score_key = scores.get('filler_words', 'N/A')
        st.markdown(f"**Filler Words:** {score_colors.get(score_key, '⚪')} {score_key.title() if score_key != 'N/A' else 'N/A'}")
    with col2:
        score_key = scores.get('vocabulary', 'N/A')
        st.markdown(f"**Vocabulary:** {score_colors.get(score_key, '⚪')} {score_key.title() if score_key != 'N/A' else 'N/A'}")
    with col3:
        score_key = scores.get('readability', 'N/A')
        st.markdown(f"**Readability:** {score_colors.get(score_key, '⚪')} {score_key.title() if score_key != 'N/A' else 'N/A'}")
    with col4:
        score_key = scores.get('sentence_structure', 'N/A')
        st.markdown(f"**Structure:** {score_colors.get(score_key, '⚪')} {score_key.title() if score_key != 'N/A' else 'N/A'}")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        score_key = scores.get('repetition', 'N/A')
        st.markdown(f"**Repetition:** {score_colors.get(score_key, '⚪')} {score_key.title() if score_key != 'N/A' else 'N/A'}")
    with col2:
        score_key = scores.get('tone', 'N/A')
        st.markdown(f"**Tone:** {score_colors.get(score_key, '⚪')} {score_key.title().replace('_', ' ') if score_key != 'N/A' else 'N/A'}")
    with col3:
        score_key = scores.get('grammar', 'N/A')
        st.markdown(f"**Grammar:** {score_colors.get(score_key, '⚪')} {score_key.title() if score_key != 'N/A' else 'N/A'}")
