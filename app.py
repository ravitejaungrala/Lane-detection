import streamlit as st
import numpy as np
import matplotlib.image as mpimg
from FindLaneLines import FindLaneLines
import os
import time

# Set page configuration (MUST BE THE FIRST STREAMLIT COMMAND)
st.set_page_config(page_title="Lane Line Detection", layout="wide")

# Custom CSS for styling and animations
st.markdown(
    """
    <style>
    .main {
        background-color: #f5f5f5;
    }
    .header {
        text-align: center;
        font-size: 36px;
        font-weight: bold;
        color: #2c3e50;
        margin-top: 20px;
        animation: fadeIn 2s;
    }
    .logo-container {
        display: flex;
        justify-content: center;
        align-items: center;
        background: linear-gradient(90deg, #4b6cb7, #182848);
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        animation: slideIn 1.5s;
    }
    .logo-container img {
        max-width: 100%;
        height: auto;
        animation: zoomIn 1.5s;
    }
    .upload-section {
        margin-top: 30px;
        margin-bottom: 30px;
        background: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        animation: fadeIn 2s;
    }
    .output-section {
        margin-top: 30px;
        background: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        animation: fadeIn 2s;
    }
    .sidebar {
        background: linear-gradient(180deg, #4b6cb7, #182848);
        color: white;
        padding: 20px;
        border-radius: 10px;
        animation: slideIn 1.5s;
    }
    .sidebar h1 {
        color: white;
    }
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    @keyframes slideIn {
        from { transform: translateY(-50px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
    @keyframes zoomIn {
        from { transform: scale(0.5); opacity: 0; }
        to { transform: scale(1); opacity: 1; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Streamlit app
def main():
    # Sidebar for team members and guide
    with st.sidebar:
        st.markdown('<div class="sidebar">', unsafe_allow_html=True)
        st.title("Team Members")
        st.write("1. 21A21A6159-U.N.V.RAVI TEJA")
        st.write("2. 21A21A6138-M.ANAKAMMARAO")
        st.write("3. 21A21A6148-P.SHIVA MUKESH")
        st.write("4. 21A21A6136-M.L.S.TEJAS")
        st.write("5. 21A21A6129-K.RESHI CHARAN")
        st.markdown("---")
        st.title("Under the Guidance of:")
        st.write("Mr. M.N.V. Viswanadh, M.Tech (Asst.Professor)")
        st.markdown('</div>', unsafe_allow_html=True)

    # Main page layout
    # College Logo
    # st.markdown('<div class="logo-container">', unsafe_allow_html=True)
    # st.image("main-logo.jpg", use_container_width=True)
    # st.markdown('</div>', unsafe_allow_html=True)

    # Project Title
    st.markdown('<div class="header">Lane Detection For Self-Driving Cars</div>', unsafe_allow_html=True)


    # File uploader for image or video
    st.markdown('<div class="upload-section">', unsafe_allow_html=True)
    st.subheader("Upload an Image or Video")
    file = st.file_uploader("Choose a file", type=["jpg", "jpeg", "png", "mp4"], key="file_uploader")
    st.markdown('</div>', unsafe_allow_html=True)

    if file is not None:
        file_details = {"filename": file.name, "filetype": file.type, "filesize": file.size}
        st.write(file_details)

        if file.type.startswith('image'):
            # Process image
            st.write("Processing image...")
            findLaneLines = FindLaneLines()
            img = mpimg.imread(file)
            out_img = findLaneLines.forward(img)
            st.markdown('<div class="output-section">', unsafe_allow_html=True)
            st.subheader("Processed Image")
            st.image(out_img, caption="Processed Image", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        elif file.type.startswith('video'):
            # Process video
            st.write("Processing video...")
            findLaneLines = FindLaneLines()
            with open("temp_video.mp4", "wb") as f:
                f.write(file.getbuffer())
            findLaneLines.process_video("temp_video.mp4", "output_video.mp4")
            st.markdown('<div class="output-section">', unsafe_allow_html=True)
            st.subheader("Processed Video")
            st.video("output_video.mp4")
            st.markdown('</div>', unsafe_allow_html=True)

            # Add a small delay to ensure the file is no longer in use
            time.sleep(2)

            # Clean up temporary files
            try:
                os.remove("temp_video.mp4")
                os.remove("output_video.mp4")
            except PermissionError as e:
                st.error(f"Failed to delete temporary files: {e}")

if __name__ == "__main__":
    main()