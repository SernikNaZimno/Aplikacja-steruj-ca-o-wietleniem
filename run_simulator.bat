@echo off
REM Batch script to run the MQTT light switch simulator

echo Starting Light Switch Simulator...

REM Check if venv exists
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install requirements
echo Installing dependencies...
pip install -r requirements.txt

REM Start simulator
echo.
echo ============================================
echo Starting MQTT Light Switch Simulator...
echo ============================================
echo Make sure FastAPI server is running
echo And MQTT broker is available
echo.
python simulator\light_switch_simulator.py
