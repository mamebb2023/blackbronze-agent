@echo off
setlocal

echo Checking if Python is installed...

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
  echo Python is not installed. Downloading and installing Python...

  :: Download Python installer
  curl -o python-installer.exe https://www.python.org/ftp/python/3.9.7/python-3.9.7-amd64.exe
  echo Python installer downloaded.
  echo Installing Python silently...
  start /wait python-installer.exe /quiet InstallAllUsers=1 PrependPath=1
  del python-installer.exe
  echo Python installation completed.
)

echo Checking if the virtual environment exists...

if not exist ".\bb-agent-env" (
  echo Virtual environment 'bb-agent-env' not found. Creating it now...
  python -m venv .\bb-agent-env
  echo Virtual environment created successfully.
)

echo Activating the virtual environment...
call .\bb-agent-env\Scripts\activate

echo Installing requirements...
pip install -q -r .\requirements.txt
if %errorlevel% neq 0 (
  echo Error occurred while installing requirements. Exiting...
  exit /b 1
)
echo Requirements installed successfully.

echo Setting PYTHONPATH to project root...
set PYTHONPATH=%cd%

echo Running the agent with the provided API key...

if "%1"=="" (
  echo Please provide the BB_API_KEY as an argument.
  echo Example: install.bat YOUR_API_KEY
  exit /b 1
)

python .\metrics\agent.py --BB_API_KEY %1

:: Check if the command succeeded
if %errorlevel% equ 0 (
  echo BB Agent is running
) else (
  echo BB Agent failed to start
)

endlocal
