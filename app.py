import os

import streamlit as st

from src.pipeline import generate_short


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="ClipForge AI",
    page_icon="🎬",
    layout="centered"
)


# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("🎬 ClipForge AI")

st.subheader("Long Video → AI Short")

st.write(
    "Upload a long-form video and let AI identify "
    "and generate a strong short-form clip."
)


# --------------------------------------------------
# FILE UPLOAD
# --------------------------------------------------

uploaded_file = st.file_uploader(
    "Upload a video",
    type=["mp4", "mov", "mkv", "avi"]
)


# --------------------------------------------------
# GENERATE BUTTON
# --------------------------------------------------

if uploaded_file is not None:

    st.video(uploaded_file)

    if st.button("🚀 Generate Short", type="primary"):

        # Create directories if they don't exist
        os.makedirs("sample", exist_ok=True)
        os.makedirs("outputs", exist_ok=True)

        # Save uploaded video
        input_path = os.path.join(
            "sample",
            uploaded_file.name
        )

        with open(input_path, "wb") as file:
            file.write(uploaded_file.getbuffer())

        # --------------------------------------------------
        # PIPELINE
        # --------------------------------------------------

        with st.status(
            "Running ClipForge pipeline...",
            expanded=True
        ) as status:

            st.write("🎙️ Transcribing video...")
            
            result = generate_short(input_path)

            status.update(
                label="✅ ClipForge pipeline complete!",
                state="complete",
                expanded=False
            )

        # --------------------------------------------------
        # AI ANALYSIS
        # --------------------------------------------------

        st.divider()

        st.header("🧠 AI Clip Analysis")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Viral Score",
                f"{result['score']}/10"
            )

        with col2:
            duration = (
                result["end_time"]
                - result["start_time"]
            )

            st.metric(
                "Clip Duration",
                f"{duration:.1f}s"
            )

        st.subheader("Hook")

        st.info(result["hook"])

        st.subheader("Why this clip?")

        st.write(result["reason"])

        # --------------------------------------------------
        # FINAL VIDEO
        # --------------------------------------------------

        st.divider()

        st.header("🎬 Generated Short")

        video_path = result["video_path"]

        if os.path.exists(video_path):

            with open(video_path, "rb") as video_file:
                video_bytes = video_file.read()

            st.video(video_bytes)

            st.download_button(
                label="⬇️ Download Short",
                data=video_bytes,
                file_name="clipforge_short.mp4",
                mime="video/mp4"
            )

        else:

            st.error(
                "The pipeline completed but the final video "
                "could not be found."
            )