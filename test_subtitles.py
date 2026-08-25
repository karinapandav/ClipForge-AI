from src.transcription import transcribe_video
from src.subtitles import create_ass_subtitles


video_path = "sample/test.mp4"
subtitle_path = "outputs/test_subtitles.ass"

print("Transcribing video...")

transcript = transcribe_video(video_path)

print("Generating ASS subtitles...")

create_ass_subtitles(
    transcript=transcript,
    clip_start=53.16,
    clip_end=68.28,
    output_path=subtitle_path
)

print("Subtitle file created:")
print(subtitle_path)