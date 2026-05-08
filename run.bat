@echo off
setlocal

cd Scripts

if not exist "venv" (
    echo Creating venv...
    python -m venv venv
)

echo Activating venv...
call venv\Scripts\activate

echo Installing packages...
python -m pip install -r requirements.txt

echo Starting bot...
python main.py

pause