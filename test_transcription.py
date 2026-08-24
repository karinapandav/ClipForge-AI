from src.transcription import transcribe_video, format_transcript


video_path = "sample/test.mp4"

transcript = transcribe_video(video_path)

formatted = format_transcript(transcript)

print("\nFORMATTED TRANSCRIPT\n")
print("=" * 60)
print(formatted)