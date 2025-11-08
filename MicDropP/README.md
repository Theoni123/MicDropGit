# 🎤 MicDrop - AI Public Speaking Coach

A free, comprehensive AI-powered public speaking coach that analyzes voice, language, and body language to help you improve your presentation skills.

## Features

### 🎙️ Voice Analysis (Implemented)
- **Pace**: Words per minute, speaking rate
- **Pitch**: Average pitch, variation, monotony detection
- **Pauses**: Frequency and duration analysis
- **Volume**: Consistency and variation tracking
- **Clarity**: Audio quality assessment

### 📝 Language Analysis (Coming Soon)
- Clarity and sentence structure
- Word choice and vocabulary diversity
- Filler word detection
- Grammar and structure analysis
- Tone and engagement level

### 👤 Body Language Analysis (Coming Soon)
- Posture and body alignment
- Gesture detection and frequency
- Eye contact analysis
- Facial expression recognition
- Movement and presence analysis

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd MicDrop
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   # For Phase 1 (Voice Analysis) - recommended for Python 3.13
   pip install -r requirements-phase1.txt
   
   # Or for full installation (requires Python 3.11 or 3.12 for some packages)
   pip install -r requirements.txt
   ```
   
   **Note**: Some packages (like MediaPipe) don't support Python 3.13 yet. Use `requirements-phase1.txt` for Phase 1 features, or use Python 3.11/3.12 for full installation.

4. **Download NLTK data** (for language analysis)
   ```bash
   python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
   ```

5. **Download spaCy model** (for language analysis)
   ```bash
   python -m spacy download en_core_web_sm
   ```

## Usage

1. **Run the Streamlit app**
   ```bash
   streamlit run app.py
   ```

2. **Open your browser**
   - The app will automatically open at `http://localhost:8501`
   - Or navigate manually to the URL shown in the terminal

3. **Analyze your speech**
   - Choose "Voice Analysis" from the sidebar
   - Upload an audio file (MP3, WAV, M4A, OGG, FLAC)
   - Wait for processing
   - Review your feedback and recommendations

## Supported Audio Formats

- MP3
- WAV
- M4A
- OGG
- FLAC

## Project Structure

```
MicDrop/
├── app.py                      # Main Streamlit application
├── pages/                      # Page modules
│   ├── voice_analysis.py       # Voice analysis page
│   ├── language_analysis.py    # Language analysis page
│   ├── body_language_analysis.py  # Body language analysis page
│   └── comprehensive_report.py    # Combined report page
├── utils/                      # Utility modules
│   ├── audio_processor.py      # Audio processing functions
│   └── feedback_generator.py   # Feedback generation
├── requirements.txt            # Python dependencies
├── PLAN.md                     # Detailed project plan
└── README.md                   # This file
```

## Development Status

- ✅ **Phase 1**: Voice Analysis - Complete
- 🚧 **Phase 2**: Language Analysis - In Progress
- 🚧 **Phase 3**: Body Language Analysis - Planned
- 🚧 **Phase 4**: Integration & Polish - Planned

## Technical Stack

- **Framework**: Streamlit
- **Audio Processing**: librosa, pydub, soundfile
- **Speech Recognition**: openai-whisper (offline, no API key needed)
- **Visualization**: Plotly, Matplotlib
- **NLP**: spaCy, NLTK (for Phase 2)
- **Video Processing**: MediaPipe, OpenCV (for Phase 3)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is free and open source.

## Notes

- The speech recognition uses OpenAI Whisper (offline, no API key needed)
- First transcription will download the Whisper model (~150MB) - this only happens once
- Processing time depends on audio length (typically 10-30 seconds for 1-minute audio)
- Whisper works offline and doesn't require internet connection

## Troubleshooting

### Audio loading errors
- Ensure your audio file is in a supported format
- Check that the file is not corrupted
- Try converting to WAV format

### Speech recognition errors
- Check your internet connection (Google API requires internet)
- Ensure audio quality is good (minimal background noise)
- Try speaking more clearly or using a different audio file

### Import errors
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Verify your Python version (3.8+ recommended)

