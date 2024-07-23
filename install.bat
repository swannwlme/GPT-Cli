@echo off
setlocal enabledelayedexpansion

REM Check if running as Administrator
openfiles >nul 2>&1
if %errorlevel% equ 0 (
  echo Please do not run this script as Administrator
  exit /b 1
)

REM Check if Python is installed
where python >nul 2>&1
if %errorlevel% neq 0 (
  echo Error: you need to install Python and add it to the PATH in order to use gpt_cli.
  exit /b 1
)

REM Check if pip is installed
where pip >nul 2>&1
if %errorlevel% neq 0 (
  echo Error: you need to install pip and add it to the PATH in order to use gpt_cli.
  exit /b 1
)

REM Install the required Python packages
pip install -r data_files/requirements.txt

REM Prompt user to install gpt command
set /p answer=Do you also want to be able to use gpt <prompt> with gptc <prompt> ? (y/n):

REM Remove the gpt_cli directory if it exists
if exist "%USERPROFILE%\gpt_cli" (
  rmdir /s /q "%USERPROFILE%\gpt_cli"
)

REM Remove the gptc command if it exists
if exist "%USERPROFILE%\gptc.bat" (
  del "%USERPROFILE%\gptc.bat"
)

REM Remove the gpt command if it exists
if exist "%USERPROFILE%\gpt.bat" (
  del "%USERPROFILE%\gpt.bat"
)

REM Create gptc command
echo @echo off > "%USERPROFILE%\gptc.bat"
echo python "%USERPROFILE%\gpt_cli\gpt_cli.py" %%* >> "%USERPROFILE%\gptc.bat"

REM Add gptc to the PATH (user path)
setx PATH "%PATH%;%USERPROFILE%"

REM Optionally create gpt command
if /i "!answer!"=="y" (
  copy "%USERPROFILE%\gptc.bat" "%USERPROFILE%\gpt.bat"
)

REM Create the gpt_cli directory and copy gpt_cli.py
mkdir "%USERPROFILE%\gpt_cli"
copy "data_files\gpt_cli.py" "%USERPROFILE%\gpt_cli"

echo.
echo Installation complete, have fun :)
