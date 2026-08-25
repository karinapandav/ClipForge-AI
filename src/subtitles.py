def seconds_to_ass_time(seconds: float) -> str:
    """
    Convert seconds into ASS timestamp format.

    Example:
    65.5 -> 0:01:05.50
    """

    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)

    remaining_seconds = seconds % 60
    whole_seconds = int(remaining_seconds)

    centiseconds = int(
        round((remaining_seconds - whole_seconds) * 100)
    )

    if centiseconds == 100:
        whole_seconds += 1
        centiseconds = 0

    return (
        f"{hours}:"
        f"{minutes:02d}:"
        f"{whole_seconds:02d}."
        f"{centiseconds:02d}"
    )


def create_ass_subtitles(
    transcript: list,
    clip_start: float,
    clip_end: float,
    output_path: str
):
    """
    Create an ASS subtitle file for the selected clip.

    Only transcript segments that overlap the selected
    clip are included.
    """

    header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,60,&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,1,0,0,0,100,100,0,0,1,3,1,2,80,80,250,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

    lines = [header]

    for segment in transcript:

        # Ignore segments completely outside selected clip
        if segment["end"] <= clip_start:
            continue

        if segment["start"] >= clip_end:
            continue

        # Adjust timestamps relative to the selected clip
        start = max(segment["start"], clip_start) - clip_start
        end = min(segment["end"], clip_end) - clip_start

        text = segment["text"].strip()

        if not text:
            continue

        start_ass = seconds_to_ass_time(start)
        end_ass = seconds_to_ass_time(end)

        # ASS uses \N for line breaks
        text = text.replace("\n", r"\N")

        line = (
            f"Dialogue: 0,"
            f"{start_ass},"
            f"{end_ass},"
            f"Default,,0,0,0,,"
            f"{text}"
        )

        lines.append(line)

    with open(output_path, "w", encoding="utf-8") as file:
        file.write("\n".join(lines))

    return output_path