import subprocess


def trim_video(
    input_path: str,
    output_path: str,
    start_time: float,
    end_time: float
):
    """
    Extract the selected segment from the original video.
    """

    duration = end_time - start_time

    command = [
        "ffmpeg",
        "-y",
        "-ss", str(start_time),
        "-i", input_path,
        "-t", str(duration),
        "-c:v", "libx264",
        "-c:a", "aac",
        output_path
    ]

    subprocess.run(command, check=True)

    return output_path


def convert_to_vertical(
    input_path: str,
    output_path: str
):
    """
    Convert the video to 9:16 using center cropping.
    """

    command = [
        "ffmpeg",
        "-y",
        "-i", input_path,

        "-vf",
        "crop=ih*9/16:ih,scale=1080:1920",

        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "23",

        "-c:a", "aac",

        output_path
    ]

    subprocess.run(command, check=True)

    return output_path


def burn_subtitles(
    input_path: str,
    subtitle_path: str,
    output_path: str
):
    """
    Burn ASS subtitles directly into the video.
    """

    subtitle_path = subtitle_path.replace("\\", "/").replace(":", "\\:")

    command = [
        "ffmpeg",
        "-y",
        "-i", input_path,

        "-vf",
        f"ass='{subtitle_path}'",

        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "23",

        "-c:a", "aac",

        output_path
    ]

    subprocess.run(command, check=True)

    return output_path