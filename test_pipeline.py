from src.pipeline import generate_short


video_path = "sample/test.mp4"

result = generate_short(video_path)

print("\nRESULT")
print("=" * 50)
print(f"Video:    {result['video_path']}")
print(f"Start:    {result['start_time']:.2f}s")
print(f"End:      {result['end_time']:.2f}s")
print(f"Score:    {result['score']}/10")
print(f"Hook:     {result['hook']}")
print(f"Reason:   {result['reason']}")