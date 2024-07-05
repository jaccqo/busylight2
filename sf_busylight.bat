@echo off
REM Run the Python script
python server.py

REM Check if the last command was successful
if %errorlevel% neq 0 (
    echo There was an error running the Python script.
    echo Error code: %errorlevel%
) else (
    echo The Python script ran successfully.
)