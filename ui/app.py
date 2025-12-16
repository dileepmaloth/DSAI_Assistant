# import streamlit as st
# import requests
# import json

# st.set_page_config(page_title="Agentic Assistant", page_icon="🤖", layout="wide")

# # Custom CSS for better styling
# st.markdown("""
# <style>
#     .main-header {
#         font-size: 2.5rem;
#         font-weight: bold;
#         color: #1f77b4;
#         text-align: center;
#         margin-bottom: 1rem;
#     }
#     .sub-header {
#         font-size: 1.2rem;
#         color: #666;
#         text-align: center;
#         margin-bottom: 2rem;
#     }
#     .log-box {
#         background-color: #f0f2f6;
#         padding: 1rem;
#         border-radius: 5px;
#         border-left: 4px solid #1f77b4;
#     }
#     .result-box {
#         background-color: #e8f4f8;
#         padding: 1.5rem;
#         border-radius: 5px;
#         margin-top: 1rem;
#     }
# </style>
# """, unsafe_allow_html=True)

# st.markdown('<div class="main-header">🤖 Agentic Assistant</div>', unsafe_allow_html=True)
# st.markdown('<div class="sub-header">Your intelligent assistant for text, images, PDFs, and audio</div>', unsafe_allow_html=True)

# # Initialize session state for chat history
# if 'history' not in st.session_state:
#     st.session_state.history = []

# # Sidebar for supported features
# with st.sidebar:
#     st.header("📋 Supported Features")
#     st.markdown("""
#     **Input Types:**
#     - 📝 Text
#     - 🖼️ Images (JPG, PNG)
#     - 📄 PDFs
#     - 🎵 Audio (MP3, WAV, M4A)
    
#     **Tasks:**
#     - Summarization
#     - Sentiment Analysis
#     - Code Explanation
#     - YouTube Transcripts
#     - Text Extraction
#     - Conversational Q&A
#     """)
    
#     st.divider()
    
#     if st.button("🗑️ Clear History"):
#         st.session_state.history = []
#         st.rerun()

# # Main interface
# col1, col2 = st.columns([2, 1])

# with col1:
#     st.subheader("💬 Input")
#     text_input = st.text_area(
#         "Enter your text or question:",
#         height=150,
#         placeholder="Type here or upload a file..."
#     )

# with col2:
#     st.subheader("📎 File Upload")
#     uploaded_file = st.file_uploader(
#         "Upload file",
#         type=['jpg', 'jpeg', 'png', 'pdf', 'mp3', 'wav', 'm4a'],
#         help="Supported: Images, PDFs, Audio files"
#     )

# # Run button
# if st.button("🚀 Process", type="primary", use_container_width=True):
#     if not text_input and not uploaded_file:
#         st.warning("Please provide text input or upload a file.")
#     else:
#         with st.spinner("🔄 Processing..."):
#             try:
#                 # Prepare request
#                 files = None
#                 data = {"text": text_input}
                
#                 if uploaded_file:
#                     files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
                
#                 # Call API
#                 response = requests.post(
#                     "http://localhost:8000/run",
#                     data=data,
#                     files=files,
#                     timeout=60
#                 )
                
#                 if response.status_code == 200:
#                     result = response.json()
                    
#                     # Add to history
#                     st.session_state.history.append({
#                         "input": text_input or f"[File: {uploaded_file.name}]",
#                         "result": result
#                     })
                    
#                     st.success("✅ Processing complete!")
#                 else:
#                     st.error(f"API Error: {response.status_code}")
                    
#             except Exception as e:
#                 st.error(f"❌ Error: {str(e)}")

# # Display results and history

# # Display results and history
# st.divider()

# if st.session_state.history:
#     st.subheader("📜 Results")
    
#     # Show most recent first
#     for idx, item in enumerate(reversed(st.session_state.history)):
#         with st.expander(f"Query {len(st.session_state.history) - idx}: {item['input'][:50]}...", expanded=(idx==0)):
#             result = item['result']
            
#             # Show extracted text if available
#             if result.get('extracted_text'):
#                 st.markdown("**📝 Extracted Text:**")
#                 with st.container():
#                     st.markdown(f'<div class="log-box">{result["extracted_text"][:500]}...</div>', unsafe_allow_html=True)
                
#                 # Show confidence if available
#                 if result.get('ocr_confidence'):
#                     st.caption(f"OCR Confidence: {result['ocr_confidence']:.2%}")
            
#             # Show duration for audio
#             if result.get('duration'):
#                 st.info(f"🎵 Audio Duration: {result['duration']:.1f} seconds")
            
#             # Show result
#             st.markdown("**🎯 Result:**")
#             if result.get('result'):
#                 st.markdown(f'<div class="result-box">{result["result"]}</div>', unsafe_allow_html=True)
        
#         # MOVE THIS OUTSIDE THE EXPANDER - UNINDENT IT
#         # Show logs
#         if item['result'].get('logs'):
#             with st.expander(f"🔍 View Processing Logs for Query {len(st.session_state.history) - idx}"):
#                 for log in item['result']['logs']:
#                     st.text(f"• {log}")
# else:
#     st.info("👋 Welcome! Enter text or upload a file to get started.")

# st.divider()
# st.markdown("""
# <div style='text-align: center; color: #666; font-size: 0.9rem;'>
#     Built with LangGraph • FastAPI • Streamlit
# </div>
# """, unsafe_allow_html=True)




import streamlit as st
import requests
import json

st.set_page_config(
    page_title="Agentic Assistant",
    layout="wide"
)

st.title("Agentic Assistant")
st.write("Assistant for text, images, PDFs, and audio files")

# keep history
if "history" not in st.session_state:
    st.session_state.history = []

# sidebar
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

# layout
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

# run button
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

# results
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
