from src.video_processor import trim_video


input_video = "sample/test.mp4"
output_video = "outputs/test_clip.mp4"

trim_video(
    input_video,
    output_video,
    start_time=53.16,
    end_time=68.28
)

print("Video clip created successfully.")
print(f"Output: {output_video}")