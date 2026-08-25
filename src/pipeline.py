from src.transcription import transcribe_video
from src.clip_selector import select_best_clip
from src.subtitles import create_ass_subtitles
from src.video_processor import (
    trim_video,
    convert_to_vertical,
    burn_subtitles
)


def generate_short(video_path: str):
    """
    Run the complete ClipForge pipeline.

    Video
        ↓
    Transcription
        ↓
    AI clip selection
        ↓
    Video trimming
        ↓
    Vertical conversion
        ↓
    Subtitle generation
        ↓
    Caption burning
    """

    print("\n=== CLIPFORGE AI PIPELINE ===\n")

    # --------------------------------------------------
    # 1. TRANSCRIPTION
    # --------------------------------------------------

    print("[1/6] Transcribing video...")

    transcript = transcribe_video(video_path)

    print("✓ Transcription complete")

    # --------------------------------------------------
    # 2. AI CLIP SELECTION
    # --------------------------------------------------

    print("\n[2/6] Asking AI to select the best clip...")

    clip = select_best_clip(transcript)

    start_time = clip["start_time"]
    end_time = clip["end_time"]

    print("✓ Clip selected")
    print(f"  Start: {start_time:.2f}s")
    print(f"  End:   {end_time:.2f}s")
    print(f"  Score: {clip['score']}/10")
    print(f"  Hook:  {clip['hook']}")

    # --------------------------------------------------
    # 3. TRIM VIDEO
    # --------------------------------------------------

    trimmed_path = "outputs/selected_clip.mp4"

    print("\n[3/6] Trimming video...")

    trim_video(
        input_path=video_path,
        output_path=trimmed_path,
        start_time=start_time,
        end_time=end_time
    )

    print("✓ Clip trimmed")

    # --------------------------------------------------
    # 4. CONVERT TO VERTICAL
    # --------------------------------------------------

    vertical_path = "outputs/vertical.mp4"

    print("\n[4/6] Converting to 9:16...")

    convert_to_vertical(
        input_path=trimmed_path,
        output_path=vertical_path
    )

    print("✓ Vertical video created")

    # --------------------------------------------------
    # 5. GENERATE SUBTITLES
    # --------------------------------------------------

    subtitle_path = "outputs/captions.ass"

    print("\n[5/6] Generating captions...")

    create_ass_subtitles(
        transcript=transcript,
        clip_start=start_time,
        clip_end=end_time,
        output_path=subtitle_path
    )

    print("✓ ASS subtitles created")

    # --------------------------------------------------
    # 6. BURN SUBTITLES
    # --------------------------------------------------

    final_path = "outputs/final_short.mp4"

    print("\n[6/6] Burning captions into video...")

    burn_subtitles(
        input_path=vertical_path,
        subtitle_path=subtitle_path,
        output_path=final_path
    )

    print("✓ Final video created")

    print("\n=== PIPELINE COMPLETE ===")
    print(f"Output: {final_path}")

    return {
        "video_path": final_path,
        "start_time": start_time,
        "end_time": end_time,
        "score": clip["score"],
        "hook": clip["hook"],
        "reason": clip["reason"]
    }