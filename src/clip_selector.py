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

Return ONLY valid JSON in this exact format:

{{
    "start_time": 0.0,
    "end_time": 0.0,
    "score": 0.0,
    "hook": "Short hook/title",
    "reason": "Why this segment is a strong short-form clip."
}}

Timestamped transcript:

{transcript}
"""

    response = client.chat.completions.create(
        model="openrouter/free",
        messages=[
            {
                "role": "system",
                "content": "You select high-quality short-form video clips."
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

    try:
        result = json.loads(content)
    except json.JSONDecodeError:
        raise ValueError(
            f"LLM returned invalid JSON:\n{content}"
        )

    return result