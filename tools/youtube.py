from youtube_transcript_api import YouTubeTranscriptApi
import re
import logging

logger = logging.getLogger(__name__)

def extract_video_id(text: str) -> str | None:
    patterns = [
        r'(?:youtube\.com\/watch\?v=|youtu\.be\/)([a-zA-Z0-9_-]{11})',
        r'(?:youtube\.com\/embed\/)([a-zA-Z0-9_-]{11})',
        r'(?:youtube\.com\/v\/)([a-zA-Z0-9_-]{11})'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(1)
    
    return None

def fetch_youtube_transcript(text: str) -> str:
    """
    Fetch YouTube video transcript
    
    Args:
        text: Text containing YouTube URL
        
    Returns:
        Transcript text or error message
    """
    try:
        video_id = extract_video_id(text)
        
        if not video_id:
            return "No valid YouTube URL found in input."
        
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        transcript_text = " ".join([entry['text'] for entry in transcript_list])
        
        logger.info(f"Fetched transcript for video {video_id}")
        return transcript_text.strip()
        
    except Exception as e:
        logger.error(f"YouTube transcript error: {str(e)}")
        return f"Could not fetch transcript. Video may not have captions available."