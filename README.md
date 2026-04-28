# 🏗️ AI Construction Progress Monitor

An AI-powered aerial image analysis tool that detects construction progress and changes using computer vision and deep learning.

## Features

- **Dual Image Upload**: Upload before and after aerial images
- **AI-Powered Analysis**: Detects construction changes using both classical CV and deep learning models
- **Progress Metrics**: Calculates SSIM scores and construction progress percentage
- **Visual Output**: 
  - Side-by-side image comparison
  - Change detection visualization
  - Progress charts and reports
- **AI Explanation**: Generates interpretations based on detected progress levels
- **Report Generation**: Download analysis reports as text files

## Installation

### Local Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd aerial-progress-monitoring

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
.\venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Running the App

### Local Development
```bash
streamlit run app/app.py
```

The app will be available at `http://localhost:8501`

### Cloud Deployment (Streamlit Cloud)

1. Push your code to GitHub
2. Go to [Streamlit Cloud](https://streamlit.io/cloud)
3. Create a new app and select your repository
4. Set main file path to `app/app.py`
5. Deploy!

### Docker Deployment (Recommended for Production)

```bash
# Build the Docker image
docker build -t aerial-monitor .

# Run the container
docker run -p 8501:8501 aerial-monitor

# Or use docker-compose
docker-compose up
```

### Deployment Checklist

✅ **Code Quality**
- [x] Error handling for image upload
- [x] Temporary file cleanup (using `tempfile` module)
- [x] Model caching for performance
- [x] Robust model path resolution
- [x] Input validation

✅ **Configuration**
- [x] `.streamlit/config.toml` - Properly configured
- [x] `requirements.txt` - Pinned versions for reproducibility
- [x] `runtime.txt` - Python 3.10 specified
- [x] `packages.txt` - System dependencies listed

✅ **Deployment Files**
- [x] `Dockerfile` - Production-ready container
- [x] `.dockerignore` - Optimized build context
- [x] `.gitignore` - Excludes unnecessary files

✅ **Production Ready**
- Platform: ✅ Streamlit Cloud, ✅ Docker, ✅ Heroku, ✅ HuggingFace Spaces

## Project Structure

```
aerial-progress-monitoring/
├── app/
│   └── app.py              # Main Streamlit application
├── src/
│   ├── pipeline.py         # Main processing pipeline
│   ├── inference.py        # Deep learning inference
│   ├── change_detection.py # Change detection algorithms
│   ├── preprocessing.py    # Image preprocessing
│   ├── visualization.py    # Visualization utilities
│   ├── metrics.py          # Metrics calculation
│   ├── alignment.py        # Image alignment
│   ├── dataset.py          # Dataset utilities
│   ├── model.py            # Model definitions
│   ├── train.py            # Training script
│   └── utils.py            # Utility functions
├── data/
│   ├── raw/
│   │   └── LEVIR-CD/       # Training dataset (LEVIR-CD)
│   └── processed/          # Processed data
├── notebooks/              # Jupyter notebooks
├── outputs/                # Analysis outputs
├── requirements.txt        # Python dependencies
├── runtime.txt            # Python version specification
├── model.pth              # Pre-trained model weights
└── main.py                # Training/testing script
```

## Dependencies

- **streamlit**: Web framework
- **torch & torchvision**: Deep learning
- **opencv-python**: Computer vision
- **numpy**: Numerical computing
- **Pillow**: Image processing
- **matplotlib**: Visualization
- **scikit-image**: Advanced image processing

See `requirements.txt` for complete list.

## Model

The app uses a pre-trained deep learning model (`model.pth`) for construction change detection. The model is optimized for aerial imagery analysis.

## Usage

1. **Upload Images**: Select a "before" and "after" aerial image (PNG or JPG)
2. **Adjust Sensitivity**: Use the slider to control detection sensitivity (0.1 - 0.9)
3. **Run Analysis**: Click the "Run AI Analysis" button
4. **View Results**: 
   - SSIM Score (0-1, lower = more change)
   - Progress percentage
   - AI Confidence level
5. **Download Report**: Save the analysis report as a text file

## Sensitivity Levels

- **0.1-0.3**: Low sensitivity - detects major changes only
- **0.3-0.6**: Medium sensitivity - balanced detection
- **0.6-0.9**: High sensitivity - detects subtle changes

## Performance Metrics

The app calculates:
- **SSIM (Structural Similarity Index)**: Measures image similarity (0-1 scale)
- **Progress %**: Estimated construction progress based on change map
- **AI Confidence**: Inverse of SSIM score, indicating change probability

## API Reference

### Main Pipeline

```python
from src.pipeline import process_pair

img1, img2, change_cv, change_dl, highlighted, score, progress = process_pair(
    "image1.png", "image2.png"
)
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Model not loading | Ensure `model.pth` is in project root |
| Image upload fails | Check file size (max 200MB) and format (PNG/JPG) |
| Slow processing | Reduce image resolution or lower sensitivity threshold |

## System Requirements

- Python 3.10+
- 4GB RAM (minimum)
- 500MB disk space (excluding model/data)

## License

[Add your license here]

## Authors

[Your name/team]

## Contact

[Your contact information]

## Acknowledgments

- Dataset: LEVIR-CD (Change Detection dataset)
- Built with Streamlit, PyTorch, and OpenCV

---

**Last Updated**: April 2026
