import speech_recognition as sr
from pydub import AudioSegment
import os
import logging

logger = logging.getLogger(__name__)

def transcribe_audio(audio_path: str) -> tuple[str, float]:
    """
    Transcribe audio file to text using Google Speech Recognition
    
    Args:
        audio_path: Path to audio file (MP3/WAV/M4A)
        
    Returns:
        tuple: (transcribed_text, duration_in_seconds)
    """
    try:
        recognizer = sr.Recognizer()
        
        file_ext = os.path.splitext(audio_path)[1].lower()
        
        if file_ext in ['.mp3', '.m4a']:
            logger.info(f"Converting {file_ext} to WAV")
            audio = AudioSegment.from_file(audio_path)
            wav_path = audio_path.replace(file_ext, '_temp.wav')
            audio.export(wav_path, format='wav')
            duration = len(audio) / 1000.0  # Convert to seconds
            audio_path = wav_path
        else:
            audio = AudioSegment.from_wav(audio_path)
            duration = len(audio) / 1000.0
        
        with sr.AudioFile(audio_path) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)
        
        if '_temp.wav' in audio_path and os.path.exists(audio_path):
            os.remove(audio_path)
        
        logger.info(f"Transcribed {duration:.1f}s of audio")
        return text.strip(), duration
        
    except sr.UnknownValueError:
        logger.error("Could not understand audio")
        return "Could not transcribe audio - speech unclear", 0.0
    except Exception as e:
        logger.error(f"Audio transcription error: {str(e)}")
        return f"Error transcribing audio: {str(e)}", 0.0