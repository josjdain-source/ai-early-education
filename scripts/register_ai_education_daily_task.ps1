# Register Windows Scheduled Task: "AI Early Education Daily Watch"
# Runs the daily observatory pipeline (--write) every day at 07:30.
# Auto-observe only. No site edit / sitemap / deploy / upload.
# Run this yourself (with your permission): powershell -ExecutionPolicy Bypass -File scripts\register_ai_education_daily_task.ps1

$ErrorActionPreference = "Stop"

$TaskName = "AI Early Education Daily Watch"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$Bat = Join-Path $ScriptDir "run_ai_education_daily_pipeline.bat"

if (-not (Test-Path $Bat)) {
    Write-Error "BAT not found: $Bat"
    exit 1
}

$Action  = New-ScheduledTaskAction -Execute "cmd.exe" -Argument "/c `"$Bat`""
$Trigger = New-ScheduledTaskTrigger -Daily -At 7:30am
$Settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -DontStopOnIdleEnd `
    -ExecutionTimeLimit (New-TimeSpan -Minutes 30) -MultipleInstances IgnoreNew

# Register for current user, run only when logged on (no stored password needed).
Register-ScheduledTask -TaskName $TaskName -Action $Action -Trigger $Trigger `
    -Settings $Settings -Description "AI Early Education daily 7-axis observatory (auto-observe, human approval gate). No auto-publish." -Force | Out-Null

Write-Host "Registered task: '$TaskName' (daily 07:30)."
Write-Host "Runs: $Bat"
Write-Host "Verify: Get-ScheduledTask -TaskName '$TaskName'"
Write-Host "Run now (test): Start-ScheduledTask -TaskName '$TaskName'"
