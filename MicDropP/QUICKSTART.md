# Quick Start Guide 🚀

## Step-by-Step Setup Procedure

### 1. **Install Python Dependencies**

First, make sure you have Python 3.8 or higher installed. Then install all required packages:

```bash
pip install -r requirements.txt
```

**Note**: This will install:
- Streamlit (web framework)
- librosa, pydub, soundfile (audio processing)
- speech-recognition (transcription)
- plotly (visualizations)
- And other dependencies

### 2. **Download NLP Models** (Optional for now, needed for Phase 2)

For language analysis (coming soon), you'll need:

```bash
# NLTK data
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"

# spaCy model
python -m spacy download en_core_web_sm
```

### 3. **Run the Application**

Start the Streamlit app:

```bash
streamlit run app.py
```

The app will automatically open in your browser at `http://localhost:8501`

### 4. **Test Voice Analysis**

1. Navigate to **"🎙️ Voice Analysis"** in the sidebar
2. Click **"Choose an audio file"**
3. Upload an audio file (MP3, WAV, M4A, etc.)
4. Wait for processing (usually 10-30 seconds)
5. Review your results!

## How It Works

### Voice Analysis Pipeline

1. **Audio Loading** (`utils/audio_processor.py`)
   - Converts uploaded file to numpy array
   - Normalizes sample rate to 22050 Hz

2. **Transcription** (`utils/audio_processor.py`)
   - Uses Google Speech Recognition API
   - Converts speech to text for language analysis

3. **Pace Calculation**
   - Counts words from transcription
   - Calculates words per minute (WPM)
   - Compares to ideal range (140-160 WPM)

4. **Pause Detection**
   - Analyzes audio energy levels
   - Identifies silence regions (>0.3 seconds)
   - Counts and measures pause durations

5. **Pitch Analysis**
   - Extracts pitch using librosa's piptrack
   - Calculates mean, variation, and range
   - Detects monotony (lack of pitch variation)

6. **Volume Analysis**
   - Calculates RMS energy over time
   - Measures volume consistency
   - Identifies volume variations

7. **Feedback Generation** (`utils/feedback_generator.py`)
   - Scores each metric
   - Generates personalized recommendations
   - Provides actionable advice

### Visualization

The app creates interactive charts using Plotly:
- **Pace Gauge**: Shows WPM with ideal range indicators
- **Pause Chart**: Visualizes pauses over time
- **Pitch Graph**: Shows pitch variation throughout speech
- **Volume Graph**: Displays volume consistency over time

## Project Structure Explained

```
MicDrop/
├── app.py                    # Main entry point - handles routing
├── pages/                    # Individual analysis pages
│   ├── voice_analysis.py     # ✅ Complete - Voice metrics
│   ├── language_analysis.py  # 🚧 Coming soon
│   ├── body_language_analysis.py  # 🚧 Coming soon
│   └── comprehensive_report.py    # 🚧 Coming soon
├── utils/                    # Core processing functions
│   ├── audio_processor.py    # Audio loading, transcription, analysis
│   └── feedback_generator.py # Generates recommendations
└── requirements.txt          # All Python dependencies
```

## Next Steps (Development Roadmap)

### Phase 2: Language Analysis
- Implement filler word detection
- Add readability metrics
- Analyze sentence structure
- Generate language-specific feedback

### Phase 3: Body Language Analysis
- Integrate MediaPipe for pose detection
- Analyze gestures and posture
- Detect eye contact patterns
- Video processing pipeline

### Phase 4: Integration
- Combine all three analyses
- Create comprehensive scoring system
- Add progress tracking
- Export reports

## Troubleshooting

### "Could not understand audio" error
- **Cause**: Poor audio quality or background noise
- **Solution**: Use clearer audio, reduce background noise

### Import errors
- **Cause**: Missing dependencies
- **Solution**: Run `pip install -r requirements.txt` again

### Slow processing
- **Cause**: Long audio files or slow internet (for transcription)
- **Solution**: Use shorter clips (< 5 minutes) for testing

### Audio format not supported
- **Cause**: Uncommon audio format
- **Solution**: Convert to MP3 or WAV using online tools

## Tips for Best Results

1. **Audio Quality**: 
   - Use a quiet environment
   - Minimize background noise
   - Speak clearly into microphone

2. **File Format**:
   - WAV or MP3 work best
   - Ensure file is not corrupted

3. **Duration**:
   - 30 seconds to 5 minutes ideal
   - Longer files take more time to process

4. **Content**:
   - Natural speech works best
   - Avoid music or sound effects

## Understanding Your Results

### Pace (WPM)
- **< 120 WPM**: Too slow - may lose audience attention
- **120-180 WPM**: Good range
- **> 180 WPM**: Too fast - may be hard to follow

### Pauses
- **Too few**: Speech may feel rushed
- **3-15 pauses**: Good for emphasis and clarity
- **Too many**: May indicate hesitation or lack of preparation

### Pitch Variation
- **Monotone**: Limited variation - may sound boring
- **Varied**: Good variation - engaging and expressive
- **Too varied**: May sound overly dramatic

### Volume
- **Consistent**: Good - maintains clarity
- **Inconsistent**: May indicate nervousness or poor technique

## Need Help?

- Check the main `README.md` for detailed documentation
- Review `PLAN.md` for the full project roadmap
- Ensure all dependencies are installed correctly

