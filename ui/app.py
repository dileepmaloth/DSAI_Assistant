

import streamlit as st
import requests
import json

st.set_page_config(
    page_title="Agentic Assistant",
    layout="wide"
)

st.title("Agentic Assistant")
st.write("Assistant for text, images, PDFs, and audio files")


if "history" not in st.session_state:
    st.session_state.history = []


with st.sidebar:
    st.header("Supported Features")

    st.write("Input Types:")
    st.write("- Text")
    st.write("- Images (JPG, PNG)")
    st.write("- PDFs")
    st.write("- Audio (MP3, WAV, M4A)")

    st.write("")
    st.write("Tasks:")
    st.write("- Summarization")
    st.write("- Sentiment Analysis")
    st.write("- Code Explanation")
    st.write("- YouTube Transcripts")
    st.write("- Text Extraction")
    st.write("- Q&A")

    st.divider()

    if st.button("Clear History"):
        st.session_state.history = []
        st.rerun()


col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Input")
    text_input = st.text_area(
        "Enter text",
        height=150,
        placeholder="Type here or upload a file"
    )

with col2:
    st.subheader("File Upload")
    uploaded_file = st.file_uploader(
        "Upload file",
        type=["jpg", "jpeg", "png", "pdf", "mp3", "wav", "m4a"]
    )


if st.button("Process"):
    if not text_input and not uploaded_file:
        st.warning("Please enter text or upload a file")
    else:
        with st.spinner("Processing"):
            try:
                data = {"text": text_input}
                files = None

                if uploaded_file:
                    files = {
                        "file": (
                            uploaded_file.name,
                            uploaded_file.getvalue()
                        )
                    }

                response = requests.post(
                    "http://localhost:8000/run",
                    data=data,
                    files=files,
                    timeout=60
                )

                if response.status_code == 200:
                    result = response.json()

                    st.session_state.history.append(
                        {
                            "input": text_input or f"[File: {uploaded_file.name}]",
                            "result": result
                        }
                    )

                    st.success("Done")
                else:
                    st.error(f"API error: {response.status_code}")

            except Exception as e:
                st.error(str(e))

st.divider()

if st.session_state.history:
    st.subheader("Results")

    for index, item in enumerate(reversed(st.session_state.history)):
        title = f"Query {len(st.session_state.history) - index}"

        with st.expander(title, expanded=index == 0):
            result = item["result"]

            if result.get("extracted_text"):
                st.write("Extracted Text")
                st.text(result["extracted_text"][:500])

                if result.get("ocr_confidence"):
                    st.write(
                        f"OCR confidence: {result['ocr_confidence']:.2f}"
                    )

            if result.get("duration"):
                st.write(
                    f"Audio duration: {result['duration']:.1f} seconds"
                )

            st.write("Result")

            if result.get("result"):
                st.write(result["result"])

        if item["result"].get("logs"):
            with st.expander(f"Logs for query {len(st.session_state.history) - index}"):
                for log in item["result"]["logs"]:
                    st.write(log)

else:
    st.write("Enter text or upload a file to start")

st.divider()
st.write("Built with FastAPI and Streamlit")
