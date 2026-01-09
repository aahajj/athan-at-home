#!/bin/bash

# Path to your Python virtual environment
VENV_PATH="../.env"

# Absolute path to your Python app
APP_PATH="./main.py"

# Function to start the app
start() {
    if pgrep -f "$APP_PATH" > /dev/null; then
        echo "Athan is already running."
        exit 0
    fi

    # Activate virtual environment
    source "$VENV_PATH/bin/activate"

    # Ensure output directory exists
    mkdir -p out

    # Run app detached from terminal
    nohup python3 "$APP_PATH" > out/athan.log 2>&1 &

    # Deactivate venv in the shell (optional)
    deactivate

    echo "Athan started."
}

# Function to stop the app
stop() {
    PIDS=$(pgrep -f "$APP_PATH")
    if [ -z "$PIDS" ]; then
        echo "Athan is not running."
        exit 0
    fi

    echo "Stopping Athan..."
    kill $PIDS
    echo "Athan stopped."
}

# Command-line handling
case "$1" in
    a)
        start
        ;;
    d)
        stop
        ;;
    *)
        echo "Usage: $0 {a|d}"
        echo "  a = start Athan"
        echo "  d = stop Athan"
        exit 1
        ;;
esac
