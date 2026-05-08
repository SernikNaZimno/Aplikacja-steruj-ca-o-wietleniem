#!/bin/bash
# Shell script to run the lighting control application

echo "Starting Lighting Control Application..."

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install requirements
echo "Installing dependencies..."
pip install -r requirements.txt

# Start MQTT Broker
echo ""
echo "============================================"
echo "Starting MQTT Broker..."
echo "============================================"
echo "Make sure Mosquitto is installed and running"
echo "OR run: mosquitto -v"
echo ""

# Start FastAPI server
echo ""
echo "============================================"
echo "Starting FastAPI Server..."
echo "============================================"
echo "API will be available at: http://localhost:8000"
echo "Swagger UI: http://localhost:8000/docs"
echo ""
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
