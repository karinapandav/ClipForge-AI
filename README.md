# ClipForge AI 🎬

**AI-powered long-form video → short-form video generator**

ClipForge AI is a proof-of-concept application that automatically transforms long-form videos into short-form vertical content.

It combines **Whisper transcription, LLM-based clip selection, and FFmpeg video processing** into a simple AI pipeline.

---

## Current Pipeline

```text
Long-form Video
       ↓
Whisper Transcription
       ↓
Timestamped Transcript
       ↓
LLM Clip Analysis
       ↓
Best Clip + Score + Hook
       ↓
FFmpeg Video Processing
       ↓
9:16 Vertical Video
       ↓
Captions
       ↓
Final Short
```

## Features
🎙️ AI Transcription using faster-whisper
⏱️ Timestamped transcripts
🧠 LLM-powered clip selection
📊 AI-generated viral potential score
🎯 AI-generated hook/title
💡 AI-generated reasoning for clip selection
✂️ FFmpeg video trimming
📱 9:16 vertical video conversion
📝 Timestamp-based captions
🖥️ Simple Streamlit interface
🧩 Modular Python architecture

## Tech Stack
| Technology     | Purpose                         |
| -------------- | ------------------------------- |
| Python         | Core application                |
| faster-whisper | Video transcription             |
| OpenRouter     | LLM inference                   |
| FFmpeg         | Video processing                |
| Streamlit      | Web interface                   |
| python-dotenv  | Environment variable management |

## How It Works
1. Video Transcription

The input video is processed using faster-whisper to generate timestamped transcript segments.

Example:

[53.16s - 58.92s] Every morning in SEAL training...
[58.92s - 63.92s] ...the first thing they'd do was inspect my bed.

Timestamps are important because they allow the AI-selected content to be mapped back to the original video.

2. AI Clip Selection

The timestamped transcript is sent to an LLM.

The model evaluates the transcript based on:

Hook strength
Curiosity
Emotional impact
Usefulness
Standalone context
Conciseness
Shareability

The model returns structured information such as:

{
  "start_time": 53.16,
  "end_time": 68.28,
  "score": 9.1,
  "hook": "SEAL Training: The Bed Inspection That Built Discipline",
  "reason": "Strong hook, credibility and standalone insight."
}

The LLM decides which segment is promising, while FFmpeg performs the deterministic video processing.

3. Video Processing

The selected timestamps are passed to FFmpeg.

The video is:

Trimmed to the selected segment
Center-cropped to a 9:16 aspect ratio
Resized to 1080 × 1920
Prepared for short-form video output

Center cropping is currently used as the MVP baseline.

## Project Structure
clipforge-ai/
│
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
│
├── src/
│   ├── __init__.py
│   ├── transcription.py
│   ├── clip_selector.py
│   └── video_processor.py
│
├── test_transcription.py
├── test_clip_selector.py
├── test_video_processor.py
└── test_vertical.py

## Setup
1. Clone the repository
git clone https://github.com/YOUR_USERNAME/clipforge-ai.git
cd clipforge-ai
2. Create a virtual environment
python -m venv .venv
3. Activate the environment
Windows PowerShell:
.\.venv\Scripts\Activate.ps1
4. Install dependencies
pip install -r requirements.txt
5. Install FFmpeg
FFmpeg must be installed and available in the system PATH.
Verify:
ffmpeg -version
6. Configure the API key
Create a .env file:
OPENROUTER_API_KEY=your_api_key_here
Never commit the .env file or API keys to GitHub.

## Running the Project

Start the Streamlit application:
streamlit run app.py
The application will provide a simple interface for uploading a video and generating a short.

## Current Development Status

Proof of Concept — actively being developed.

## Completed
 Video transcription
 Timestamped transcript generation
 LLM-based clip selection
 AI clip scoring
 AI-generated hook
 AI-generated reasoning
 FFmpeg clip trimming
 9:16 vertical conversion

## In Progress
 Caption generation and burning
 End-to-end pipeline integration
 Streamlit UI refinement
 Final demo workflow

## Engineering Goal
The goal of ClipForge AI is not to reproduce an entire production video platform.
Instead, it demonstrates how multiple AI and engineering components can be combined into a working pipeline:

AI Model
   ↓
Structured Decision
   ↓
Deterministic Processing
   ↓
Media Output

The project focuses on understanding the integration between AI inference, APIs, timestamps, structured outputs, and media processing.

## Disclaimer

ClipForge AI is an educational proof-of-concept project built to demonstrate applied AI/ML engineering concepts for automated video repurposing.

