from src.video_processor import burn_subtitles


input_video = "outputs/vertical.mp4"
subtitle_file = "outputs/test_subtitles.ass"
output_video = "outputs/captioned_vertical.mp4"

print("Burning subtitles into video...")

burn_subtitles(
    input_path=input_video,
    subtitle_path=subtitle_file,
    output_path=output_video
)

print("Done!")
print(f"Output: {output_video}")