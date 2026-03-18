import whisper

whisper_model = whisper.load_model("base")

IMPORTANT_WORDS = ["important", "key", "ai", "result", "conclusion"]

def transcribe(video_path):
    result = whisper_model.transcribe(video_path)
    return result["segments"]

def format_time(seconds):
    mins = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{mins:02d}:{secs:02d}"

def detect_highlights(segments):
    highlights = []
    
    for seg in segments:
        text = seg["text"].lower()
        score = 0
        
        for word in IMPORTANT_WORDS:
            if word in text:
                score += 2
        
        if len(text.split()) > 8:
            score += 1
        
        highlights.append({
            "start": format_time(seg["start"]),
            "text": seg["text"],
            "highlight": score >= 2
        })
    
    return highlights