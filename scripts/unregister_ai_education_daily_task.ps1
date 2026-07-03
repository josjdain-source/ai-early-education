# Unregister Windows Scheduled Task: "AI Early Education Daily Watch"
# Run: powershell -ExecutionPolicy Bypass -File scripts\unregister_ai_education_daily_task.ps1

$ErrorActionPreference = "Stop"
$TaskName = "AI Early Education Daily Watch"

$task = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
if ($null -eq $task) {
    Write-Host "Task '$TaskName' not found (nothing to remove)."
    exit 0
}

Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
Write-Host "Unregistered task: '$TaskName'."
