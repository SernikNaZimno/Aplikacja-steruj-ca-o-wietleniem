#!/bin/bash
# Script to run the MQTT light switch simulator

echo "Starting Light Switch Simulator..."

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

# Start simulator
echo ""
echo "============================================"
echo "Starting MQTT Light Switch Simulator..."
echo "============================================"
echo "Make sure FastAPI server is running"
echo "And MQTT broker is available"
echo ""
python simulator/light_switch_simulator.py
