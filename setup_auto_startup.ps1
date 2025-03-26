$scriptPath = (Get-Location).Path
$pythonExe = (Get-Command python).Source
$monitorScript = Join-Path $scriptPath "website_monitor.py"

# Create a scheduled task to run at system startup
$taskName = "AIEngineerPack-Monitor"
$action = New-ScheduledTaskAction -Execute $pythonExe -Argument $monitorScript -WorkingDirectory $scriptPath
$trigger = New-ScheduledTaskTrigger -AtLogon
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -RunOnlyIfNetworkAvailable

# Register the task
Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Settings $settings -Description "Monitors AIEngineerPack website for updates" -Force

Write-Host "Task '$taskName' has been created successfully. The script will run automatically whenever you log in to Windows."
Write-Host "To check the task status, open Task Scheduler from Windows Start menu." 