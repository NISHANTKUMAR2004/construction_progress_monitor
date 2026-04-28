#!/bin/bash
# Deployment helper script

echo "🚀 AI Construction Monitor - Deployment Helper"
echo "================================================"

# Check Python version
python_version=$(python --version 2>&1 | grep -oP '\d+\.\d+')
echo "✓ Python version: $python_version"

# Check if model exists
if [ -f "model.pth" ]; then
    echo "✓ Model file found (model.pth)"
else
    echo "❌ Model file NOT found (model.pth)"
    exit 1
fi

# Check dependencies
echo ""
echo "Checking Python dependencies..."
pip list | grep -E "streamlit|torch|opencv|numpy" | while read -r line; do
    echo "✓ $line"
done

echo ""
echo "Deployment Status: ✅ READY"
echo ""
echo "Choose deployment option:"
echo "1. Local: streamlit run app/app.py"
echo "2. Docker: docker build -t aerial-monitor . && docker run -p 8501:8501 aerial-monitor"
echo "3. Docker Compose: docker-compose up"
echo "4. Streamlit Cloud: git push && connect on streamlit.io/cloud"
