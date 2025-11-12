# AI Public Speaking Coach - Project Plan

## Overview
A free Streamlit-based application that analyzes voice, language, and body language to provide comprehensive public speaking feedback.

## Core Features

### 1. Voice Analysis
**Metrics to Analyze:**
- **Pace/Speed**: Words per minute, speaking rate
- **Pitch**: Average pitch, pitch variation, monotony detection
- **Pauses**: Frequency and duration of pauses, filler words ("um", "uh", "like")
- **Volume**: Average volume, volume variation, consistency
- **Clarity**: Articulation quality, pronunciation
- **Energy**: Voice energy and enthusiasm level

**Technical Stack:**
- `librosa` - Audio analysis (pitch, tempo, spectral features)
- `pydub` - Audio processing
- `speech_recognition` or `whisper` - Speech-to-text transcription
- `webrtcvad` - Voice activity detection

### 2. Language Analysis
**Metrics to Analyze:**
- **Clarity**: Sentence structure, complexity
- **Word Choice**: Vocabulary diversity, jargon usage
- **Grammar**: Grammatical errors
- **Structure**: Organization, transitions, coherence
- **Tone**: Formality, confidence, engagement
- **Filler Words**: Detection and frequency
- **Repetition**: Repeated phrases or words

**Technical Stack:**
- `spaCy` or `NLTK` - NLP processing
- `textstat` - Readability metrics
- Custom analysis for speech patterns
- OpenAI API (optional) - Advanced language understanding

### 3. Body Language Analysis
**Metrics to Analyze:**
- **Posture**: Upright vs. slouched, body alignment
- **Gestures**: Hand movements, frequency, appropriateness
- **Eye Contact**: Direction of gaze (if face visible)
- **Facial Expressions**: Engagement, confidence indicators
- **Movement**: Stationary vs. excessive movement
- **Presence**: Overall stage presence

**Technical Stack:**
- `MediaPipe` - Pose estimation, face detection, hand tracking
- `OpenCV` - Video processing
- `moviepy` - Video handling
- Custom analysis for gesture patterns

## Application Architecture

### Streamlit App Structure
```
app.py (main entry point)
├── pages/
│   ├── voice_analysis.py
│   ├── language_analysis.py
│   ├── body_language_analysis.py
│   └── comprehensive_report.py
├── utils/
│   ├── audio_processor.py
│   ├── video_processor.py
│   ├── language_analyzer.py
│   └── feedback_generator.py
├── requirements.txt
└── README.md
```

### User Flow
1. **Upload/Record**: User uploads audio/video or records directly
2. **Processing**: System processes the media
3. **Analysis**: All three analyses run (or selected ones)
4. **Results**: Visualized feedback with scores and recommendations
5. **Export**: Option to download report

## Technical Implementation Plan

### Phase 1: Setup & Voice Analysis
- [ ] Set up Streamlit app structure
- [ ] Implement audio upload/recording
- [ ] Basic voice analysis (pace, pauses, volume)
- [ ] Speech-to-text transcription
- [ ] Voice metrics visualization

### Phase 2: Language Analysis
- [ ] Text processing pipeline
- [ ] Language metrics calculation
- [ ] Filler word detection
- [ ] Readability and structure analysis
- [ ] Language feedback generation

### Phase 3: Body Language Analysis
- [ ] Video upload/recording support
- [ ] MediaPipe integration for pose/face/hand detection
- [ ] Body language metrics calculation
- [ ] Gesture and posture analysis
- [ ] Body language visualization

### Phase 4: Integration & Polish
- [ ] Combine all three analyses
- [ ] Comprehensive feedback report
- [ ] Score calculation and recommendations
- [ ] UI/UX improvements
- [ ] Performance optimization

## Dependencies

### Core
- `streamlit` - Web framework
- `numpy` - Numerical operations
- `pandas` - Data handling

### Audio Processing
- `librosa` - Audio analysis
- `pydub` - Audio manipulation
- `soundfile` - Audio I/O
- `speech_recognition` or `openai-whisper` - Transcription

### Video Processing
- `opencv-python` - Video processing
- `mediapipe` - Pose/face/hand detection
- `moviepy` - Video editing
- `Pillow` - Image processing

### NLP
- `spacy` - NLP processing
- `nltk` - Natural language toolkit
- `textstat` - Readability metrics

### Utilities
- `plotly` or `matplotlib` - Visualizations
- `scipy` - Scientific computing

## File Size & Performance Considerations
- **Audio**: Support common formats (mp3, wav, m4a)
- **Video**: Support mp4, webm; consider compression
- **Processing**: Use efficient algorithms, consider caching
- **Streamlit**: Optimize for cloud deployment (Streamlit Cloud)

## Future Enhancements
- Real-time feedback during recording
- Comparison with previous sessions
- Practice exercises and drills
- Customizable feedback criteria
- Multi-language support
- Integration with presentation slides analysis

## Challenges & Solutions

### Challenge 1: Video Processing Performance
- **Solution**: Use efficient MediaPipe models, process in chunks, cache results

### Challenge 2: Accurate Body Language Analysis
- **Solution**: Combine multiple signals (pose, face, hands), use confidence thresholds

### Challenge 3: Real-time Processing
- **Solution**: For MVP, focus on post-recording analysis; real-time can be Phase 2

### Challenge 4: Free API Limits
- **Solution**: Use open-source libraries (librosa, MediaPipe, spaCy) instead of paid APIs

## Success Metrics
- Accurate voice metrics (pace, pitch, pauses)
- Reliable language analysis (filler words, clarity)
- Functional body language detection (posture, gestures)
- User-friendly interface
- Fast processing (< 30 seconds for 1-minute video)

STARTING IT: 
cd /Users/theonic/Documents/GitHub/Aalto/MicDropGit/MicDropP && source venv312/bin/activate && streamlit run app.py

