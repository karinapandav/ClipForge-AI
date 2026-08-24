from src.transcription import transcribe_video, format_transcript
from src.clip_selector import select_best_clip


video_path = "sample/test.mp4"

print("Transcribing video...")

transcript = transcribe_video(video_path)

formatted_transcript = format_transcript(transcript)

print("Sending transcript to AI clip selector...")

result = select_best_clip(formatted_transcript)

print("\nAI CLIP SELECTION")
print("=" * 60)

print(f"Start:   {result['start_time']} seconds")
print(f"End:     {result['end_time']} seconds")
print(f"Score:   {result['score']}/10")
print(f"Hook:    {result['hook']}")
print(f"Reason:  {result['reason']}")