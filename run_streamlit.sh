#!/bin/bash

# MenuLens Streamlit App Runner
# This script runs the Streamlit testing interface

echo "🍽️  Starting MenuLens Streamlit App..."
echo ""

# # Check if virtual environment exists
# if [ ! -d "backend/venv" ]; then
#     echo "❌ Virtual environment not found. Creating one..."
#     cd backend
#     python3 -m venv venv
#     cd ..
# fi

# # Activate virtual environment
# echo "Activating virtual environment..."
# source backend/venv/bin/activate

# # Install dependencies if needed
# echo "Installing dependencies..."
# pip install -q -r backend/requirements.txt

echo ""
echo "✅ Dependencies installed!"
echo ""
echo "Starting Streamlit app at http://localhost:8501"
echo "Make sure the FastAPI backend is running at http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop"
echo ""

# Run Streamlit
streamlit run streamlit_app.py
