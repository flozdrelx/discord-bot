#!/bin/bash

cd Scripts || exit

if [ ! -d "venv" ]; then
    echo "Creating venv..."
    python3 -m venv venv
fi

echo "Activating venv..."
source venv/bin/activate

echo "Installing packages..."
python3 -m pip install -r requirements.txt

echo "Starting bot..."
python3 main.py

read -p "Press Enter to continue..."