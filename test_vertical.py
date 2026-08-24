from src.video_processor import convert_to_vertical


input_video = "outputs/test_clip.mp4"
output_video = "outputs/test_vertical.mp4"


convert_to_vertical(
    input_video,
    output_video
)

print("Vertical video created successfully.")
print(f"Output: {output_video}")