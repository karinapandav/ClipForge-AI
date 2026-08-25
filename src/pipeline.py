import os

from src.transcription import transcribe_video
from src.clip_selector import select_best_clip
from src.subtitles import create_ass_subtitles
from src.video_processor import (
    trim_video,
    convert_to_vertical,
    burn_subtitles
)


def generate_short(input_path: str):
    """
    Run the complete ClipForge AI pipeline.

    Video
      ↓
    Transcription
      ↓
    AI clip selection
      ↓
    Trim
      ↓
    Vertical conversion
      ↓
    ASS subtitles
      ↓
    Burn subtitles
      ↓
    Final short
    """

    os.makedirs("outputs", exist_ok=True)

    # --------------------------------------------------
    # STEP 1 — TRANSCRIPTION
    # --------------------------------------------------

    print("Step 1: Transcribing video...")

    transcript = transcribe_video(input_path)

    print("Transcription complete.")

    # --------------------------------------------------
    # STEP 2 — AI CLIP SELECTION
    # --------------------------------------------------

    print("Step 2: Selecting best clip with AI...")

    clip = select_best_clip(transcript)

    start_time = clip["start_time"]
    end_time = clip["end_time"]

    print(
        f"Selected clip: "
        f"{start_time:.2f}s → {end_time:.2f}s"
    )

    # --------------------------------------------------
    # STEP 3 — TRIM VIDEO
    # --------------------------------------------------

    trimmed_path = os.path.join(
        "outputs",
        "selected_clip.mp4"
    )

    print("Step 3: Trimming video...")

    trim_video(
        input_path=input_path,
        output_path=trimmed_path,
        start_time=start_time,
        end_time=end_time
    )

    # --------------------------------------------------
    # STEP 4 — CONVERT TO 9:16
    # --------------------------------------------------

    vertical_path = os.path.join(
        "outputs",
        "vertical_clip.mp4"
    )

    print("Step 4: Converting to vertical...")

    convert_to_vertical(
        input_path=trimmed_path,
        output_path=vertical_path
    )

    # --------------------------------------------------
    # STEP 5 — CREATE ASS SUBTITLES
    # --------------------------------------------------

    subtitle_path = os.path.join(
        "outputs",
        "captions.ass"
    )

    print("Step 5: Creating subtitles...")

    create_ass_subtitles(
        transcript=transcript,
        clip_start=start_time,
        clip_end=end_time,
        output_path=subtitle_path
    )

    # --------------------------------------------------
    # STEP 6 — BURN SUBTITLES
    # --------------------------------------------------

    final_path = os.path.join(
        "outputs",
        "final_short.mp4"
    )

    print("Step 6: Burning subtitles...")

    burn_subtitles(
        input_path=vertical_path,
        subtitle_path=subtitle_path,
        output_path=final_path
    )

    print()
    print("=" * 60)
    print("CLIPFORGE PIPELINE COMPLETE")
    print("=" * 60)
    print(f"Final video: {final_path}")

    return {
        "transcript": transcript,
        "clip": clip,
        "video_path": final_path
    }