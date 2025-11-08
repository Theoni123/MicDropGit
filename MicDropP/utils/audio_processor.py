"""
Audio processing utilities for voice analysis
"""

import librosa
import numpy as np
import soundfile as sf
from pydub import AudioSegment
import io
import whisper
import tempfile
import os

# Try to import streamlit for caching (optional)
try:
    import streamlit as st
    HAS_STREAMLIT = True
except ImportError:
    HAS_STREAMLIT = False
    st = None


def load_audio(audio_file, target_sr=22050):
    """
    Load audio file and convert to numpy array
    
    Args:
        audio_file: Uploaded file or file path
        target_sr: Target sample rate (default 22050)
    
    Returns:
        y: Audio time series
        sr: Sample rate
    """
    tmp_path = None
    wav_path = None
    try:
        # Handle Streamlit uploaded file
        if hasattr(audio_file, 'read'):
            # Get file extension from name if available
            file_ext = os.path.splitext(audio_file.name)[1].lower() if hasattr(audio_file, 'name') else '.wav'
            if not file_ext or file_ext == '':
                file_ext = '.wav'
            
            # Save to temporary file (librosa works better with actual files)
            audio_bytes = audio_file.read()
            audio_file.seek(0)  # Reset file pointer for potential reuse
            
            # Create temporary file with proper extension
            with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as tmp_file:
                tmp_file.write(audio_bytes)
                tmp_path = tmp_file.name
            
            # For formats that librosa might not handle well (m4a, aac, etc.), use pydub first
            formats_need_conversion = ['.m4a', '.aac', '.mp4', '.3gp', '.flv', '.webm']
            
            if file_ext in formats_need_conversion:
                # Convert to WAV using pydub first
                try:
                    audio = AudioSegment.from_file(tmp_path)
                    # Create WAV temp file
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as wav_file:
                        wav_path = wav_file.name
                    audio.export(wav_path, format="wav")
                    # Now load with librosa
                    y, sr = librosa.load(wav_path, sr=target_sr)
                except Exception as e2:
                    error_msg = str(e2)
                    if "ffmpeg" in error_msg.lower() or "codec" in error_msg.lower():
                        raise Exception(
                            f"Could not process {file_ext} file. This format requires ffmpeg to be installed. "
                            f"Please install ffmpeg: 'brew install ffmpeg' (macOS) or 'sudo apt-get install ffmpeg' (Linux). "
                            f"Original error: {error_msg}"
                        )
                    else:
                        raise Exception(f"Could not convert audio format {file_ext} to WAV. Error: {error_msg}")
            else:
                # Try to load with librosa directly first
                try:
                    y, sr = librosa.load(tmp_path, sr=target_sr)
                except Exception as e1:
                    # If librosa can't read it, convert to WAV using pydub
                    try:
                        audio = AudioSegment.from_file(tmp_path)
                        # Create WAV temp file
                        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as wav_file:
                            wav_path = wav_file.name
                        audio.export(wav_path, format="wav")
                        # Now load with librosa
                        y, sr = librosa.load(wav_path, sr=target_sr)
                    except Exception as e2:
                        error_msg = str(e2)
                        if "ffmpeg" in error_msg.lower() or "codec" in error_msg.lower():
                            raise Exception(
                                f"Could not process {file_ext} file. This format requires ffmpeg to be installed. "
                                f"Please install ffmpeg: 'brew install ffmpeg' (macOS) or 'sudo apt-get install ffmpeg' (Linux). "
                                f"Original error: {error_msg}"
                            )
                        else:
                            raise Exception(f"Could not load audio format {file_ext}. Librosa error: {str(e1)}. Pydub error: {error_msg}")
        else:
            # File path - determine strategy based on extension
            file_ext = os.path.splitext(audio_file)[1].lower() if isinstance(audio_file, str) else '.wav'
            formats_need_conversion = ['.m4a', '.aac', '.mp4', '.3gp', '.flv', '.webm']
            
            if file_ext in formats_need_conversion:
                # Convert to WAV using pydub first
                try:
                    audio = AudioSegment.from_file(audio_file)
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as wav_file:
                        wav_path = wav_file.name
                    audio.export(wav_path, format="wav")
                    y, sr = librosa.load(wav_path, sr=target_sr)
                except Exception as e2:
                    error_msg = str(e2)
                    if "ffmpeg" in error_msg.lower() or "codec" in error_msg.lower():
                        raise Exception(
                            f"Could not process {file_ext} file. This format requires ffmpeg to be installed. "
                            f"Please install ffmpeg: 'brew install ffmpeg' (macOS) or 'sudo apt-get install ffmpeg' (Linux). "
                            f"Original error: {error_msg}"
                        )
                    else:
                        raise Exception(f"Could not convert audio format {file_ext} to WAV. Error: {error_msg}")
            else:
                # Try direct load first
                try:
                    y, sr = librosa.load(audio_file, sr=target_sr)
                except Exception:
                    # Fallback: convert to WAV using pydub
                    try:
                        audio = AudioSegment.from_file(audio_file)
                        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as wav_file:
                            wav_path = wav_file.name
                        audio.export(wav_path, format="wav")
                        y, sr = librosa.load(wav_path, sr=target_sr)
                    except Exception as e2:
                        raise Exception(f"Could not load audio format. Error: {str(e2)}")
        
        return y, sr
    except Exception as e:
        raise Exception(f"Error loading audio: {str(e)}")
    finally:
        # Clean up temp files if we created them
        for path in [tmp_path, wav_path]:
            if path and os.path.exists(path):
                try:
                    os.unlink(path)
                except:
                    pass


def convert_to_wav(audio_file):
    """
    Convert audio file to WAV format for speech recognition
    
    Args:
        audio_file: Uploaded file
    
    Returns:
        wav_path: Path to converted WAV file
    """
    try:
        if hasattr(audio_file, 'read'):
            audio_bytes = audio_file.read()
            audio = AudioSegment.from_file(io.BytesIO(audio_bytes))
        else:
            audio = AudioSegment.from_file(audio_file)
        
        # Convert to WAV
        wav_io = io.BytesIO()
        audio.export(wav_io, format="wav")
        wav_io.seek(0)
        
        return wav_io
    except Exception as e:
        raise Exception(f"Error converting audio: {str(e)}")


# Cache Whisper model if streamlit is available
if HAS_STREAMLIT:
    @st.cache_resource
    def load_whisper_model(model_name="base"):
        """Load Whisper model with caching"""
        return whisper.load_model(model_name)
else:
    def load_whisper_model(model_name="base"):
        """Load Whisper model without caching"""
        return whisper.load_model(model_name)


def transcribe_audio(audio_file):
    """
    Transcribe audio to text using Whisper
    
    Args:
        audio_file: Uploaded audio file
    
    Returns:
        text: Transcribed text
    """
    tmp_path = None
    try:
        # Load Whisper model (cached if streamlit available)
        model = load_whisper_model("base")
        
        # Handle Streamlit uploaded file
        if hasattr(audio_file, 'read'):
            # Get file extension from name if available
            file_ext = os.path.splitext(audio_file.name)[1] if hasattr(audio_file, 'name') else '.wav'
            if not file_ext:
                file_ext = '.wav'
            
            # Save to temporary file with proper extension
            audio_bytes = audio_file.read()
            audio_file.seek(0)  # Reset file pointer for potential reuse
            
            with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as tmp_file:
                tmp_file.write(audio_bytes)
                tmp_path = tmp_file.name
        else:
            tmp_path = audio_file
        
        try:
            # Transcribe with Whisper
            result = model.transcribe(tmp_path, language="en")
            text = result["text"].strip()
            
            return text if text else "Could not understand audio"
            
        except Exception as e:
            return f"Error transcribing audio: {str(e)}"
            
    except Exception as e:
        raise Exception(f"Error transcribing audio: {str(e)}")
    finally:
        # Clean up temp file if we created it
        if tmp_path and hasattr(audio_file, 'read') and os.path.exists(tmp_path):
            try:
                os.unlink(tmp_path)
            except:
                pass


def calculate_pace(audio_file, text=None):
    """
    Calculate speaking pace (words per minute)
    
    Args:
        audio_file: Uploaded audio file
        text: Optional transcribed text (if not provided, will transcribe)
    
    Returns:
        wpm: Words per minute
        duration: Audio duration in seconds
    """
    try:
        # Get audio duration
        y, sr = load_audio(audio_file)
        duration = len(y) / sr  # Duration in seconds
        
        # Get text if not provided
        if text is None:
            text = transcribe_audio(audio_file)
        
        # Calculate WPM
        if text and text != "Could not understand audio":
            word_count = len(text.split())
            wpm = (word_count / duration) * 60 if duration > 0 else 0
        else:
            wpm = 0
        
        return wpm, duration, text
        
    except Exception as e:
        raise Exception(f"Error calculating pace: {str(e)}")


def detect_pauses(y, sr, min_pause_duration=0.3):
    """
    Detect pauses in audio
    
    Args:
        y: Audio time series
        sr: Sample rate
        min_pause_duration: Minimum pause duration in seconds
    
    Returns:
        pauses: List of (start, end) tuples for pauses
    """
    # Calculate energy
    frame_length = int(0.025 * sr)  # 25ms frames
    hop_length = int(0.010 * sr)    # 10ms hop
    
    # Calculate RMS energy
    rms = librosa.feature.rms(y=y, frame_length=frame_length, hop_length=hop_length)[0]
    
    # Normalize energy
    energy_threshold = np.percentile(rms, 20)  # Bottom 20% considered silence
    
    # Find silence regions
    is_silence = rms < energy_threshold
    
    # Convert to time
    times = librosa.frames_to_time(np.arange(len(is_silence)), sr=sr, hop_length=hop_length)
    
    # Find pause segments
    pauses = []
    in_pause = False
    pause_start = 0
    
    for i, silence in enumerate(is_silence):
        if silence and not in_pause:
            pause_start = times[i]
            in_pause = True
        elif not silence and in_pause:
            pause_end = times[i]
            pause_duration = pause_end - pause_start
            if pause_duration >= min_pause_duration:
                pauses.append((pause_start, pause_end))
            in_pause = False
    
    # Handle pause at end
    if in_pause:
        pause_end = times[-1]
        pause_duration = pause_end - pause_start
        if pause_duration >= min_pause_duration:
            pauses.append((pause_start, pause_end))
    
    return pauses


def analyze_pitch(y, sr):
    """
    Analyze pitch characteristics
    
    Args:
        y: Audio time series
        sr: Sample rate
    
    Returns:
        pitch_stats: Dictionary with pitch statistics
    """
    try:
        # Extract pitch using librosa
        pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
        
        # Get pitch values (non-zero)
        pitch_values = []
        for t in range(pitches.shape[1]):
            index = magnitudes[:, t].argmax()
            pitch = pitches[index, t]
            if pitch > 0:
                pitch_values.append(pitch)
        
        if len(pitch_values) == 0:
            return {
                'mean_pitch': 0,
                'std_pitch': 0,
                'pitch_range': 0,
                'monotony_score': 1.0  # High monotony if no pitch detected
            }
        
        pitch_values = np.array(pitch_values)
        
        # Calculate statistics
        mean_pitch = np.mean(pitch_values)
        std_pitch = np.std(pitch_values)
        pitch_range = np.max(pitch_values) - np.min(pitch_values)
        
        # Monotony score (0 = very varied, 1 = very monotone)
        # Based on coefficient of variation
        cv = std_pitch / mean_pitch if mean_pitch > 0 else 1.0
        monotony_score = 1.0 / (1.0 + cv)  # Normalize to 0-1
        
        return {
            'mean_pitch': mean_pitch,
            'std_pitch': std_pitch,
            'pitch_range': pitch_range,
            'monotony_score': monotony_score,
            'pitch_values': pitch_values
        }
        
    except Exception as e:
        raise Exception(f"Error analyzing pitch: {str(e)}")


def analyze_volume(y, sr):
    """
    Analyze volume characteristics
    
    Args:
        y: Audio time series
        sr: Sample rate
    
    Returns:
        volume_stats: Dictionary with volume statistics
    """
    try:
        # Calculate RMS energy
        frame_length = int(0.025 * sr)
        hop_length = int(0.010 * sr)
        rms = librosa.feature.rms(y=y, frame_length=frame_length, hop_length=hop_length)[0]
        
        # Convert to dB
        rms_db = librosa.amplitude_to_db(rms, ref=np.max)
        
        # Calculate statistics
        mean_volume = np.mean(rms)
        std_volume = np.std(rms)
        max_volume = np.max(rms)
        min_volume = np.min(rms)
        
        # Volume consistency (lower std = more consistent)
        volume_consistency = 1.0 / (1.0 + std_volume / mean_volume) if mean_volume > 0 else 0
        
        return {
            'mean_volume': mean_volume,
            'std_volume': std_volume,
            'max_volume': max_volume,
            'min_volume': min_volume,
            'volume_consistency': volume_consistency,
            'rms_db': rms_db
        }
        
    except Exception as e:
        raise Exception(f"Error analyzing volume: {str(e)}")

