from faster_whisper import WhisperModel


def transcribe_video(video_path: str):
    """
    Transcribe a video and return timestamped segments.
    """

    model = WhisperModel(
        "base",
        device="cpu",
        compute_type="int8"
    )

    segments, info = model.transcribe(
        video_path,
        beam_size=5
    )

    transcript = []

    for segment in segments:
        transcript.append({
            "start": segment.start,
            "end": segment.end,
            "text": segment.text.strip()
        })

    return transcript


def format_transcript(transcript):
    """
    Convert timestamped transcript segments into
    a format suitable for an LLM.
    """

    lines = []

    for segment in transcript:
        lines.append(
            f"[{segment['start']:.2f}s - "
            f"{segment['end']:.2f}s] "
            f"{segment['text']}"
        )

    return "\n".join(lines)