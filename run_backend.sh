#!/bin/bash

# MenuLens Backend API Runner
# This script runs the FastAPI backend server

echo "🚀 Starting MenuLens Backend API..."
echo ""

# Check if virtual environment exists
if [ ! -d "backend/venv" ]; then
    echo "❌ Virtual environment not found. Creating one..."
    cd backend
    python3 -m venv venv
    cd ..
fi

# Activate virtual environment
echo "Activating virtual environment..."
source backend/venv/bin/activate

# Install dependencies if needed
echo "Installing dependencies..."
pip install -q -r backend/requirements.txt

echo ""
echo "✅ Dependencies installed!"
echo ""
echo "Starting FastAPI server at http://localhost:8000"
echo "API Documentation: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop"
echo ""

# Run backend
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
