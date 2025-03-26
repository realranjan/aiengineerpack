@echo off
echo Starting AIEngineerPack website monitor...
start /min pythonw website_monitor.py
echo Monitor is now running in the background.
echo You can check the monitor_data folder for updates.
pause 