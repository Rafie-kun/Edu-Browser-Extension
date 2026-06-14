@echo off
REM =============================================================================
REM start.bat
REM =============================================================================
REM THE LEVER
REM
REM This batch file is the single "lever" the player pulls to power on the
REM entire redstone contraption. Double-click it (or run it from a terminal)
REM and it will:
REM
REM   1. Activate the .venv (virtual environment) - so we use the project's
REM      own Python and libraries, NOT the global system Python.
REM   2. Launch the FastAPI Command Block (main.py) via uvicorn, with
REM      --reload so code changes are picked up automatically.
REM   3. Wait 3 seconds to give the server a moment to boot up.
REM   4. Open index.html (the Player Interface) in your default browser.
REM
REM NOTE: The uvicorn server keeps running in THIS window. Closing this
REM       window (or pressing Ctrl+C) will shut the server down.
REM =============================================================================

echo ============================================================
echo  COURSE MATERIAL AGGREGATOR - Powering On the Contraption
echo ============================================================

REM --- Step 1: Activate the virtual environment ---
echo [1/4] Activating virtual environment (.venv)...
call .venv\Scripts\activate

IF NOT EXIST ".venv\Scripts\activate.bat" (
    echo.
    echo [ERROR] Could not find .venv\Scripts\activate.bat
    echo         Make sure you've created the virtual environment first:
    echo             py -m venv .venv
    echo         and installed dependencies:
    echo             .venv\Scripts\pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)

REM --- Step 2: Start the FastAPI Command Block ---
echo [2/4] Starting the FastAPI server (main.py) on http://127.0.0.1:8000 ...
start "Course Aggregator API" cmd /k "call .venv\Scripts\activate && py -m uvicorn main:app --reload"

REM --- Step 3: Give the server a moment to boot up ---
echo [3/4] Waiting 3 seconds for the server to wake up...
timeout /t 3 /nobreak >nul

REM --- Step 4: Launch the Player Interface ---
echo [4/4] Opening index.html in your default browser...
start "" "index.html"

echo.
echo ============================================================
echo  Contraption is live!
echo    - API:  http://127.0.0.1:8000
echo    - UI:   index.html (opened in browser)
echo.
echo  Tip: If the UI shows "API Offline", give the server window
echo       a few more seconds to finish starting, then refresh.
echo.
echo  To stop the server, close the "Course Aggregator API" window.
echo ============================================================
echo.
pause