import os
import json

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


def select_best_clip(transcript: str):
    """
    Send the timestamped transcript to an LLM
    and ask it to select the strongest short-form clip.
    """

    api_key = os.getenv("OPENROUTER_API_KEY")

    if not api_key:
        raise ValueError("OPENROUTER_API_KEY is not set.")

    client = OpenAI(
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1"
    )

    prompt = f"""
You are an expert short-form video editor.

Analyze the following timestamped transcript and identify
the single strongest segment for a short-form vertical video.

The selected clip must:

- Be between 15 and 60 seconds.
- Have a strong hook.
- Make sense without requiring the rest of the video.
- Provide useful, interesting, emotional, or surprising content.
- Have strong short-form/social-media potential.
- Avoid starting in the middle of an idea if possible.
- Prefer a clear beginning and ending.

Score the clip from 0 to 10 based on:

- Hook strength
- Curiosity
- Emotional impact
- Usefulness
- Standalone context
- Conciseness
- Shareability

Return ONLY a JSON object in this exact format:

{{
    "start_time": 0.0,
    "end_time": 0.0,
    "score": 0.0,
    "hook": "Short hook/title",
    "reason": "Why this segment is a strong short-form clip."
}}

Do not include Markdown.
Do not include ```json.
Do not include explanations outside the JSON object.

Timestamped transcript:

{transcript}
"""

    response = client.chat.completions.create(
        model="openrouter/free",
        messages=[
            {
                "role": "system",
                "content": (
                    "You select high-quality short-form video clips. "
                    "Return ONLY the requested JSON object. "
                    "Do not include explanations, reasoning, or Markdown."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    content = response.choices[0].message.content

    if not content:
        raise ValueError("LLM returned an empty response.")

    content = content.strip()

    # Remove Markdown code fences if the model ignored our instruction.
    if content.startswith("```"):
        lines = content.splitlines()

        if lines[0].startswith("```"):
            lines = lines[1:]

        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]

        content = "\n".join(lines).strip()

    # Find the JSON object even if the model
    # included additional text around it.
    start = content.find("{")
    end = content.rfind("}")

    if start == -1 or end == -1:
        raise ValueError(
            f"LLM response did not contain a JSON object:\n{content}"
        )

    json_text = content[start:end + 1]

    try:
        result = json.loads(json_text)

    except json.JSONDecodeError:
        raise ValueError(
            f"LLM returned invalid JSON:\n{content}"
        )

    # Validate the fields required by the pipeline.
    required_fields = [
        "start_time",
        "end_time",
        "score",
        "hook",
        "reason"
    ]

    missing_fields = [
        field
        for field in required_fields
        if field not in result
    ]

    if missing_fields:
        raise ValueError(
            f"LLM response is missing fields: {missing_fields}"
        )

    # Basic validation of the selected timestamps.
    if result["start_time"] >= result["end_time"]:
        raise ValueError("LLM returned invalid clip timestamps.")

    duration = result["end_time"] - result["start_time"]

    if duration < 15 or duration > 60:
        raise ValueError(
            f"LLM selected a clip of {duration:.2f} seconds. "
            "Expected 15-60 seconds."
        )

    return result