@echo off

REM Clearing the screen
test&cls

REM Remove any previous mp4 files
echo [92mCurrent folder has been cleaned up[0m
IF EXIST "*.mp4" (
    DEL /Q *.mp4
)
echo.

:: Prompt the user for the speedup
set /p fps="Enter the FPS value (e.g. 10 for 10 frames per second): "

echo.
echo Creating a dynamic trendline animation with the following settings: [92mFPS=%fps%[0m...
python GenerateAnimation.py %fps%
echo [92mAnimation created[0m
echo.

PAUSE