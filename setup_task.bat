@echo off
echo Setting up AIEngineerPack Monitor to run automatically at system startup...
powershell -Command "Start-Process powershell -ArgumentList '-ExecutionPolicy Bypass -File \"%~dp0setup_auto_startup.ps1\"' -Verb RunAs"
echo.
echo If UAC prompt appeared and you clicked Yes, the task should be created.
echo Please check the output of the PowerShell window for confirmation.
pause 