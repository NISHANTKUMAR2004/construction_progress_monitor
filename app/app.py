import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import numpy as np
import cv2
from PIL import Image
import matplotlib.pyplot as plt
import tempfile
from src.pipeline import process_pair

# ------------------ MODEL CACHING (for faster startup) ------------------
@st.cache_resource
def load_model_cache():
    """Cache the model to avoid reloading on every rerun."""
    from src.inference import model
    return model

# Load cached model
_ = load_model_cache()

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="AI Construction Monitor", layout="wide")

# ------------------ CUSTOM CSS (ANIMATIONS) ------------------
st.markdown("""
<style>
.main {
    background-color: #0E1117;
    color: white;
}

.card {
    padding: 20px;
    border-radius: 15px;
    background: linear-gradient(145deg, #1e1e2f, #2a2a40);
    box-shadow: 0 0 20px rgba(0,0,0,0.5);
    animation: fadeIn 1s ease-in-out;
}

@keyframes fadeIn {
    from {opacity: 0; transform: translateY(20px);}
    to {opacity: 1; transform: translateY(0);}
}

.metric {
    font-size: 22px;
    font-weight: bold;
    color: #00FFAA;
}
</style>
""", unsafe_allow_html=True)

# ------------------ TITLE ------------------
st.title("🏗️ AI Construction Progress Monitor")

st.markdown("### 🚀 Upload aerial images and detect construction changes using AI")

# ------------------ SIDEBAR ------------------
st.sidebar.title("⚙️ Controls")
threshold = st.sidebar.slider("Detection Sensitivity", 0.1, 0.9, 0.3)

# ------------------ UPLOAD ------------------
col1, col2 = st.columns(2)

with col1:
    file1 = st.file_uploader("Upload BEFORE Image", type=["png", "jpg"])

with col2:
    file2 = st.file_uploader("Upload AFTER Image", type=["png", "jpg"])

# ------------------ PROCESS ------------------
if file1 and file2:

    try:
        img1 = np.array(Image.open(file1))
        img2 = np.array(Image.open(file2))

        # Validate image dimensions
        if img1.shape[0] < 50 or img1.shape[1] < 50 or img2.shape[0] < 50 or img2.shape[1] < 50:
            st.error("❌ Images must be at least 50x50 pixels")
        elif len(img1.shape) != 3 or len(img2.shape) != 3:
            st.error("❌ Images must be in RGB/BGR format (3 channels)")
        else:
            # Use temporary files with proper cleanup
            with tempfile.TemporaryDirectory() as tmpdir:
                temp1_path = os.path.join(tmpdir, "temp1.png")
                temp2_path = os.path.join(tmpdir, "temp2.png")
                
                cv2.imwrite(temp1_path, cv2.cvtColor(img1, cv2.COLOR_RGB2BGR))
                cv2.imwrite(temp2_path, cv2.cvtColor(img2, cv2.COLOR_RGB2BGR))

                if st.button("🚀 Run AI Analysis"):

                    progress_bar = st.progress(0)

                    for i in range(100):
                        progress_bar.progress(i + 1)

                    with st.spinner("Running AI model..."):
                        try:
                            img1, img2, change_cv, change_dl, highlighted, score, progress = process_pair(
                                temp1_path, temp2_path
                            )
                        except Exception as e:
                            st.error(f"❌ Error during analysis: {str(e)}")
                            st.stop()

                        st.divider()

                        # ------------------ METRICS ------------------
                        colA, colB, colC = st.columns(3)

                        colA.markdown(f"<div class='card'><div class='metric'>SSIM: {score:.2f}</div></div>", unsafe_allow_html=True)
                        colB.markdown(f"<div class='card'><div class='metric'>Progress: {progress:.2f}%</div></div>", unsafe_allow_html=True)
                        colC.markdown(f"<div class='card'><div class='metric'>AI Confidence: {(1-score)*100:.1f}%</div></div>", unsafe_allow_html=True)

                        st.divider()

                        # ------------------ IMAGES ------------------
                        col1, col2, col3 = st.columns(3)

                        with col1:
                            st.image(img1, caption="Before")

                        with col2:
                            st.image(img2, caption="After")

                        with col3:
                            st.image(highlighted, caption="Detected Changes")

                        st.divider()

                        # ------------------ CHART ------------------
                        st.subheader("📊 Progress Visualization")

                        fig, ax = plt.subplots()
                        ax.bar(["Completed", "Remaining"], [progress, 100-progress])
                        ax.set_ylabel("Percentage")
                        st.pyplot(fig)

                        st.divider()

                        # ------------------ AI EXPLANATION ------------------
                        st.subheader("🧠 AI Explanation")

                        def generate_explanation(progress):
                            if progress < 5:
                                return "Minimal construction detected."
                            elif progress < 20:
                                return "Early-stage construction activity."
                            elif progress < 50:
                                return "Moderate development detected."
                            else:
                                return "Major construction progress observed."

                        st.success(generate_explanation(progress))

                        # ------------------ DOWNLOAD REPORT ------------------
                        st.subheader("📄 Download Report")

                        report_text = f"""
        Construction Analysis Report

        SSIM Score: {score:.2f}
        Progress: {progress:.2f}%

        Interpretation:
        {generate_explanation(progress)}
        """

                        st.download_button("Download Report", report_text, file_name="report.txt")
    except Exception as e:
        st.error(f"❌ Error loading images: {str(e)}")