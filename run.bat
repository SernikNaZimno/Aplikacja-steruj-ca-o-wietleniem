@echo off
REM Batch script to run the lighting control application

echo Starting Lighting Control Application...

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

REM Start MQTT Broker
echo.
echo ============================================
echo Starting MQTT Broker...
echo ============================================
echo Make sure Mosquitto is installed and running
echo OR run: mosquitto -v
echo.

REM Start FastAPI server
echo.
echo ============================================
echo Starting FastAPI Server...
echo ============================================
echo API will be available at: http://localhost:8000
echo Swagger UI: http://localhost:8000/docs
echo.
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
