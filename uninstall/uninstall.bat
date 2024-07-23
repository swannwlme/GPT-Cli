@echo off
setlocal

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

echo Cleanup complete.
